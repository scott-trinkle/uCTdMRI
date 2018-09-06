from sensitivity_funcs import crossing_sensitivity
import numpy as np

sds = np.arange(1, 21) / 1.2
sns = np.arange(1, 21) / 1.2

imfn = "../phantoms/crossing_fibers/phants/z_phantom_nfib9x4_r8_75deg.tif"
maskfn = "../phantoms/crossing_fibers/masks/z_phantom_mask_nfib9x4_r8_75deg.tif"
resultspath = "../phantoms/crossing_fibers/results/deg75"

peak_data=crossing_sensitivity(imfn, maskfn, resultspath, sds, sns)