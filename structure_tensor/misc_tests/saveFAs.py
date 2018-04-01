import numpy as np
from skimage import io
import sys
sys.path.append('..')
import st_tools as st
import tifffile as tf

print('Reading')
im = io.imread('../../data/recon_2x_stack-1.tif')

print('Running STA')
sl = 35
dsigs = [0.5, 1, 2, 3, 4, 5, 10, 20]
nsigs = [0.5, 1, 2, 3, 4, 5, 10, 20]

for dsig, nsig in zip(dsigs, nsigs):
    FA, vects = st.st_3D(im,
                         d_sigma=dsig,
                         n_sigma=nsig,
                         westin=True)
    tf.imsave('FAs/d{}_n{}.tif'.format(dsig, nsig), im[sl])
