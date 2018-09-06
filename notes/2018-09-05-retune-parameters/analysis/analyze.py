import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, IndexFormatter
from strtens import odftools
import colorcet as cc


class SensitivityData(object):
    def __init__(self, path, metric, value):
        '''
        path : path to directory containing csv and .npy data
        metric : either 'angle' or 'radius'
        value : value for metric in degrees or pixels
        '''

        # Set up object-wide parameters
        fn = path + \
            'r{}'.format(value) if metric == 'radius' else path + \
            'deg{}'.format(value)

        self.metric = metric
        self.value = value
        if metric == 'radius':
            self.title = '{} = {}'.format(
                metric.title(), np.round(1.2 * value, 1))
        else:
            self.title = '{} = {}'.format(metric.title(), value)

        # Reads in csv data
        print('Reading CSV')
        self.data = pd.read_csv(fn + 'results.csv', header=0,
                                index_col=[0, 1], skipinitialspace=True)

        # Creates mask
        # (Only interested in sd, sn combinations that yield
        # the correct number of peaks in the final ODF)
        print('Making mask')
        if metric == 'angle':
            self.mask = self.data['npeaks'] == 2.0
        elif metric == 'radius':
            self.mask = self.data['npeaks'] == 1.0

        # Reads the ST peak data
        print('Reading peaks')
        self.peaks = np.load(fn + 'peak_data.npy')

        # Reads the true SH coeff data
        print('Reading true SH coeffs')
        self.coeffs = np.load(fn + 'coeffs.npy')
        true_path = '/'.join(fn.split('/')[:3]) + '/true_coeffs/'
        if self.metric == 'angle':
            true_fn = 'z_phantom_nfib9x4_r8_{}deg_coeffs.npy'.format(
                self.value)
        elif self.metric == 'radius':
            true_fn = 'x_phantom_nfib9_r{}_coeffs.npy'.format(self.value)
        self.true_coeffs = np.load(true_path + true_fn)

        # Calculates true peak locations
        print('Calculating true peak locations')
        self.get_true_peaks()

        # Add columns calculated from peak and SH data
        print('Adding ODF peak error column')
        self.add_odf_peak_column()
        print('Adding ACC column')
        self.add_ACC_column()
        print('Adding JSD column')
        self.add_JSD_column()

        if metric == 'angle':
            print('Adding crossing angle column')
            self.add_crossing_angle_column()

        self.main_cols = ['ACC', 'JSD', 'ODF Peak Error', 'AUC']

        print('Creating max inds df')
        self.max_data = self.make_max_inds_df()

    def get_true_peaks(self):
        sphere = odftools.make_sphere(1500)
        odf = odftools.get_odf(self.true_coeffs, sphere)
        peaks, vals, inds = odftools.get_peaks(odf, sphere)
        self.true_peaks = peaks

    def add_odf_peak_column(self):
        n = self.data.shape[0]  # number of data points
        odf_error = np.zeros(n)

        # Still calculate for bad peaks for radius
        if self.metric == 'radius':
            # Initialize array with number of mis-identified peaks
            # Remember - mask gives sd, sn combos that yield the
            # CORRECT number of peaks
            badpeaks = np.zeros(self.mask.size - self.mask.sum())

            # looping over sd, sn combos with misidentified # of peaks
            for i, peaks in enumerate(self.peaks[~self.mask]):
                npeaks = peaks.shape[0]  # number of peaks
                badpeaks[i] = odftools.get_ang_distance(
                    peaks, np.tile(self.true_peaks, (npeaks, 1))).min()

            odf_error[~self.mask] = badpeaks

        # Trickier to sort bad peaks when npeaks=2, just set to
        # nan for crossing angle phantoms
        elif self.metric == 'angle':
            odf_error[~self.mask] = np.nan

        goodpeaks = np.zeros(self.mask.sum())
        for i, peaks in enumerate(self.peaks[self.mask]):
            goodpeaks[i] = odftools.get_ang_distance(
                peaks, self.true_peaks).mean()

        odf_error[self.mask] = goodpeaks

        self.data['ODF Peak Error'] = odf_error
        np.save('maxmins/{}_{}_PE'.format(self.metric, self.value), odf_error)

    def add_ACC_column(self):
        acc = [odftools.calc_ACC(c, self.true_coeffs) for c in self.coeffs]
        self.data['ACC'] = acc
        np.save('maxmins/{}_{}_ACC'.format(self.metric, self.value), acc)

    def add_JSD_column(self):
        sphere = odftools.make_sphere(1500)
        jsd = [odftools.calc_JSD(c, self.true_coeffs, sphere)
               for c in self.coeffs]
        self.data['JSD'] = jsd
        np.save('maxmins/{}_{}_JSD'.format(self.metric, self.value), jsd)

    def add_crossing_angle_column(self):
        true_crossing_angle = odftools.get_ang_distance(
            self.true_peaks[0], self.true_peaks[1])
        crossing_angles = np.zeros(self.data.shape[0])
        crossing_angles[~self.mask] = np.nan
        temp = []
        for peaks in self.peaks[self.mask]:
            temp.append(odftools.get_ang_distance(peaks[0], peaks[1]))
        crossing_angles[self.mask] = temp
        self.data['Crossing Angle Error'] = abs(
            crossing_angles - true_crossing_angle)

    def get_max_inds(self, col, mask=False):
        data = self.mask_data() if mask else self.data
        ind = np.where(data[col] == data[col].max())[0][0]
        if any(s in col for s in ['Error', 'Std', 'JSD']):
            ind = np.where(data[col] == data[col].min())[0][0]
        sd_max, sn_max = data.iloc[ind].name
        return sd_max, sn_max

    def get_vmin_vmax(self, col):
        # Values taken from min, max values from all crossing angle phantoms
        if col == 'ACC':
            vmin, vmax = 0.293, 0.965
        if col == 'JSD':
            vmin, vmax = 0.0271, 0.3
        if col == 'ODF Peak Error':
            vmin, vmax = 0.0, 15.0
        if col == 'AUC':
            vmin, vmax = 0.224, 0.928
        return vmin, vmax

    def make_max_inds_df(self):
        max_data = pd.DataFrame(index=self.main_cols,
                                columns=['S_d', 'S_n'],
                                dtype='float')

        for col in self.main_cols:
            sd, sn = self.get_max_inds(col, mask=True)

            max_data.loc[col]['S_d'] = sd * 1.2
            max_data.loc[col]['S_n'] = sn * 1.2
        return max_data

    def mask_data(self):
        data = self.data.copy()
        data[~self.mask] = np.nan
        return data

    def plot_im(self, col, mask=False, multiply=None, divide=None,
                save=False, path=None):

        data = self.mask_data() if mask else self.data

        fig, ax = plt.subplots()

        sigma_d = data.index.levels[0]
        sigma_n = data.index.levels[1]

        values = data[col].values
        title = '{} : {}'.format(col, self.title)

        if multiply is not None:
            multiply = [multiply] if type(multiply) == str else multiply
            for mult in multiply:
                values *= data[mult].values
                title += ' * {}'.format(mult)
        if divide is not None:
            divide = [divide] if type(divide) == str else divide
            for div in divide:
                values /= data[div].values
                title += ' / {}'.format(div)

        ax.set_title(title)
        values = values.reshape((sigma_d.size, sigma_n.size)).T

        color = cc.m_fire_r if any(
            s in col for s in ['Error', 'Std', 'JSD']) else cc.m_fire
        color.set_bad(color='gray')
        vmin, vmax = self.get_vmin_vmax(col)
        image = ax.imshow(values, cmap=color, origin='lower', vmin=vmin,
                          vmax=vmax)

        nxbins = 10
        xlabels = np.round(1.2 * sigma_d, 1)
        ax.xaxis.set_major_locator(MaxNLocator(nbins=nxbins, prune='both'))
        ax.xaxis.set_major_formatter(IndexFormatter(xlabels))
        ax.set_xlabel(r'$\sigma_D$ [$\mu$m]')

        nybins = 10
        ylabels = np.round(1.2 * sigma_n, 1)
        ax.yaxis.set_major_locator(MaxNLocator(nbins=nybins, prune='both'))
        ax.yaxis.set_major_formatter(IndexFormatter(ylabels))
        ax.set_ylabel(r'$\sigma_N$ [$\mu$m]')

        plt.colorbar(image)
        plt.tight_layout()

        if save:
            fn = title.replace(': ', '').replace(
                ' = ', '_').replace(' ', '_').replace('.', '_')

            if self.metric == 'radius':
                path += '{}/'.format(np.round(1.2 *
                                              self.value, 1)).replace('.', '_')
            else:
                path += '{}/'.format(self.value)

            if not os.path.exists(path):
                os.makedirs(path)

            fig.savefig((path + fn).replace('.', '_') +
                        '.pdf', bbox_inches='tight')
        return ax

    def scatter_plot(self, cols, save=False, path=None):
        fig, ax = plt.subplots()
        for col in cols:
            ax.scatter(self.max_data.loc[col]['S_d'],
                       self.max_data.loc[col]['S_n'],
                       label=col)
        ax.set_xlim([1, 10.5])
        ax.set_ylim([1, 12.5])
        ax.legend()
        ax.set_title('Optimal parameters for {}'.format(self.title))
        ax.set_xlabel('$\sigma_D$ [$\mu$m]')
        ax.set_ylabel('$\sigma_N$ [$\mu$m]')
        plt.tight_layout()
        if save:

            if self.metric == 'radius':
                fn = '{}_{}_best_params'.format(
                    self.metric, np.round(1.2 * self.value, 1)).replace('.', '_')
                path += '{}/'.format(np.round(1.2 *
                                              self.value, 1)).replace('.', '_')
            else:
                fn = '{}_{}_best_params'.format(self.metric, self.value)
                path += '{}/'.format(self.value)

            if not os.path.exists(path):
                os.makedirs(path)

            fig.savefig(path + fn + '.pdf', bbox_inches='tight')
        return ax

    def save_all(self, path):
        ax_scatter = self.scatter_plot(self.main_cols, save=True, path=path)
        for col in self.main_cols:
            plt.close()
            ax = self.plot_im(col, mask=True, save=True, path=path)


