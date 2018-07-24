import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from strtens.util import imread

print('Reading images')
im = imread('../../data/xray/recon_2x_stack-1.tif')
mask = imread('../../data/xray/recon1mask.tif')
inv_mask = np.zeros_like(mask)
inv_mask[mask == 0] = 1


print('ROC')
fpr, tpr, thresholds = metrics.roc_curve(mask.flatten(), im.flatten())
auc = metrics.roc_auc_score(mask.flatten(), im.flatten())

dec = np.where(np.isnan(tpr / fpr), 0, tpr / fpr)
dec[dec > 18] = 15.10346129
ind = np.where(dec == dec[thresholds < 125].max())[0]
tpr_thresh = 0.95
thresh = thresholds[tpr > tpr_thresh][0]
ind = np.where(thresholds == thresh)[0]


fig, axes = plt.subplots(2, 2, figsize=(12, 10))

axes[0, 0].hist(im[mask == 0], bins=256, label='Background')
axes[0, 0].hist(im[mask == 1], bins=256, label='Fibers')
y0, y1 = axes[0, 0].get_ylim()
axes[0, 0].plot([thresh, thresh], [y0, y1], 'k:',
                label='(TPR, FPR)= ({},{})'.format(tpr[ind][0].round(2),
                                                   fpr[ind][0].round(2)))
axes[0, 0].set_xlabel('Gray value')
axes[0, 0].legend()
axes[0, 0].set_title('Distributions')
axes[0, 0].axis([0, 255, y0, y1])

axes[0, 1].plot(fpr, tpr)
axes[0, 1].plot([fpr[ind], fpr[ind]], [0, 1], 'k:',
                label='TPR = {}'.format(tpr[ind].round(2)))
axes[0, 1].set_xlabel('FPR')
axes[0, 1].set_ylabel('TPR')
axes[0, 1].set_aspect('equal')
axes[0, 1].axis([0, 1, 0, 1])
axes[0, 1].set_title('ROC Curve: AUC = {}'.format(np.round(auc, 2)))

axes[1, 0].plot(thresholds, dec)
y0, y1 = axes[1, 0].get_ylim()
axes[1, 0].plot([thresh, thresh], [y0, y1], 'k:',
                label='TPR = {}'.format(tpr[ind].round(2)))
axes[1, 0].set_title('TPR / FPR ratio')
axes[1, 0].set_xlabel('Gray value')
axes[1, 0].set_ylabel('TPR/FPR')
axes[1, 0].axis([0, 255, y0, y1])


axes[1, 1].plot(thresholds, tpr, label='TPR')
axes[1, 1].plot(thresholds, fpr, label='FPR')
axes[1, 1].plot([thresh, thresh], [0, 1], 'k:')
axes[1, 1].set_xlabel('Gray value')
axes[1, 1].set_title('TPR and FPR vs threshold')
axes[1, 1].legend()
axes[1, 1].axis([0, 255, 0, 1])


fig.suptitle('Optimal Gray Value Thresh = {}'.format(np.round(thresh, 3)))
plt.tight_layout()
fig.subplots_adjust(top=0.90)

plt.savefig('gray_level_threshold.pdf')
