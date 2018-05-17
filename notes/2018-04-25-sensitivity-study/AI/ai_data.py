import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, IndexFormatter
import colorcet as cc


class AI_data(object):
    def __init__(self, csvfn, metric_name):
        self.data = pd.read_csv(csvfn, header=0, index_col=[
                                0, 1], skipinitialspace=True)
        self.metric_name = metric_name

    def saveall(self, path):
        self.boxplot(save=True, path=path)
        for col in self.data.columns:
            self.plot_im(col, save=True, path=path)
        self.plot_im('AUC', multiply='Mask Mean', divide='Inv Mask Mean',
                     save=True, path=path)

    def plot_im(self, col, multiply=None, divide=None, save=False, path=None):

        fig, ax = plt.subplots()

        sigma_d = self.data.index.levels[0]
        sigma_n = self.data.index.levels[1]

        values = self.data[col].values
        title = '{}: {}'.format(self.metric_name, col)

        if multiply is not None:
            multiply = [multiply] if type(multiply) == str else multiply
            for mult in multiply:
                values *= self.data[mult].values
                title += ' * {}'.format(mult)
        if divide is not None:
            divide = [divide] if type(divide) == str else divide
            for div in divide:
                values /= self.data[div].values
                title += ' / {}'.format(div)

        ax.set_title(title)
        values = values.reshape((sigma_d.size, sigma_n.size)).T
        image = ax.imshow(values, cmap=cc.m_fire)

        nticks = 10

        xlabels = np.round(1.2 * sigma_d, 1)
        ax.xaxis.set_major_locator(MaxNLocator(nbins=nticks, prune='both'))
        ax.set_xticks(ax.get_xticks() + 1)
        ax.xaxis.set_major_formatter(IndexFormatter(xlabels))
        ax.set_xlabel(r'$\sigma_D$ [$\mu$m]')

        ylabels = np.round(1.2 * sigma_n, 1)
        ax.yaxis.set_major_locator(MaxNLocator(nbins=nticks, prune='both'))
        ax.set_yticks(ax.get_yticks() + 1)
        ax.yaxis.set_major_formatter(IndexFormatter(ylabels))
        ax.set_ylabel(r'$\sigma_N$ [$\mu$m]')

        plt.colorbar(image)
        plt.tight_layout()

        if save:
            fn = title.replace(' *', '').replace(' /',
                                                 '').replace(':', '').replace(' ', '_') + '.png'
            # fn = '{}_{}.png'.format(
            #     self.metric_name, col) if col2 is None else '{}_{}_{}.png'.format(
            #         self.metric_name, col, col2)

            fig.savefig(path + fn, bbox_inches='tight')

        return ax

    def boxplot(self, save=False, path=None):
        '''
        Boxplots of all four values
        '''
        fig, ax = plt.subplots(figsize=(10, 8))
        ax = self.data.boxplot(grid=False, ax=ax)
        ax.set_title('AI ({} Measure)'.format(self.metric_name))

        if save:
            fn = '{}_boxplots.png'.format(self.metric_name)
            fig.savefig(path + fn, bbox_inches='tight')

    def plot_AI_vs_sn(self, save=False, path=None):
        '''
        Plots AI vs. s_n for each s_d
        '''
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes = axes.flatten()

        for i, ax in enumerate(axes):
            lines = np.empty(self.data.index.levels[0].size, dtype=object)
            ax.set_xlabel('$\sigma_N$')
            ax.set_ylabel('AI')
            ax.set_title(self.data.columns[i+2])
            for j, s_d in enumerate(self.data.index.levels[0]):
                lines[j], = ax.plot(self.data.loc[s_d][self.data.columns[i+2]])

        labels = [r'$\sigma_D$ = {:.2f}'.format(
            s_d) for s_d in self.data.index.levels[0]]
        fig.suptitle(
            'AI ({} Metric) vs. $\sigma_N$'.format(self.metric_name))
        fig.legend(lines, labels, loc='right')
        fig.tight_layout(w_pad=2, h_pad=2)
        fig.subplots_adjust(top=0.9, right=0.88)

        if save:
            fn = '{}_AI_vs_sn.png'.format(self.metric_name)
            fig.savefig(path + fn, bbox_inches='tight')

    def plot_AI_vs_sd(self, save=False, path=None):
        '''
        Plots AI vs s_d for each s_n
        '''

        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes = axes.flatten()

        for i, ax in enumerate(axes):
            lines = np.empty(self.data.index.levels[1].size, dtype=object)
            ax.set_xlabel('$\sigma_D$')
            ax.set_ylabel('AI')
            ax.set_title(self.data.columns[i+2])
            for j, s_n in enumerate(self.data.index.levels[1]):
                lines[j], = ax.plot(self.data.xs(s_n, level=1)[
                                    self.data.columns[i+2]])

        labels = [r'$\sigma_N$ = {:.2f}'.format(
            s_n) for s_n in self.data.index.levels[1]]
        fig.suptitle(
            'AI ({} Metric) for constant $\sigma_N$'.format(self.metric_name))
        fig.legend(lines, labels, loc='right')
        plt.tight_layout(w_pad=2, h_pad=2)
        fig.subplots_adjust(top=0.9, right=0.88)

        if save:
            fn = '{}_AI_vs_sd.png'.format(self.metric_name)
            fig.savefig(path + fn, bbox_inches='tight')

    def plot_AUC(self, save=False, path=None):
        '''
        Difference curves
        '''

        fig, axes = plt.subplots(1, 2, figsize=(16, 8))
        axes = axes.flatten()
        lines = np.empty(self.data.index.levels[1].size, dtype=object)

        for j, s_d in enumerate(self.data.index.levels[0]):
            lines[j], = axes[0].plot(self.data.loc[s_d]['AUC'],
                                     label=r'$\sigma_D$ = {:.2f}'.format(s_d))

        axes[0].grid(True, alpha=0.5)
        axes[0].set_xlabel('$\sigma_N$')
        axes[0].set_ylabel('AUC')
        axes[0].set_title('AUC vs. $\sigma_N$')
        axes[0].legend()

        for j, s_n in enumerate(self.data.index.levels[1]):
            lines[j], = axes[1].plot(self.data.xs(s_n, level=1)['AUC'],
                                     label=r'$\sigma_N$ = {:.2f}'.format(s_n))

        axes[1].grid(True, alpha=0.5)
        axes[1].set_xlabel('$\sigma_D$')
        axes[1].set_ylabel('AUC')
        axes[1].set_title('AUC vs. $\sigma_D$')
        axes[1].legend()

        fig.suptitle('AUC ({} Metric)'.format(self.metric_name))

        plt.tight_layout(w_pad=2, h_pad=2)
        fig.subplots_adjust(top=0.9, right=0.88)

        if save:
            fn = '{}_AUC.png'.format(self.metric_name)
            fig.savefig(path + fn, bbox_inches='tight')

    def plot_diff(self, save=False, path=None):
        '''
        Difference curves
        '''

        fig, axes = plt.subplots(1, 2, figsize=(14, 8))
        axes = axes.flatten()
        lines = np.empty(self.data.index.levels[1].size, dtype=object)

        for j, s_d in enumerate(self.data.index.levels[0]):
            diff = self.data.loc[s_d]['AUC'] * self.data.loc[s_d]['Mask Mean']
            lines[j], = axes[0].plot(
                diff, label=r'$\sigma_d$ = {:.2f}'.format(s_d))

        axes[0].grid(True, alpha=0.5)
        axes[0].set_xlabel('$\sigma_N$')
        axes[0].set_ylabel(r'AUC * $\bar{AI}_{mask}$')
        axes[0].set_title('AI mean in mask scaled by AUC vs. $\sigma_N$')
        axes[0].legend()

        for j, s_n in enumerate(self.data.index.levels[1]):
            diff = self.data.xs(s_n, level=1)[
                'AUC'] * self.data.xs(s_n, level=1)['Mask Mean']
            lines[j], = axes[1].plot(
                diff, label=r'$\sigma_N$ = {:.2f}'.format(s_n))

        axes[1].grid(True, alpha=0.5)
        axes[1].set_xlabel('$\sigma_D$')
        axes[1].set_ylabel(r'AUC * $\bar{AI}_{mask}$')
        axes[1].set_title('AI mean in mask scaled by AUC vs. $\sigma_D$')
        axes[1].legend()

        fig.suptitle(
            'AUC and Mean Mask AI ({} Metric)'.format(self.metric_name))

        plt.tight_layout(w_pad=2, h_pad=2)
        fig.subplots_adjust(top=0.9, right=0.88)

        if save:
            fn = '{}_difference.png'.format(self.metric_name)
            fig.savefig(path + fn, bbox_inches='tight')
