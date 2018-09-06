from sensitivity_funcs import sensitivity
import numpy as np

sds = np.arange(1, 21) / 1.2
sns = np.arange(1, 21) / 1.2

imfn = "../phantoms/different_size/phants/x_phantom_nfib9_r12.tif"
maskfn = "../phantoms/different_size/masks/x_phantom_nfib9_r12.tif"
resultspath = "../phantoms/different_size/results/r12"
peak_data=sensitivity(imfn, maskfn, resultspath, sds, sns)