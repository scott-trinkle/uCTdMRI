import numpy as np
from strtens.util import imread, imsave, k_means

im = imread('./sample_8_0.tif')
labels = k_means(im, sig=1)
mask = np.zeros_like(labels)
mask[labels == 2] = 1
imsave('vasculature_mask.tif', mask)
