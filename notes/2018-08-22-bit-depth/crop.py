import numpy as np
from glob import glob
from tifffile import imread, imsave

fns = glob('../../../Data/2017_07_22_WholeMouseMRI_5x_2k_phase35cm_gap31_exp30_newfocus/recon_flatcorr_1x/recon/*')

x0, y0 = 1104, 2064
dx, dy = 10096, 6720

for fn in fns:
    outfn = 'recon_cropped/recon_cropped_' + \
        fn.split('/')[-1].split('_')[1].split('.tiff')[0] + '.tiff'
    print(outfn)
    im = imread(fn)
    imsave(outfn, im[y0:y0 + dy, x0:x0 + dx])
