import numpy as np
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt

aff_fns = glob('data/affine_*.csv')
list_ = []
for fn in aff_fns:
    list_.append(pd.read_csv(fn, index_col=[0, 1]))
aff = pd.concat(list_)

resolutions = aff.index.levels[0]
# metrics = ['MSE (affine)', 'Correlation (affine)',
#            'MSE (translation)', 'Correlation (translation)']
metrics = ['MSE', 'Correlation']

# fig1, axes = plt.subplots(2, 2, figsize=(12, 12))
fig1, axes = plt.subplots(1, 2, figsize=(12, 6))
axes = axes.flatten()
colors = ['C0', 'C1', 'C2']
for i, met in enumerate(['MSE_t', 'CC_t']):  # , 'MSE_f', 'CC_f']):
    for j, interp in enumerate(['bicubic_bilinear', 'bicubic_no_interp', 'bilinear_no_interp']):
        data = [aff.loc[res, interp][met] for res in resolutions]
        if j == 0:
            lab = 'Bicubic / Bilinear'
        elif j == 1:
            lab = 'Bicubic / No interp'
        elif j == 2:
            lab = 'Bilinear / No interp'

        axes[i].plot(resolutions,
                     data,
                     ':o',
                     color=colors[j],
                     label=lab)
    # mean_data = [aff.loc[res][met].mean() for res in resolutions]
    # axes[i].plot(resolutions, mean_data, '-ok', label='Mean')
    axes[i].set_xlabel('Voxel size ($\mu$m)')
    axes[i].set_title(metrics[i])
    # axes[i].legend()

handles, labels = axes[0].get_legend_handles_labels()
fig1.legend(handles, labels, loc='lower center', ncol=3)
fig1.suptitle('Comparison of linear transforms')
plt.tight_layout()
fig1.subplots_adjust(top=0.9, bottom=0.15)
fig1.savefig('plots/affine.pdf')
