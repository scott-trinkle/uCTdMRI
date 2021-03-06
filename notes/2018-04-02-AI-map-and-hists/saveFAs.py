import numpy as np
from skimage import io
from strtens import StructureTensor
from tifffile import imsave

print('Reading\n')
im = io.imread('../data/recon_2x_stack-1.tif')

print('Running STA\n')
sl = 35
dsigs = [0.5, 1, 2, 3, 4, 5, 10, 20]
nsigs = [0.5, 1, 2, 3, 4, 5, 10, 20]

for dsig in dsigs:
    for nsig in nsigs:
        print('dsig: {}\nnsig: {}'.format(dsig, nsig))
        FA, vects = StructureTensor(im,
                                    d_sigma=dsig,
                                    n_sigma=nsig).results()

        print('Saving...\n')
        imsave('FAs/d{}_n{}.tif'.format(dsig, nsig), im[sl])

print('Done!')
