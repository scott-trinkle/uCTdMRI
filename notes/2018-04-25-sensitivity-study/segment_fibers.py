import numpy as np
from strtens.util import imread, imsave
from sklearn import cluster
from scipy.ndimage import gaussian_filter, binary_dilation
import matplotlib.pyplot as plt


def get_mask(im, sig=2.7):
    im = gaussian_filter(im, sig)
    kmeans = cluster.MiniBatchKMeans(n_clusters=3,
                                     n_init=3,
                                     batch_size=100,
                                     random_state=48).fit(im.reshape((-1, 1)))

    labels = kmeans.labels_.reshape(im.shape)
    mask = np.zeros_like(labels)
    mask[labels == 1] = 1
    mask = binary_dilation(mask, iterations=1).astype(mask.dtype)
    return mask


print('Reading images')
im1 = imread('../../data/xray/recon_2x_stack-1.tif')
im2 = imread('../../data/xray/recon_2x_stack-2.tif')

print('Calculating')
mask1 = get_mask(im1)
mask2 = get_mask(im2)

print('Saving')
imsave('recon1mask.tif', mask1)
imsave('recon2mask.tif', mask2)
