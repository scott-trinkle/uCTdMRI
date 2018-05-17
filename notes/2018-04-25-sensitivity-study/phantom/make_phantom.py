import numpy as np
import matplotlib.pyplot as plt
from strtens.util import imsave, imread
from scipy.ndimage import gaussian_filter

vasc_mask = imread('vasculature_mask.tif')

np.random.seed(94)


def get_dims(orient, shape):
    # orient corresponds to axis of fibers
    if orient == 0:
        d1 = shape[1]
        d2 = shape[2]
    elif orient == 1:
        d1 = shape[0]
        d2 = shape[2]
    elif orient == 2:
        d1 = shape[0]
        d2 = shape[1]

    return d1, d2


def make_uniform_dir_phantom(orient, n_fibers, r_min, r_max,
                             mu_bg=86, sigma_bg=9,
                             mu_fib=100, sigma_fib=10,
                             mu_vasc=49, sigma_vasc=15,
                             vasc_mask=vasc_mask):
    '''
    Here, I make a phantom with straight fibers parallel to the y axis
    '''

    shape = vasc_mask.shape

    if type(orient) == int:
        orient = [orient]

    fib_mask = []
    for n in orient:
        d1, d2 = get_dims(n, shape)

        # choose random radii within range
        r_fibers = np.random.uniform(r_min, r_max, n_fibers)

        # choose the pixel centers in the non-orientation axis
        centers = np.vstack((np.random.randint(0, d1, n_fibers),
                             np.random.randint(0, d2, n_fibers))).T

        # Make fiber mask
        fib_mask.append(make_fib_mask_1d(n, r_fibers, centers, shape))

    fib_mask = sum(fib_mask)
    fib_mask[fib_mask > 0] = 1

    phant = make_bg_phantom(shape)

    # Add fibers
    phant[fib_mask == 1] = np.random.normal(
        mu_fib, sigma_fib, phant[fib_mask == 1].size).astype(np.uint8)

    return phant


def make_bg_phantom(shape,
                    mu_bg=86, sigma_bg=9,
                    mu_vasc=49, sigma_vasc=15,
                    vasc_mask=vasc_mask):

    # Background material
    phant = np.random.normal(mu_bg, sigma_bg, shape).astype(np.uint8)
    phant = gaussian_filter(phant, sigma=0.5)  # add some smoothing

    # Add vasculature
    phant[vasc_mask == 1] = np.random.normal(
        mu_vasc, sigma_vasc, phant[vasc_mask == 1].size)

    return phant


def make_fib_mask_1d(orient, r_fibers, centers, shape):
    d1, d2 = get_dims(orient, shape)

    fib_mask = np.zeros(shape, dtype=np.int)
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
    return fib_mask


n_fibers = 15
r_min = 1
r_max = 10


print('Making z phantom')
phant = make_uniform_dir_phantom(orient=0,
                                 n_fibers=n_fibers,
                                 r_min=r_min,
                                 r_max=r_max)
imsave('phants/z_phantom.tif', phant)

print('Making y phantom')
phant = make_uniform_dir_phantom(orient=r_min,
                                 n_fibers=n_fibers,
                                 r_min=r_min,
                                 r_max=r_max)
imsave('phants/y_phantom.tif', phant)

print('Making x phantom')
phant = make_uniform_dir_phantom(orient=2,
                                 n_fibers=n_fibers,
                                 r_min=r_min,
                                 r_max=r_max)
imsave('phants/x_phantom.tif', phant)

print('Making yz phantom')
phant = make_uniform_dir_phantom(orient=[0, 1],
                                 n_fibers=n_fibers,
                                 r_min=r_min,
                                 r_max=r_max)
imsave('phants/yz_phantom.tif', phant)

print('Making xz phantom')
phant = make_uniform_dir_phantom(orient=[0, 2],
                                 n_fibers=n_fibers,
                                 r_min=r_min,
                                 r_max=r_max)
imsave('phants/xz_phantom.tif', phant)

print('Making xy phantom')
phant = make_uniform_dir_phantom(orient=[1, 2],
                                 n_fibers=n_fibers,
                                 r_min=r_min,
                                 r_max=r_max)
imsave('phants/xy_phantom.tif', phant)

print('Making xyz phantom')
phant = make_uniform_dir_phantom(orient=[0, 1, 2],
                                 n_fibers=n_fibers,
                                 r_min=r_min,
                                 r_max=r_max)
imsave('phants/xyz_phantom.tif', phant)

print('Saving bg phantom')
phant = make_bg_phantom((100, 256, 256))
imsave('phants/bg_phantom.tif', phant)
