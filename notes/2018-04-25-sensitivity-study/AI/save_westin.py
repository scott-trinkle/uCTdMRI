import numpy as np
from strtens.util import imread, imsave
from write_csv import write_csv


print('Reading image')
im = imread('../../../data/xray/recon_2x_stack-1.tif')
mask = imread('../../../data/xray/recon1mask.tif')

print('Creating sigmas')
# 1.2 um / vox, so this converts um to voxels
sds = np.arange(0, 10.5, 0.5) / 1.2
sns = np.arange(0, 10.5, 0.5) / 1.2

print('Writing CSVs and images')
write_csv('AIs_westin.csv', sds=sds, sns=sns,
          im=im, mask=mask, metric='westin', saveim=True,
          rgb=False, impath='../tifs/westin/')
