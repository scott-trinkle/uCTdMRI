import numpy as np
from phantom_funcs import make_bg_phantom, make_orth_phantom
from strtens.util import imread, imsave


def make_crossing_phantom(deg, mu_fib=100):
    # These phantoms were taken by rotating the mask from a
    # make_orth_phantom(0, 16, 8) call in Fiji.
    fn = 'crossing_fibers/fiji_masks/z_phantom_mask_nfib9x4_r8_{}deg.tif'.format(
        deg)
    fib_mask = imread(fn)[:122]
    fib_mask[:, 0:35, :] = 0
    fib_mask[:, 90:, :] = 0

    _, base_mask = make_orth_phantom(0, 4, 8, pad=3)

    fib_mask += 2 * base_mask

    phant = make_bg_phantom()

    phant[fib_mask > 0] = np.random.poisson(
        100, phant[fib_mask > 0].size).astype(np.uint8)

    return phant, fib_mask


for deg in range(15, 86, 10):
    print(deg)
    phant, mask = make_crossing_phantom(deg)
    imsave('crossing_fibers/phants/z_phantom_nfib9x4_r8_{}deg.tif'.format(deg),
           phant)
    imsave('crossing_fibers/masks/z_phantom_mask_nfib9x4_r8_{}deg.tif'.format(deg),
           mask, dtype=np.float32)
