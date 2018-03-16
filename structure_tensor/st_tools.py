import numpy as np
from skimage import io, color
from skimage.feature import structure_tensor, structure_tensor_eigvals
import tifffile
from scipy import ndimage as ndi
from skimage._shared.utils import assert_nD
from skimage.util.dtype import img_as_float


def _rescale(a):
    '''
    Rescales an array to 0-1.0
    '''
    return (a - a.min()) / (a - a.min()).max()


def st_2D(im, sigma=2):
    '''
    Calculates the principal orientation direction and anisotropy index
    from a 2D image using the structure tensor.

    Assumes image shape is (y,x)


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


def st_3D(im, d_sigma, n_sigma):
    '''
    Calculates principal orientation vector and fractional anisotropy from
    a 3D volume using the structure tensor.

    NOTE: Assumes image shape is (x,y,z)
    '''

    print('Calculating tensor elements')
    fxx, fxy, fxz, fyy, fyz, fzz = _structure_tensor_3D(
        im, d_sigma=d_sigma, n_sigma=n_sigma)

    F = np.array([[fxx, fxy, fxz],
                  [fxy, fyy, fyz],
                  [fxz, fyz, fzz]])

    # np.linalg.eigh requires shape = (...,3,3)
    F = np.moveaxis(F, [0, 1], [3, 4])

    print('Calculating eigenvectors')
    evals, evectors = np.linalg.eigh(F)
    evectors = evectors[..., 0]  # taking vector w/ smallest eval

    FA = np.where(np.linalg.norm(evals, axis=-1) **
                  2 != 0, _FA(evals), np.zeros_like(im))

    return FA, evectors


def _FA(evals):
    '''
    Calculates fractional anisotropy image from the eigenvalues image. 
    Eigenvalues are ordered from smallest to largest, so t1 > t2 > t3. 

    Formula taken from [Khan et al, NeuroImage (111), 2015.]
    '''

    t1 = evals[..., 2]
    t2 = evals[..., 1]
    t3 = evals[..., 0]

    norm2 = t1**2 + t2**2 + t3**2
    with np.errstate(invalid='ignore'):
        return np.sqrt(((t1 - t2)**2 + (t2 - t3)**2 + (t3 - t1)**2) / (2 * norm2))


def make_3D_rgb(im, d_sigma=1.0, n_sigma=1.0, bit=50):
    '''
    Makes HSL (Hue, Saturation, Level) image from 3D structure tensor results.
    Hue is mapped from orientation (more work on that in the future), Saturation:
    FA, Level: im.

    Converts HSL to RGB stack for export to tiff.
    '''

    FA, vects = st_3D(im, d_sigma=d_sigma, n_sigma=n_sigma)

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


def make_comps(vects, im, reorient=False):
    '''
    Returns separate arrays for three components of eigenvector, masked by im
    '''
    u = np.where(im != 0, vects[..., 0], np.zeros_like(im))  # x
    v = np.where(im != 0, vects[..., 1], np.zeros_like(im))  # y
    w = np.where(im != 0, vects[..., 2], np.zeros_like(im))  # z

    if reorient:
        cond = (w < 0) | ((w == 0) & (v < 0)) | ((w == 0) & (v == 0) & (u < 0))
        u = np.where(cond, -1 * u, u)
        v = np.where(cond, -1 * v, v)
        w = np.where(cond, -1 * w, w)

    return u, v, w


def _structure_tensor_3D(image, d_sigma=1, n_sigma=1, mode='constant', cval=0):
    """
    MODIFIED FROM SKIMAGE BY SCOTT TRINKLE, 2018

    Compute structure tensor using sum of squared differences.

    The structure tensor A is defined as::

        A = [Axx Axy Axz]
            [Axy Ayy Ayz]
            [Axz Ayz Azz]

    which is approximated by the weighted sum of squared differences in a local
    window around each pixel in the image.

    Parameters
    ----------
    image : ndarray
        Input image.
    d_sigma : float, optional
        Standard deviation used for the Gaussian partial derivatives
    n_sigma : float, optional
        Standard deviation used for the Gaussian kernel, which is used as a
        weighting function for the local summation of squared differences.
    mode : {'constant', 'reflect', 'wrap', 'nearest', 'mirror'}, optional
        How to handle values outside the image borders.
    cval : float, optional
        Used in conjunction with mode 'constant', the value outside
        the image boundaries.

    Returns
    -------
    Axx : ndarray
        Element of the structure tensor for each pixel in the input image.
    Axy : ndarray
        Element of the structure tensor for each pixel in the input image.
    Axz : ndarray
        Element of the structure tensor for each pixel in the input image.
    Ayy : ndarray
        Element of the structure tensor for each pixel in the input image.
    Ayz : ndarray
        Element of the structure tensor for each pixel in the input image.
    Azz : ndarray
        Element of the structure tensor for each pixel in the input image.



    Examples
    --------
    >>> from skimage.feature import structure_tensor
    >>> square = np.zeros((5, 5))
    >>> square[2, 2] = 1
    >>> Axx, Axy, Ayy = structure_tensor(square, sigma=0.1)
    >>> Axx
    array([[ 0.,  0.,  0.,  0.,  0.],
           [ 0.,  1.,  0.,  1.,  0.],
           [ 0.,  4.,  0.,  4.,  0.],
           [ 0.,  1.,  0.,  1.,  0.],
           [ 0.,  0.,  0.,  0.,  0.]])

    """

    # image = _prepare_grayscale_input_3D(image)

    imx, imy, imz = _compute_derivatives(
        image, d_sigma=d_sigma, mode=mode, cval=cval)

    # structure tensor
    Axx = ndi.gaussian_filter(imx * imx, n_sigma, mode=mode, cval=cval)
    Axy = ndi.gaussian_filter(imx * imy, n_sigma, mode=mode, cval=cval)
    Axz = ndi.gaussian_filter(imx * imz, n_sigma, mode=mode, cval=cval)
    Ayy = ndi.gaussian_filter(imy * imy, n_sigma, mode=mode, cval=cval)
    Ayz = ndi.gaussian_filter(imy * imz, n_sigma, mode=mode, cval=cval)
    Azz = ndi.gaussian_filter(imz * imz, n_sigma, mode=mode, cval=cval)

    return Axx, Axy, Axz, Ayy, Ayz, Azz


def _compute_derivatives(image, d_sigma=1.0, mode='constant', cval=0):
    """
    MODIFIED FROM SKIMAGE BY SCOTT TRINKLE, 2018

    Compute derivatives in x, y and z directions using the Sobel operator.

    Parameters
    ----------
    image : ndarray
        Input image.
    d_sigma : float
        Standard deviation for Gaussian partial derivative
    mode : {'constant', 'reflect', 'wrap', 'nearest', 'mirror'}, optional
        How to handle values outside the image borders.
    cval : float, optional
        Used in conjunction with mode 'constant', the value outside
        the image boundaries.

    Returns
    -------
    imz : ndarray
        Derivative in z-direction.
    imy : ndarray
        Derivative in y-direction.
    imx : ndarray
        Derivative in x-direction.

    """
    # imx = ndi.sobel(image, axis=0, mode=mode, cval=cval)
    # imy = ndi.sobel(image, axis=1, mode=mode, cval=cval)
    # imz = ndi.sobel(image, axis=2, mode=mode, cval=cval)
    imx = ndi.gaussian_filter(
        image, [d_sigma, 0, 0], order=1, mode=mode, cval=cval)
    imy = ndi.gaussian_filter(
        image, [0, d_sigma, 0], order=1, mode=mode, cval=cval)
    imz = ndi.gaussian_filter(
        image, [0, 0, d_sigma], order=1, mode=mode, cval=cval)

    return imx, imy, imz


def _prepare_grayscale_input_3D(image):
    '''
    Input handling, from skimage
    '''
    image = np.squeeze(image)
    assert_nD(image, 3)
    return img_as_float(image)
