import numpy as np
from strtens.util import imread, imsave, compute_derivatives
from skimage import img_as_float

im = imread('../../../data/xray/recon_2x_stack-1.tif')
im = img_as_float(im)

sigmas = np.arange(1, 11) / 1.2

for sig in sigmas:
    print(np.round(sig, 2))
    dz, dy, dx = compute_derivatives(im, d_sigma=sig)
    imsave('{}_dx.tif'.format(np.round(sig, 2)), dx, dtype=np.float32)
    imsave('{}_dy.tif'.format(np.round(sig, 2)), dy, dtype=np.float32)
    imsave('{}_dz.tif'.format(np.round(sig, 2)), dz, dtype=np.float32)
