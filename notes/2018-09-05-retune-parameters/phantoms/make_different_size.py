import numpy as np
from strtens.util import imsave
from phantom_funcs import make_bg_phantom, make_orth_phantom

for r in [4, 8, 12, 16]:
    phant, mask = make_orth_phantom(2, 9, r)
    imsave('./different_size/phants/x_phantom_nfib9_r{}.tif'.format(r), phant)
    imsave('./different_size/masks/x_phantom_nfib9_r{}.tif'.format(r), mask)
