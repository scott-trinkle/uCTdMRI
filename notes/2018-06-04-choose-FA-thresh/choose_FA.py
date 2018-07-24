import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from strtens.util import imread
from strtens import StructureTensor

print('Reading images')
im = imread(
    '../2018-05-22-tuning-parameters/phantoms/crossing_fibers/phants/z_phantom_nfib9x4_r8_45deg.tif')
mask = imread(
    '../2018-05-22-tuning-parameters/phantoms/crossing_fibers/masks/z_phantom_mask_nfib9x4_r8_45deg.tif')
mask[mask > 0] = 1

print('ST')
ST = StructureTensor(im)

print('Getting FA')
FA = ST.get_anisotropy_index('fa')

print('ROC')
fpr, tpr, thresholds = metrics.roc_curve(mask.flatten(), FA.flatten())

dec = np.where(np.isnan(tpr / fpr), 0, tpr / fpr)
ind = dec == dec.max()
thresh = thresholds[dec == dec.max()]

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

axes[0, 0].hist(FA[mask == 0], bins=100, label='Background')
axes[0, 0].hist(FA[mask == 1], bins=100, label='Fibers')
y0, y1 = axes[0, 0].get_ylim()
axes[0, 0].plot([thresh, thresh], [y0, y1], 'k:',
                label='(TPR, FPR)= ({},{})'.format(tpr[ind][0].round(2), fpr[ind][0].round(2)))
axes[0, 0].set_xlabel('FA')
axes[0, 0].legend()
axes[0, 0].set_title('Distributions')
axes[0, 0].axis([0, 1, y0, y1])

axes[0, 1].plot(fpr, tpr)
axes[0, 1].plot([fpr[ind], fpr[ind]], [0, 1], 'k:',
                label='TPR = {}'.format(tpr[ind].round(2)))
axes[0, 1].set_xlabel('FPR')
axes[0, 1].set_ylabel('TPR')
axes[0, 1].set_aspect('equal')
axes[0, 1].axis([0, 1, 0, 1])
axes[0, 1].set_title('ROC Curve')

axes[1, 0].plot(thresholds, tpr, label='TPR')
axes[1, 0].plot(thresholds, fpr, label='FPR')
axes[1, 0].plot([thresh, thresh], [0, 1], 'k:')
axes[1, 0].set_xlabel('FA Threshold')
axes[1, 0].set_title('TPR and FPR vs threshold')
axes[1, 0].legend()
axes[1, 0].set_xlim([0, 1.])
axes[1, 0].axis([0, 1, 0, 1])

axes[1, 1].plot(thresholds, dec)
y0, y1 = axes[1, 1].get_ylim()
axes[1, 1].plot([thresh, thresh], [y0, y1], 'k:',
                label='TPR = {}'.format(tpr[ind].round(2)))
axes[1, 1].set_title('TPR / FPR ratio')
axes[1, 1].set_xlabel('FA')
axes[1, 1].set_ylabel('TPR/FPR')
axes[1, 1].axis([0, 1, 0, 1.2])

fig.suptitle('Optimal Thresh: FA = {}'.format(thresh[0].round(3)))
plt.tight_layout()
fig.subplots_adjust(top=0.90)

plt.show()
