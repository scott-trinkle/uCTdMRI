from sensitivity_funcs import sensitivity, get_odfs
import numpy as np

sds = np.arange(1, 10.5, 0.5) / 1.2
sns = np.arange(2, 12.5, 0.5) / 1.2

r = 8

imfn = '../phantoms/different_size/phants/x_phantom_nfib9_r{}.tif'.format(r)
maskfn = '../phantoms/different_size/masks/x_phantom_mask_nfib9_r{}.tif'.format(
    r)
resultspath = '../phantoms/different_size/results/r{}'.format(r)

# peak_data = sensitivity(imfn, maskfn, resultspath, sds, sns)
get_odfs(imfn, resultspath, sds, sns)
