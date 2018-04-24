import numpy as np
from strtens.util import imread, imsave
from strtens import StructureTensor


print('Reading image')
im = imread('../../../data/xray/recon_2x_stack-1.tif')

print('Structure tensor analysis')
for d in [1, 2, 3]:
    for n in [1, 2, 3, 5]:
        print('n = {}'.format(n))
        AI, vectors = StructureTensor(im,
                                      d_sigma=d,
                                      n_sigma=n).results()

        # To make x = red, y = green, z = blue
        vectors = np.flip(vectors, axis=-1)

        print('Saving\n')
        imsave(fn='choose_sigmas/RGB_d{}_n{}.tif'.format(d, n),
               im=vectors,
               rgb=True,
               scalar=AI)
