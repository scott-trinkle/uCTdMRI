import numpy as np
from strtens.util import imsave
from phantom_funcs import make_orth_phantom

# MAKE GENERIC ORIENTATION PHANTOMS FOR EACH ORIENTATION
n_fibers = 16
r = 8
labels = ['z', 'y', 'x']
for i, orient in enumerate([0, 1, 2]):
    print(i)
    phant, mask = make_orth_phantom(orient=orient,
                                    n_fibers=n_fibers,
                                    r=r)
    imsave('generic_xyz/masks/{}_phantom_mask_nfib16_r{}.tif'.format(
        labels[i], r), mask, dtype=np.float32)
    imsave('generic_xyz/phants/{}_phantom_nfib16_r{}.tif'.format(
        labels[i], r), phant)
