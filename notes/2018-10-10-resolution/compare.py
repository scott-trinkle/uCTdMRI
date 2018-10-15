import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from strtens import odftools
from glob import glob
from dipy.reconst.odf import gfa


def calc_data(save_data=True):
    sphere = odftools.make_sphere(1200)
    df = pd.DataFrame(0, index=pd.MultiIndex.from_product(
        [[2, 3, 4, 5], list(range(1, 226))]), columns=['ACC', 'JSD', 'RMSE', 'GFA Diff'])
    for factor in range(2, 6):
        for ID in range(1, 226):
            print('{}-{}'.format(factor, ID))
            fn0 = glob(
                '../2018-09-17-bit-depth/results_32/*_{}_*_coeffs.npy'.format(ID))[0]
            fntest = glob(
                './results_{}x/*_{}_*_coeffs.npy'.format(factor, ID))[0]
            c0 = np.load(fn0)
            ctest = np.load(fntest)

            ACC = odftools.calc_ACC(c0, ctest)
            JSD = odftools.calc_JSD(c0, ctest, sphere)
            RMSE = np.sqrt(np.mean((c0 - ctest)**2))

            odf0 = odftools.get_odf(c0, sphere)
            odftest = odftools.get_odf(ctest, sphere)
            gfa0 = float(gfa(odf0))
            gfatest = float(gfa(odftest))
            gfadiff = gfatest - gfa0

            df.loc[factor, ID] = [ACC, JSD, RMSE, gfadiff]
    if save_data:
        df.to_pickle('df_raw.pkl')
    return df


calc = False
if calc:
    df = calc_data()
else:
    df = pd.read_pickle('df_raw.pkl')


fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(15, 12))
ax1, ax2 = ax[0, :]
ax3, ax4 = ax[1, :]


ax1.errorbar(range(2, 6),
             [df.loc[i].ACC.mean() for i in range(2, 6)],
             fmt='k:o',
             yerr=[df.loc[i].ACC.std() for i in range(2, 6)])
ax1.xaxis.set_ticks(range(2, 6))
ax1.xaxis.set_ticklabels(['{}x'.format(i) for i in range(2, 6)])
ax1.set_ylabel('ACC')
ax1.set_title('ACC')

ax2.errorbar(range(2, 6),
             [df.loc[i].JSD.mean() for i in range(2, 6)],
             fmt='k:o',
             yerr=[df.loc[i].JSD.std() for i in range(2, 6)])
ax2.xaxis.set_ticks(range(2, 6))
ax2.xaxis.set_ticklabels(['{}x'.format(i) for i in range(2, 6)])
ax2.set_ylabel('JSD')
ax2.set_title('JSD')

ax3.errorbar(range(2, 6),
             [df.loc[i].RMSE.mean() for i in range(2, 6)],
             fmt='k:o',
             yerr=[df.loc[i].RMSE.std() for i in range(2, 6)])
ax3.xaxis.set_ticks(range(2, 6))
ax3.xaxis.set_ticklabels(['{}x'.format(i) for i in range(2, 6)])
ax3.set_ylabel('RMSE')
ax3.set_title('RMSE')

ax4.errorbar(range(2, 6),
             [df.loc[i]['GFA Diff'].mean() for i in range(2, 6)],
             fmt='k:o',
             yerr=[df.loc[i]['GFA Diff'].std() for i in range(2, 6)])
ax4.xaxis.set_ticks(range(2, 6))
ax4.xaxis.set_ticklabels(['{}x'.format(i) for i in range(2, 6)])
ax4.set_ylabel(r'$\Delta$GFA')
ax4.set_title(r'$\Delta$GFA = GFA$_{ds}$ - GFA$_{0}$')

plt.tight_layout()
fig.savefig('plots/per_ds_factor.pdf')


for col in df.columns:
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(15, 12), sharex=True)
    ax1, ax2 = ax[0, :]
    ax3, ax4 = ax[1, :]

    nbins = 30

    ax1.hist(df.loc[2][col], bins=nbins)
    ax1.set_xlabel(col)
    ax1.set_title('2x')

    ax2.hist(df.loc[3][col], bins=nbins)
    ax2.set_xlabel(col)
    ax2.set_title('3x')

    ax3.hist(df.loc[4][col], bins=nbins)
    ax3.set_xlabel(col)
    ax3.set_title('4x')

    ax4.hist(df.loc[5][col], bins=nbins)
    ax4.set_xlabel(col)
    ax4.set_title('5x')

    [ax_i.xaxis.set_tick_params(labelbottom=True) for ax_i in ax.flatten()]

    fig.suptitle(col)

    plt.tight_layout()
    fig.subplots_adjust(top=0.95)
    fig.savefig('plots/{}.pdf'.format(col))
