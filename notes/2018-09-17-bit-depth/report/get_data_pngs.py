import numpy as np
import tifffile as tf
import matplotlib.pyplot as plt
from glob import glob
from skimage import io

ids = [8, 32, 104, 12, 216, 198, 136, 28]
accs = [0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

fns8 = glob('../samples_8/*')
fns32 = glob('../samples_32/*')

num = 62

for fn in fns8:
    ID = fn.split('/')[-1].split('sample_8_')[-1].split('_')[0]
    print(ID)
    im = tf.imread(fn)
    io.imsave('figs/slices/{}_8.tif'.format(ID),
              np.flip(np.flip(im[..., num], axis=0), axis=1))

for fn in fns32:
    ID = fn.split('/')[-1].split('sample_32_')[-1].split('_')[0]
    print(ID)
    im = tf.imread(fn)
    io.imsave('figs/slices/{}_32.tif'.format(ID),
              np.flip(np.flip(im[..., num], axis=0), axis=1))
