# Sample warp fields AND apply transform

import numpy as np
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt

warp_fns = glob('data/warp_*.csv')
list_ = []
for fn in warp_fns:
    list_.append(pd.read_csv(fn, index_col=[1]))
df = pd.concat(list_)
warp = df.loc['warp'].set_index(['Resolution', 'Interp-pair'])
warped = df.loc['warped'].set_index(['Resolution', 'Interp-pair'])

resolutions = warp.index.levels[0]
metrics = ['MSE', 'Correlation', 'Mutual Information']

fig1, axes = plt.subplots(1, 3, figsize=(15, 8))
axes = axes.flatten()
colors = ['C0', 'C1', 'C2']
for i, met in enumerate(['MSE', 'CC', 'MI']):
    for j, interp in enumerate(['bicubic', 'bilinear', 'no_interp']):
        data = [warped.loc[res, interp][met] for res in resolutions]
        axes[i].plot(resolutions,
                     data,
                     ':o',
                     color=colors[j],
                     label=interp)
    mean_data = [warped.loc[res][met].mean() for res in resolutions]
    axes[i].plot(resolutions, mean_data, '-ok', label='Mean')
    axes[i].set_xlabel('Voxel size ($\mu$m)')
    axes[i].legend()
    axes[i].set_title(metrics[i])


fig1.suptitle('Warped image comparison metrics')
plt.tight_layout()
fig1.subplots_adjust(top=0.9)
fig1.savefig('plots/warped_image.pdf')

fig2, axes = plt.subplots(1, 3, figsize=(15, 8))
axes = axes.flatten()
colors = ['C0', 'C1', 'C2']
for i, met in enumerate(['MSE', 'CC', 'MI']):
    for j, interp in enumerate(['bicubic_bilinear', 'bicubic_no_interp', 'bilinear_no_interp']):
        data = [warp.loc[res, interp][met] for res in resolutions]
        axes[i].plot(resolutions,
                     data,
                     ':o',
                     color=colors[j],
                     label=interp)
    mean_data = [warp.loc[res][met].mean() for res in resolutions]
    axes[i].plot(resolutions, mean_data, '-ok', label='Mean')
    axes[i].set_xlabel('Voxel size ($\mu$m)')
    axes[i].legend()
    axes[i].set_title(metrics[i])


fig2.suptitle('Image warp field comparison metrics')
plt.tight_layout()
fig2.subplots_adjust(top=0.9)
plt.show()
fig2.savefig('plots/warp_field.pdf')
