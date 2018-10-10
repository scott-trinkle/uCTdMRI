import numpy as np
from tifffile import imread, imsave

fns = ['../../../Data/2018_04_03_WholeBrainMRI1_retake_newfocus/recon_flatcorr_1x/recon/recon_{}.tiff'.format(
    i) for i in range(10250, 10375)]


x0, y0 = 4919 - 4907, 2554 - 922
dx, dy = 9156, 5958

for fn in fns:
    outfn = 'recon_cropped/recon_cropped_' + \
        fn.split('/')[-1].split('_')[1].split('.tiff')[0] + '.tiff'
    print(outfn)
    im = imread(fn)
    imsave(outfn, im[y0:y0 + dy, x0:x0 + dx])