def plot_optimal_params(df_list, save=False, path=None):
    '''
    Input iterable list of SensitivityData objects
    '''
    cols = df_list[0].max_data.index
    axes = []
    for col in cols:
        fig, ax = plt.subplots()
        for df in df_list:
            ax.scatter(df.max_data.loc[col]['S_d'],
                       df.max_data.loc[col]['S_n'],
                       label=df.title)
        ax.set_xlim([1, 10.5])
        ax.set_ylim([1, 12.5])
        ax.legend()
        ax.set_title('Optimal parameters for {}'.format(col))
        ax.set_xlabel('$\sigma_D$ [$\mu$m]')
        ax.set_ylabel('$\sigma_N$ [$\mu$m]')
        plt.tight_layout()
        if save:
            fn = '{}_{}_best_params.pdf'.format(col, df.metric)

            if not os.path.exists(path):
                os.makedirs(path)

            fig.savefig(path + fn, bbox_inches='tight')
        axes.append(ax)

    return axes


def one_plot(df_list, save=False, path=None):
    '''
    Input iterable list of SensitivityData objects
    '''
    cols = df_list[0].max_data.index
    colors = ['C{}'.format(i) for i in range(8)]  # indicating value
    markers = ['o', '^', 's', '*', 'D']  # indicating metric
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, df in enumerate(df_list):
        for j, col in enumerate(cols):
            ax.scatter(df.max_data.loc[col]['S_d'],
                       df.max_data.loc[col]['S_n'],
                       marker=markers[j],
                       color=colors[i])
    ax.set_xlim([1, 10.5])
    ax.set_ylim([1, 12.5])

    if df_list[0].metric == 'angle':
        values = ['angle = {} deg'.format(deg)
                  for deg in list(range(15, 86, 10))]
    elif df_list[0].metric == 'radius':
        values = ['r = {} $\mu$m'.format(np.round(r * 1.2, 2))
                  for r in list(range(4, 17, 4))]

    color_artists = [plt.Line2D((0, 1), (0, 0), color=c)
                     for c in colors[:i + 1]]
    marker_artists = [plt.Line2D(
        (0, 1), (0, 0), color='k', marker=m, linestyle='') for m in markers[:j + 1]]

    ax.legend(color_artists + marker_artists,
              values + list(cols))  # , loc='center left', bbox_to_anchor=(1, 0.5))

    ax.set_title('Optimal parameters for {}'.format(df_list[0].metric))
    ax.set_xlabel('$\sigma_D$ [$\mu$m]')
    ax.set_ylabel('$\sigma_N$ [$\mu$m]')
    if save:
        fn = '{}_best_params.pdf'.format(df_list[0].metric)

        if not os.path.exists(path):
            os.makedirs(path)

        fig.savefig(path + fn, bbox_inches='tight')

    return ax
