from sensitivity_funcs import sensitivity, crossing_sensitivity, get_odfs
import numpy as np

sds = np.arange(1, 10.5, 0.5) / 1.2
sns = np.arange(2, 12.5, 0.5) / 1.2

deg = 45

imfn = '../phantoms/crossing_fibers/phants/z_phantom_nfib9x4_r8_{}deg.tif'.format(
    deg)
maskfn = '../phantoms/crossing_fibers/masks/z_phantom_mask_nfib9x4_r8_{}deg.tif'.format(
    deg)

resultspath = '../phantoms/crossing_fibers/results/deg{}'.format(deg)

peak_data = crossing_sensitivity(imfn, maskfn, resultspath, sds, sns)
get_odfs(imfn, resultspath, sds, sns)
