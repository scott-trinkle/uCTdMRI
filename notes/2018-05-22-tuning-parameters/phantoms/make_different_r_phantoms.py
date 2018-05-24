import numpy as np
from strtens.util import imsave
from phantom_funcs import make_orth_phantom

n_fibers = 9
for r in [4, 8, 12, 16]:
    print('r = ', r)
    phant, mask = make_orth_phantom(orient=0,
                                    n_fibers=n_fibers,
                                    r=r)
    imsave('different_size/masks/z_phantom_nfib9_r{}.tif'.format(r),
           mask, dtype=np.float32)
    imsave('different_size/phants/z_phantom_nfib9_r{}.tif'.format(r),
           phant)
