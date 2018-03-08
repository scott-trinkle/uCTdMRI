import numpy as np
from skimage import io, color
from skimage.feature import structure_tensor, structure_tensor_eigvals
import tifffile
from st3d import structure_tensor_3D


def _rescale(a):
    return (a - a.min()) / (a - a.min()).max()


def st_2D(im, sigma=2):
    '''
    Calculates the principal orientation direction and anisotropy index
    from a 2D image using the structure tensor. 

    Returns:
    ________
    theta : ndarray
        Principle orientation direction in radians on the interval [-pi,pi]
    AI : ndarray
        Anisotropy index, calculated according to (Budde 2012)
    '''

    fxx, fxy, fyy = structure_tensor(im, sigma)
    theta = 1 / 2 * np.arctan2(2 * fxy, fyy - fxx)

    l1, l2 = structure_tensor_eigvals(fxx, fxy, fyy)
    AI = np.where(l1 + l2 > 0, (l1 - l2) / (l1 + l2), np.zeros(l1.shape))

    return theta, AI


def make_2D_rgb(im, sigma):
    '''
    Make HSL (Hue, Saturation, Level) image from 2D structure tensor results. 
    Hue: Theta, Saturation: AI, Level: im. 

    Converts HSL to RGB for export to tiff. 
    '''

    theta, AI = st_2D(im, sigma)
    hsv = np.zeros((im.shape[0], im.shape[1], 3), dtype=np.float64)
    hsv[..., 0] = _rescale(theta)
    hsv[..., 1] = _rescale(AI)
    hsv[..., 2] = _rescale(im)

    return color.hsv2rgb(hsv)


def st_3D(im, sigma):
    '''
    Calculates principal orientation vector and fractional anisotropy from
    a 3D volume using the structure tensor. 
    '''

    fxx, fxy, fxz, fyy, fyz, fzz = structure_tensor_3D(im, sigma)
    F = np.array([[fxx, fxy, fxz],
                  [fxy, fyy, fyz],
                  [fxz, fyz, fzz]])

    # np.linalg.eigh requires shape = (...,3,3)
    F = np.moveaxis(F, [0, 1], [3, 4])

    evals, evectors = np.linalg.eigh(F)
    evectors = evectors[..., 0]  # taking vector w/ smallest eval

    # t1 = 2  largest
    # t2 = 1  middle
    # t3 = 0  smallest

    FA = np.where(np.linalg.norm(evals, axis=-1) ** 2 != 0,
                  np.sqrt(0.5 * ((evals[..., 2] - evals[..., 1])**2 +
                                 (evals[..., 1] - evals[..., 0])**2 +
                                 (evals[..., 2] - evals[..., 0])**2) / (np.linalg.norm(evals, axis=-1)**2)), np.zeros_like(im))
    return FA, evectors


def make_3D_rgb(im, sigma, bit=50):
    '''
    Makes HSL (Hue, Saturation, Level) image from 3D structure tensor results. 
    Hue is mapped from orientation (more work on that in the future), Saturation:
    FA, Level: im. 

    Converts HSL to RGB stack for export to tiff. 
    '''

    FA, vects = st_3D(im, sigma)

    s = bit**2 + vects[..., 0] + bit * vects[..., 1] + vects[..., 2]

    slices, rows, cols = im.shape
    hsv = np.zeros((slices, rows, cols, 3), dtype=np.float64)
    hsv[..., 0] = _rescale(s)
    hsv[..., 1] = _rescale(FA)
    hsv[..., 2] = _rescale(im)

    return np.array([color.hsv2rgb(hsv[z]) for z in np.arange(slices)])


def save_rgb(fn, im):
    '''
    Saves output of make_2D_rgb or make_3D_rgb as tiff image. 

    Example:
    save_rgb('results/visualize_3d/full_sample_sigma_3.tif', make_3D_rgb(im, 3))

    for sig in [1, 2, 3, 5, 10, 25]:
        print('Saving sig: {}'.format(sig))
        fn = 'sig_{}.tif'.format(sig)
        save_rgb(fn, make_3D_rgb(im, sig))

    '''
    rescaled = (_rescale(im) * 255).astype(np.uint8)
    tifffile.imsave(fn, rescaled)


def make_comps(vects, im):
    '''
    Returns separate arrays for three components of eigenvector, masked by im
    '''
    u = np.where(im != 0, vects[..., 2], np.zeros_like(im))  # x
    v = np.where(im != 0, vects[..., 1], np.zeros_like(im))  # y
    w = np.where(im != 0, vects[..., 0], np.zeros_like(im))  # z (^I assume...)
    return u, v, w
