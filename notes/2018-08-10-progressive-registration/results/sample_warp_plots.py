# Sample warp fields AND apply transform

import numpy as np
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt

warp_fns = glob('data/warp_*.csv')
warp_list = []
for fn in warp_fns:
    warp_list.append(pd.read_csv(fn, index_col=[1]))
warp_df = pd.concat(warp_list)
warp = warp_df.loc['warp'].set_index(['Resolution', 'Interp-pair'])
warped = warp_df.loc['warped'].set_index(['Resolution', 'Interp-pair'])

samp_warp_fns = glob('data/sample_warp_*.csv')
samp_warp_list = []
for fn in samp_warp_fns:
    samp_warp_list.append(pd.read_csv(fn, index_col=[1]))
samp_warp_df = pd.concat(samp_warp_list)
warp = samp_warp_df.loc['sample-warp'].set_index(
    ['Resolution', 'Interp-pair'])
samp_warped = samp_warp_df.loc['sample-warped'].set_index(
    ['Resolution', 'Interp-pair'])

resolutions = warp.index.levels[0]
metrics = ['MSE', 'Correlation', 'Mutual Information']

fig1, axes = plt.subplots(1, 3, figsize=(15, 8))
axes = axes.flatten()
colors = ['C0', 'C1', 'C2']
for i, met in enumerate(['MSE', 'CC', 'MI']):
    for j, interp in enumerate(['bicubic', 'bilinear', 'no_interp']):
        data = [warped.loc[res, interp][met] for res in resolutions]
        samp_data = [samp_warped.loc[res, interp][met] for res in resolutions]
        axes[i].plot(resolutions,
                     data,
                     '-x',
                     color=colors[j],
                     label='Resampled data: ' + interp.capitalize().replace('_', ' '))
        axes[i].plot(resolutions,
                     samp_data,
                     ':o',
                     color=colors[j],
                     label='Resampled transform: ' + interp.capitalize().replace('_', ' '))
    # mean_data = [warped.loc[res][met].mean() for res in resolutions]
    # axes[i].plot(resolutions, mean_data, '-ok', label='Mean')
    axes[i].set_xlabel('Voxel size ($\mu$m)')
    # axes[i].legend()
    axes[i].set_title(metrics[i])

handles, labels = axes[0].get_legend_handles_labels()
fig1.legend(handles, labels, loc='lower center', ncol=3)
fig1.suptitle('Registration performance metrics')
plt.tight_layout()
fig1.subplots_adjust(top=0.9, bottom=0.15)
fig1.savefig('plots/warped_image.pdf')


fig2, axes = plt.subplots(1, 3, figsize=(15, 8))
axes = axes.flatten()
colors = ['C{}'.format(i) for i in range(3)]
mstyle = ['o', '^', 's']
lstyle = ['-', '--', ':']

for i, met in enumerate(['MSE', 'CC', 'MI']):
    for j, interp in enumerate(warp.index.levels[1]):
        if len(interp.split('_')) == 2:
            sample_int = interp.split('_')[0].split('-')[1]
            nonsample_int = interp.split('_')[1]
        elif len(interp.split('_')) == 3:
            last = interp.split('_')[-1]
            if last == 'interp':
                nonsample_int = 'no_interp'
                sample_int = interp.split('-')[1].split('_')[0]
            else:
                nonsample_int = last
                sample_int = 'no_interp'
        else:
            nonsample_int = 'no_interp'
            sample_int = 'no_interp'

        for k, int_test in enumerate(['bicubic', 'bilinear', 'no_interp']):
            if nonsample_int == int_test:
                ms = mstyle[k]
                c = colors[k]
            if sample_int == int_test:
                ls = lstyle[k]

        data = [warp.loc[res, interp][met] for res in resolutions]
        axes[i].plot(resolutions,
                     data,
                     ms + ls,
                     color=c,
                     label=interp)
    # mean_data = [warp.loc[res][met].mean() for res in resolutions]
    # axes[i].plot(resolutions, mean_data, '-ok', label='Mean')
    axes[i].set_xlabel('Voxel size ($\mu$m)')
    axes[i].set_title(metrics[i])

from matplotlib.lines import Line2D
custom_lines = [Line2D([0], [0], marker=mstyle[i], color=colors[i])
                for i in range(3)] + [Line2D([0], [0], color='k', ls=lstyle[i]) for i in range(3)]

fig2.suptitle('Transform field comparison metrics')
fig2.legend(custom_lines, ['Resampled Data: Bicubic', 'Resampled Data: Bilinear',
                           'Resampled Data: No interp', 'Resampled Transform: Bicubic', 'Resampled Transform: Bilinear', 'Resampled Transform: No interp'], loc='lower center', ncol=2)
plt.tight_layout()
fig2.subplots_adjust(top=0.9, bottom=0.18)
fig2.savefig('plots/warp_field.pdf')


# for i, met in enumerate(['MSE', 'CC', 'MI']):
#     for j, interp in enumerate(['bicubic_bilinear', 'bicubic_no_interp', 'bilinear_no_interp']):
#         data = [warp.loc[res, interp][met] for res in resolutions]
#         axes[i].plot(resolutions,
#                      data,
#                      ':o',
#                      color=colors[j],
#                      label=interp)
#     mean_data = [warp.loc[res][met].mean() for res in resolutions]
#     axes[i].plot(resolutions, mean_data, '-ok', label='Mean')
#     axes[i].set_xlabel('Voxel size ($\mu$m)')
#     axes[i].legend()
#     axes[i].set_title(metrics[i])


# fig2.suptitle('Image warp field comparison metrics')
# plt.tight_layout()
# fig2.subplots_adjust(top=0.9)
# plt.show()
# fig2.savefig('plots/warp_field.pdf')
