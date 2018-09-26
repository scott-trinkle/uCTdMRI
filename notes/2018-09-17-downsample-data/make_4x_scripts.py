import numpy as np
import matplotlib.pyplot as plt
import tifffile as tf
from scipy.ndimage import zoom
from glob import glob
from time import perf_counter

fns = glob('../../../Data/2018_04_03_WholeBrainMRI1_retake_newfocus/recon_flatcorr_1x/recon_crop8_new/*.tiff')
batch_size = len(fns) // 6


for i in range(6):
    fn = 'to_4x/to_4x_{}_{}-{}.py'.format(i + 1, i * batch_size,
                                          (i + 1) * batch_size if i != 5 else len(fns))
    with open(fn, 'w') as f:
        f.write('''
import numpy as np
import tifffile as tf
from scipy.ndimage import zoom
from glob import glob

fns = sorted(glob(
    '../../../../Data/2018_04_03_WholeBrainMRI1_retake_newfocus/recon_flatcorr_1x/recon_crop8_new/recon_*.tiff'))
num_slices = (len(fns))
gen_batch_size = int(num_slices // 6)

i = {}  # replace with format
batch = slice(i * gen_batch_size, (i + 1) *
              gen_batch_size if i != 5 else num_slices)

outdir = '/'.join(fns[0].split('/')[:-2]) + '/recon_4x/'

for j, fn in enumerate(fns[batch]):
    im = tf.imread(fn)
    zoomed = zoom(im, 1 / 4, order=1)
    outfn = outdir + 'recon_4x_' + fn.split('/')[-1].split('_')[-1]
    tf.imsave(outfn, zoomed)
'''.format(i))

    shfn = 'to_4x/to_4x_{}_{}-{}.sh'.format(i + 1, i * batch_size,
                                            (i + 1) * batch_size if i != 5 else len(fns))
    nodes = ['bignode3', 'bignode4', 'bigmem1',
             'bigmem2', 'bigmem3', 'bigmem4']
    with open(shfn, 'w') as f:
        f.write('#!/bin/sh\n')
        f.write('#$ -j y\n')
        f.write('#$ -cwd\n')
        f.write('#$ -V\n')
        f.write('#$ -l h={}\n\n'.format(nodes[i]))

        f.write('python to_4x_{}_{}-{}.py\n'.format(i + 1, i * batch_size,
                                                    (i + 1) * batch_size if i != 5 else len(fns)))
