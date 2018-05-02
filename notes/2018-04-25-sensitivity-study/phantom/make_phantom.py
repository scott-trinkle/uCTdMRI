'''
DO SOME BLURRING OF THE BACKGROUND AND VESSELS
'''

import numpy as np
import matplotlib.pyplot as plt
from strtens.util import imsave, imread
np.random.seed(94)


def make_uniform_dir_phantom(orient, n_fibers, r_min, r_max, size,
                             mu_bg=86, sigma_bg=6, mu_fib=99.92,
                             sigma_fib=11.73):
    '''
    Here, I make a phantom with straight fibers parallel to the y axis
    '''

    if orient == 0:
        d1 = size[1]
        d2 = size[2]
    elif orient == 1:
        d1 = size[0]
        d2 = size[2]
    elif orient == 2:
        d1 = size[0]
        d2 = size[1]

    r_fibers = np.random.uniform(r_min, r_max, n_fibers)
    centers = [(d10, d20) for d10, d20 in zip(
        np.random.randint(r_max / 2, d1-r_max / 2, n_fibers),
        np.random.randint(r_max / 2, d2-r_max / 2, n_fibers))]

    fib_mask = np.zeros(size, dtype=np.int)
    for d1ind in range(d1):
        for d2ind in range(d2):
            for fibind, r_fib in enumerate(r_fibers):
                d10 = centers[fibind][0]
                d20 = centers[fibind][1]
                if (d2ind > d20 - np.sqrt(r_fib**2 - (d1ind - d10)**2)) and (d2ind < d20 + np.sqrt(r_fib**2 - (d1ind - d10)**2)):
                    if orient == 0:
                        fib_mask[:, d1ind, d2ind] = 1
                    elif orient == 1:
                        fib_mask[d1ind, :, d2ind] = 1
                    elif orient == 2:
                        fib_mask[d1ind, d2ind, :] = 1

    phant = np.random.normal(mu_bg, sigma_bg, size).astype(np.uint8)
    phant[fib_mask == 1] = np.random.normal(mu_fib, sigma_fib,
                                            phant[fib_mask == 1].size).astype(np.uint8)

    return phant


print('making phantom')
phant = make_uniform_dir_phantom(orient=0,
                                 n_fibers=20,
                                 r_min=10 / 2,
                                 r_max=30 / 2,
                                 size=(100, 256, 256))

im = imread('../../../data/xray/recon_2x_stack-1.tif')
vasc = imread('./Clusters.tif')
phant[vasc == 1] = 50
imsave('z_phantom.tif', phant)


# from strtens.vis import plot_ODF
# from strtens import StructureTensor

# print('calculating st')
# ai, vects = StructureTensor(phant, d_sigma=2.5, n_sigma=4.17).results('fa')
# print('plotting odf')
# plot_ODF(vects)
