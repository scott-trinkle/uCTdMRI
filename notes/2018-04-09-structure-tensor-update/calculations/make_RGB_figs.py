import numpy as np
from strtens.util import imread, imsave
from strtens import StructureTensor
from time import time

print('Reading image')
im = imread('../../../data/xray/recon_2x_stack-1.tif')

print('Structure tensor analysis')
d = 2
n = 7
a = time()
AI, vectors = StructureTensor(im,
                              d_sigma=d,
                              n_sigma=n).results()
b = time()
print('{} seconds elapsed'.format(np.round(b - a, 3)))

# To make x = red, y = green, z = blue
vectors = np.flip(vectors, axis=-1)

print('Saving')
slnum = 84

# Raw data
imsave(fn='../figs/xray_sl{}.png'.format(slnum),
       im=im[slnum],
       dtype=im.dtype)

# Raw RGB/Orientation image
imsave(fn='../figs/RGB_raw_d{}_n{}_sl{}.png'.format(d, n, slnum),
       im=vectors[slnum],
       rgb=True)

# RGB/Orientation image scaled by AI
imsave(fn='../figs/RGB_scaled_d{}_n{}_sl{}.png'.format(d, n, slnum),
       im=vectors[slnum],
       rgb=True,
       scalar=AI[slnum],
       maxperc=99)  # d2n7 yields low AI w/ Westin, this gives better display
