import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from glob import glob
import strtens.odftools as odftools
from strtens.vis import show_ODF
from dipy.reconst.odf import gfa


def calc_data(save_data=True, save_img=False):

    sphere = odftools.make_sphere(1200)
    df = pd.DataFrame(columns=['ACC', 'JSD', 'RMSE', 'GFA8', 'GFA32'])
    for ID in range(1, 226):
        print(ID)
        print('Calculating metrics')
        fn32 = glob('results_32/*_{}_*_coeffs.npy'.format(ID))[0]
        fn8 = glob('results_8/*_{}_*_coeffs.npy'.format(ID))[0]
        c32 = np.load(fn32)
        c8 = np.load(fn8)

        ACC = odftools.calc_ACC(c32, c8)
        JSD = odftools.calc_JSD(c32, c8, sphere)
        RMSE = np.sqrt(((c32 - c8) ** 2).mean())

        odf8 = odftools.get_odf(c8, sphere)
        odf32 = odftools.get_odf(c32, sphere)
        gfa8 = float(gfa(odf8))
        gfa32 = float(gfa(odf32))

        df.loc[ID] = [ACC, JSD, RMSE, gfa8, gfa32]

        if save_img:
            print('Saving ODFs')
            odf32 = odftools.get_odf(c32, sphere)
            odf8 = odftools.get_odf(c8, sphere)
            show_ODF(odf32, sphere, save=True, interactive=False,
                     fn='odf_plots/sample_32_{}.png'.format(ID))
            show_ODF(odf8, sphere, save=True, interactive=False,
                     fn='odf_plots/sample_8_{}.png'.format(ID))

    if save_data:
        df.to_pickle('df_raw.pkl')

    return df


calc = False
if calc:
    df = calc_data()
else:
    df = pd.read_pickle('df_raw.pkl')


plot = True
if plot:
    bins = 50

    # Histograms

    means = np.round(df.mean(), 3)
    stds = np.round(df.std() / means * 100, 1)

    fig1, ax = plt.subplots(1, 3, figsize=(12, 5))

    ax[0].hist(df.ACC, bins=bins, color='C0')
    ax[0].set_title(
        'ACC\n' + r'$\mu = {}, \sigma = {}$'.format(means.ACC, stds.ACC) + '%')
    ax[0].set_xlabel('ACC')
    ax[0].set_ylabel('Counts')

    ax[1].hist(df.JSD, bins=bins, color='C1')
    ax[1].set_title(
        'JSD\n' + r'$\mu = {}, \sigma = {}$'.format(means.JSD, stds.JSD) + '%')
    ax[1].set_xlabel('JSD')
    ax[1].set_ylabel('Counts')

    ax[2].hist(df.RMSE, bins=bins, color='C2')
    ax[2].set_title(
        'RMSE\n' + r'$\mu = {}, \sigma = {}$'.format(means.RMSE, stds.RMSE) + '%')
    ax[2].set_xlabel('RMSE')
    ax[2].set_ylabel('Counts')
    plt.tight_layout()
    plt.savefig('plots/hists.pdf')

    # scatterplots
    fig2, ax = plt.subplots(1, 3, figsize=(12, 5))

    r = np.corrcoef(df.ACC, df.JSD)[0, 1]
    ax[0].plot(df.ACC, df.JSD, '.', color='C3')
    ax[0].set_title('ACC/JSD\nr = {}'.format(np.round(r, 3)))
    ax[0].set_xlabel('ACC')
    ax[0].set_ylabel('JSD')

    r = np.corrcoef(df.ACC, df.RMSE)[0, 1]
    ax[1].plot(df.ACC, df.RMSE, '.', color='C3')
    ax[1].set_title('ACC/RMSE\nr = {}'.format(np.round(r, 3)))
    ax[1].set_xlabel('ACC')
    ax[1].set_ylabel('RMSE')

    r = np.corrcoef(df.JSD, df.RMSE)[0, 1]
    ax[2].plot(df.JSD, df.RMSE, '.', color='C3')
    ax[2].set_title('JSD/RMSE\nr = {}'.format(np.round(r, 3)))
    ax[2].set_xlabel('JSD')
    ax[2].set_ylabel('RMSE')

    plt.tight_layout()
    plt.savefig('plots/scatter.pdf')

    # GFA
    GFA = df.GFA8
    fig, ax = plt.subplots(1, 3, figsize=(12, 5))

    r = np.corrcoef(GFA, df.ACC)[0, 1]
    ax[0].plot(GFA, df.ACC, '.')
    ax[0].set_title('GFA/ACC\nr = {}'.format(np.round(r, 3)))
    ax[0].set_xlabel('GFA')
    ax[0].set_ylabel('ACC')

    r = np.corrcoef(GFA, df.JSD)[0, 1]
    ax[1].plot(GFA, df.JSD, '.', color='C1')
    ax[1].set_title('GFA/JSD\nr = {}'.format(np.round(r, 3)))
    ax[1].set_xlabel('GFA')
    ax[1].set_ylabel('JSD')

    r = np.corrcoef(GFA, df.RMSE)[0, 1]
    ax[2].plot(GFA, df.RMSE, '.', color='C2')
    ax[2].set_title('GFA/RMSE\nr = {}'.format(np.round(r, 3)))
    ax[2].set_xlabel('GFA')
    ax[2].set_ylabel('RMSE')

    plt.tight_layout()
    plt.savefig('plots/gfa.pdf')
