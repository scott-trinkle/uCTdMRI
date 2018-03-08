'''
This script extends the structure_tensor function from skimage to 3D. 
Most of the code is directly modified. 
'''

import numpy as np
from scipy import ndimage as ndi
from skimage._shared.utils import assert_nD
from skimage.util.dtype import img_as_float


def structure_tensor_3D(image, sigma=1, mode='constant', cval=0):
    """Compute structure tensor using sum of squared differences.

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
    sigma : float, optional
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

    image = _prepare_grayscale_input_3D(image)

    imx, imy, imz = _compute_derivatives(image, mode=mode, cval=cval)

    # structure tensor
    Axx = ndi.gaussian_filter(imx * imx, sigma, mode=mode, cval=cval)
    Axy = ndi.gaussian_filter(imx * imy, sigma, mode=mode, cval=cval)
    Axz = ndi.gaussian_filter(imx * imz, sigma, mode=mode, cval=cval)
    Ayy = ndi.gaussian_filter(imy * imy, sigma, mode=mode, cval=cval)
    Ayz = ndi.gaussian_filter(imy * imz, sigma, mode=mode, cval=cval)
    Azz = ndi.gaussian_filter(imz * imz, sigma, mode=mode, cval=cval)

    return Axx, Axy, Axz, Ayy, Ayz, Azz


def _compute_derivatives(image, mode='constant', cval=0):
    """Compute derivatives in x, y and z directions using the Sobel operator.

    Parameters
    ----------
    image : ndarray
        Input image.
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

    imz = ndi.sobel(image, axis=0, mode=mode, cval=cval)
    imy = ndi.sobel(image, axis=1, mode=mode, cval=cval)
    imx = ndi.sobel(image, axis=2, mode=mode, cval=cval)

    return imx, imy, imz


def _prepare_grayscale_input_3D(image):
    image = np.squeeze(image)
    assert_nD(image, 3)
    return img_as_float(image)
