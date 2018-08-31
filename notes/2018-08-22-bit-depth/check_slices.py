import matplotlib.pyplot as plt
import numpy as np
from glob import glob

fns = glob('../../../Data/2017_07_22_WholeMouseMRI_5x_2k_phase35cm_gap31_exp30_newfocus/recon_flatcorr_1x/recon_crop_8/*')
nums = np.sort([int(fn.split('.tiff')[0].split('_')[-1]) for fn in fns])

diff = np.setdiff1d(range(0, 13782), nums)

fig = plt.figure(figsize=(20, 6))
plt.plot(diff[:100], np.diff(diff)[:100], 'k.:')
plt.xlabel('Slice number')
plt.ylabel('Distance to next missing slice')
plt.title('Missing slices')
plt.tight_layout()
plt.show()
