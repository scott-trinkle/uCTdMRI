
import numpy as np
import tifffile as tf
from scipy.ndimage import zoom
from glob import glob

fns = sorted(glob(
    '../../../../Data/2018_04_03_WholeBrainMRI1_retake_newfocus/recon_flatcorr_1x/recon_crop8_new/recon_*.tiff'))
num_slices = (len(fns))
gen_batch_size = int(num_slices // 6)

i = 0  # replace with format
batch = slice(i * gen_batch_size, (i + 1) *
              gen_batch_size if i != 5 else num_slices)

outdir = '/'.join(fns[0].split('/')[:-2]) + '/recon_4x/'

for j, fn in enumerate(fns[batch]):
    im = tf.imread(fn)
    zoomed = zoom(im, 1 / 4, order=1)
    outfn = outdir + 'recon_4x_' + fn.split('/')[-1].split('_')[-1]
    tf.imsave(outfn, zoomed)
