import os
import numpy as np
import tifffile as tf
from strtens.util import rescale

outdir = 'recon_8bit/'
if not os.path.isdir(outdir):
    os.mkdir(outdir)

start = 4472
stop = 4474

fns = ['recon_44/recon_{:0>5d}.tiff'.format(i) for i in range(start, stop+1)]

for fn in fns:
    print(fn)
    im = tf.imread(fn)
    im = rescale(im, scale=256, dtype=np.uint8)

    outfn = outdir + 'recon_8bit_' + fn.split('/')[1].split('_')[1]
    tf.imsave(outfn, im)
