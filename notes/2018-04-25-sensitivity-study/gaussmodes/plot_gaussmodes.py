import numpy as np
from strtens.util import imread, imsave, compute_derivatives

im = imread('../../../data/xray/recon_2x_stack-1.tif')

for mode in ['constant', 'nearest', 'reflect', 'wrap', 'mirror']:
    dz, dy, dx = compute_derivatives(im, d_sigma=5, mode=mode)
    imsave('{}_dx.tif'.format(mode), dx, dtype=np.float32)
    imsave('{}_dy.tif'.format(mode), dy, dtype=np.float32)
    imsave('{}_dz.tif'.format(mode), dz, dtype=np.float32)
