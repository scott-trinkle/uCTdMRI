import numpy as np
from tifffile import imread, imsave
import matplotlib.pyplot as plt
from glob import glob

# Setting ROI corners
xs = [2173, 3791, 3504, 4092, 5670, 6768, 6864, 8028, 8874, 5358]
ys = [2950, 1145, 2886, 4170, 2472, 2802, 1452, 1254, 3714, 2256]
d = 125

# Removing missing recon_8 slices
nums = list(range(6250, 6375))
nums.remove(6301)
nums.remove(6354)
nums.remove(6368)

# Recon_32_cropped filenames
fns32 = [
    'recon_cropped/recon_cropped_0{}.tiff'.format(i) for i in nums]

# Loading recon_32 volume
print('Loading recon_32 volume')
vol_32 = []
v32app = vol_32.append
count = 1
for fn in fns32:
    v32app(imread(fn))
    print(count)
    count += 1
vol_32 = np.array(vol_32)

# For each sample
for i, (x0, y0) in enumerate(zip(xs, ys)):
    print('Sample 32: ', i)
    samp = vol_32[:, y0:y0 + d, x0:x0 + d]
    imsave('samples_32/sample_32_{}.tif'.format(i), samp)

print('Loading recon_8 volume')

crop8path = '../../../Data/2017_07_22_WholeMouseMRI_5x_2k_phase35cm_gap31_exp30_newfocus/recon_flatcorr_1x/recon_crop_8/recon_0'
fns8 = [crop8path + '{}.tiff'.format(i) for i in nums]

vol_8 = []
v8app = vol_8.append
count = 1
for fn in fns8:
    v8app(imread(fn))
    print(count)
    count += 1
vol_8 = np.array(vol_8)

# For each sample
for i, (x0, y0) in enumerate(zip(xs, ys)):
    print('Sample 8: ', i)
    samp = vol_8[:, y0:y0 + d, x0:x0 + d]
    imsave('samples_8/sample_8_{}.tif'.format(i), samp)
