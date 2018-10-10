import numpy as np
from tifffile import imread, imsave
import matplotlib.pyplot as plt
from glob import glob

# Values from ImageJ selectio box
width = 5496
height = 3378
x0 = 1890
y0 = 1488

# Setting ROI corners
nrows = 15
xs = np.linspace(x0, x0 + width, nrows, dtype=np.int)
ys = np.linspace(y0, y0 + height, nrows, dtype=np.int)
d = 125

# Slice numbers
nums = np.arange(10250, 10375)

# Recon_32_cropped filenames
fns32 = ['recon_cropped/recon_cropped_{}.tiff'.format(i) for i in nums]

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
i = 1
for x_i in xs:
    for y_i in ys:
        print('Sample 32: {}/{}'.format(i, nrows**2))
        samp = vol_32[:, y_i:y_i + d, x_i:x_i + d]
        imsave('samples_32/sample_32_{}_x{}_y{}.tif'.format(i, x_i, y_i), samp)
        i += 1

print('Loading recon_8 volume')
crop8path = '../../../Data/2018_04_03_WholeBrainMRI1_retake_newfocus/recon_flatcorr_1x/recon_crop8_new/recon_'
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
i = 1
for x_i in xs:
    for y_i in ys:
        print('Sample 8: {}/{}'.format(i, nrows**2))
        samp = vol_8[:, y_i:y_i + d, x_i:x_i + d]
        imsave('samples_8/sample_8_{}_x{}_y{}.tif'.format(i, x_i, y_i), samp)
        i += 1
