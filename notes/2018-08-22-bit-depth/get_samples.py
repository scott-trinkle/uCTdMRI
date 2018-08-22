import numpy as np
from tifffile import imread, imsave
import matplotlib.pyplot as plt


path = '../../../Data/2018_06_08_WholeBrainBK_Redtube/recon_flatcorr_1x/recon/recon_0'
slice_nums = range(5114, 5114 + 125)

samp1 = []
x1 = 8286
y1 = 4962

samp2 = []
x2 = 7662
y2 = 6738

samp3 = []
x3 = 2782
y3 = 4946


for i in slice_nums:
    print(i)
    im = imread(path + '{}.tiff'.format(i))
    samp1.append(im[y1:y1 + 125, x1:x1 + 125])
    samp2.append(im[y2:y2 + 125, x2:x2 + 125])
    samp3.append(im[y3:y3 + 125, x3:x3 + 125])

imsave('samples/sample1.tif', np.array(samp1))
imsave('samples/sample2.tif', np.array(samp2))
imsave('samples/sample3.tif', np.array(samp3))
