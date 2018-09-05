import numpy as np
from strtens.util import imsave, imread
from scipy.ndimage import gaussian_filter

vasc_mask = imread('./vasculature_mask/vasculature_mask.tif')
np.warnings.filterwarnings('ignore')


def get_dims(orient):
    # orient corresponds to axis of fibers
    shape = (122, 125, 125)
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


def make_orth_phantom(orient, n_fibers, r, pad=1.5,
                      mu_fib=100):
    '''
    Here, I make a phantom with straight fibers parallel to a given axis
    or set of axes.
    '''

    shape = (122, 125, 125)

    if type(orient) == int:
        orient = [orient]

    fib_mask = []
    for n in orient:
        d1, d2 = get_dims(n)

        # choose the pixel centers in the non-orientation axis
        c1, c2 = np.meshgrid(np.linspace(0 + pad * r, d1 - pad * r, int(n_fibers**0.5)),
                             np.linspace(0 + pad * r, d2 - pad * r, int(n_fibers**0.5)))
        centers = np.vstack((c1.flatten(), c2.flatten())).T

        # Make fiber mask
        fib_mask.append(make_fib_mask(n, r, n_fibers, centers, shape))

    fib_mask = sum(fib_mask)
    fib_mask[fib_mask > 0] = 1  # in case mask ever overlaps and sums > 1

    phant = make_bg_phantom()

    # Add fibers
    phant[fib_mask == 1] = np.random.poisson(
        100, phant[fib_mask == 1].size).astype(np.uint8)

    return phant, fib_mask


def make_fib_mask(orient, r, n_fibers, centers, shape):
    d1, d2 = get_dims(orient)

    fib_mask = np.zeros(shape, dtype=np.int)
    for d1ind in range(d1):
        for d2ind in range(d2):
            for fibind in range(n_fibers):
                d10 = centers[fibind][0]
                d20 = centers[fibind][1]
                if (d2ind > d20 - np.sqrt(r**2 - (d1ind - d10)**2)) and (d2ind < d20 + np.sqrt(r**2 - (d1ind - d10)**2)):
                    if orient == 0:
                        fib_mask[:, d1ind, d2ind] = 1
                    elif orient == 1:
                        fib_mask[d1ind, :, d2ind] = 1
                    elif orient == 2:
                        fib_mask[d1ind, d2ind, :] = 1
    return fib_mask


def make_bg_phantom(mu_bg=86, mu_vasc=49,
                    vasc_mask=vasc_mask):

    shape = (122, 125, 125)

    # Background material
    phant = np.random.poisson(mu_bg, shape).astype(np.uint8)
    phant = gaussian_filter(phant, sigma=0.5)  # add some smoothing

    # Add vasculature
    phant[vasc_mask == 1] = np.random.poisson(
        mu_vasc, phant[vasc_mask == 1].size)

    return phant
