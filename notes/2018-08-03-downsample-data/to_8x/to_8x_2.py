import os
from tifffile import imread, imsave
from scipy.misc import imresize

outdir = '../../../../Data/2018_06_08_WholeBrainBK_Redtube/recon_flatcorr_1x/recon_8x/'
if not os.path.isdir(outdir):
    os.mkdir(outdir)

start = 1851
stop = 3701

factor = 8

fns = ['../../../../Data/2018_06_08_WholeBrainBK_Redtube/recon_flatcorr_1x/recon_8bit/recon_8bit_{:0>5d}.tiff'.format(
    i) for i in range(start, stop + 1)]

for fn in fns:
    print(fn.split('/')[-1])
    im = imread(fn)
    im = imresize(im, size=1/factor, interp='bilinear')
    outfn = outdir + 'recon_8x_' + fn.split('/')[-1].split('_')[1]
    imsave(outfn, im)
