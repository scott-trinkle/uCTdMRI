from scipy import ndimage as ndi
import numpy as np


def structure_tensor(image, sigma=1, mode='constant', cval=0):
    """Compute structure tensor using sum of squared differences.

    The structure tensor A is defined as::

        A = [Axx Axy]
            [Axy Ayy]

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
    Ayy : ndarray
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

    image = _prepare_grayscale_input_2D(image)

    imx, imy = _compute_derivatives(image, mode=mode, cval=cval)

    # structure tensore
    Axx = ndi.gaussian_filter(imx * imx, sigma, mode=mode, cval=cval)
    Axy = ndi.gaussian_filter(imx * imy, sigma, mode=mode, cval=cval)
    Ayy = ndi.gaussian_filter(imy * imy, sigma, mode=mode, cval=cval)

    return Axx, Axy, Ayy


def _compute_derivatives(image, mode='constant', cval=0):
    """Compute derivatives in x and y direction using the Sobel operator.

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
    imx : ndarray
        Derivative in x-direction.
    imy : ndarray
        Derivative in y-direction.

    """

    imy = ndi.sobel(image, axis=0, mode=mode, cval=cval)
    imx = ndi.sobel(image, axis=1, mode=mode, cval=cval)

    return imx, imy


def _prepare_grayscale_input_2D(image):
    image = np.squeeze(image)
    assert_nD(image, 2)
    return img_as_float(image)


def assert_nD(array, ndim, arg_name='image'):
    """
    Verify an array meets the desired ndims and array isn't empty.

    Parameters
    ----------
    array : array-like
        Input array to be validated
    ndim : int or iterable of ints
        Allowable ndim or ndims for the array.
    arg_name : str, optional
        The name of the array in the original function.

    """
    array = np.asanyarray(array)
    msg_incorrect_dim = "The parameter `%s` must be a %s-dimensional array"
    msg_empty_array = "The parameter `%s` cannot be an empty array"
    if isinstance(ndim, int):
        ndim = [ndim]
    if array.size == 0:
        raise ValueError(msg_empty_array % (arg_name))
    if not array.ndim in ndim:
        raise ValueError(msg_incorrect_dim %
                         (arg_name, '-or-'.join([str(n) for n in ndim])))


def img_as_float(image, force_copy=False):
    """Convert an image to double-precision (64-bit) floating point format.

    Parameters
    ----------
    image : ndarray
        Input image.
    force_copy : bool, optional
        Force a copy of the data, irrespective of its current dtype.

    Returns
    -------
    out : ndarray of float64
        Output image.

    Notes
    -----
    The range of a floating point image is [0.0, 1.0] or [-1.0, 1.0] when
    converting from unsigned or signed datatypes, respectively.
    If the input image has a float type, intensity values are not modified
    and can be outside the ranges [0.0, 1.0] or [-1.0, 1.0].

    """
    return convert(image, np.float64, force_copy)


def convert(image, dtype, force_copy=False, uniform=False):
    """
    Convert an image to the requested data-type.

    Warnings are issued in case of precision loss, or when negative values
    are clipped during conversion to unsigned integer types (sign loss).

    Floating point values are expected to be normalized and will be clipped
    to the range [0.0, 1.0] or [-1.0, 1.0] when converting to unsigned or
    signed integers respectively.

    Numbers are not shifted to the negative side when converting from
    unsigned to signed integer types. Negative values will be clipped when
    converting to unsigned integers.

    Parameters
    ----------
    image : ndarray
        Input image.
    dtype : dtype
        Target data-type.
    force_copy : bool, optional
        Force a copy of the data, irrespective of its current dtype.
    uniform : bool, optional
        Uniformly quantize the floating point range to the integer range.
        By default (uniform=False) floating point values are scaled and
        rounded to the nearest integers, which minimizes back and forth
        conversion errors.

    References
    ----------
    .. [1] DirectX data conversion rules.
           http://msdn.microsoft.com/en-us/library/windows/desktop/dd607323%28v=vs.85%29.aspx
    .. [2] Data Conversions. In "OpenGL ES 2.0 Specification v2.0.25",
           pp 7-8. Khronos Group, 2010.
    .. [3] Proper treatment of pixels as integers. A.W. Paeth.
           In "Graphics Gems I", pp 249-256. Morgan Kaufmann, 1990.
    .. [4] Dirty Pixels. J. Blinn. In "Jim Blinn's corner: Dirty Pixels",
           pp 47-57. Morgan Kaufmann, 1998.

    """
    image = np.asarray(image)
    dtypeobj_in = image.dtype
    dtypeobj_out = np.dtype(dtype)
    dtype_in = dtypeobj_in.type
    dtype_out = dtypeobj_out.type
    kind_in = dtypeobj_in.kind
    kind_out = dtypeobj_out.kind
    itemsize_in = dtypeobj_in.itemsize
    itemsize_out = dtypeobj_out.itemsize

    if dtype_in == dtype_out:
        if force_copy:
            image = image.copy()
        return image

    if not (dtype_in in _supported_types and dtype_out in _supported_types):
        raise ValueError("Can not convert from {} to {}."
                         .format(dtypeobj_in, dtypeobj_out))

    def sign_loss():
        warn("Possible sign loss when converting negative image of type "
             "{} to positive image of type {}."
             .format(dtypeobj_in, dtypeobj_out))

    def prec_loss():
        warn("Possible precision loss when converting from {} to {}"
             .format(dtypeobj_in, dtypeobj_out))

    def _dtype_itemsize(itemsize, *dtypes):
        # Return first of `dtypes` with itemsize greater than `itemsize`
        return next(dt for dt in dtypes if np.dtype(dt).itemsize >= itemsize)

    def _dtype_bits(kind, bits, itemsize=1):
        # Return dtype of `kind` that can store a `bits` wide unsigned int
        def compare(x, y, kind='u'):
            if kind == 'u':
                return x <= y
            else:
                return x < y

        s = next(i for i in (itemsize, ) + (2, 4, 8) if compare(bits, i * 8,
                                                                kind=kind))
        return np.dtype(kind + str(s))

    def _scale(a, n, m, copy=True):
        """Scale an array of unsigned/positive integers from `n` to `m` bits.

        Numbers can be represented exactly only if `m` is a multiple of `n`.

        Parameters
        ----------
        a : ndarray
            Input image array.
        n : int
            Number of bits currently used to encode the values in `a`.
        m : int
            Desired number of bits to encode the values in `out`.
        copy : bool, optional
            If True, allocates and returns new array. Otherwise, modifies
            `a` in place.

        Returns
        -------
        out : array
            Output image array. Has the same kind as `a`.
        """
        kind = a.dtype.kind
        if n > m and a.max() < 2 ** m:
            mnew = int(np.ceil(m / 2) * 2)
            if mnew > m:
                dtype = "int{}".format(mnew)
            else:
                dtype = "uint{}".format(mnew)
            n = int(np.ceil(n / 2) * 2)
            warn("Downcasting {} to {} without scaling because max "
                 "value {} fits in {}".format(a.dtype, dtype, a.max(), dtype))
            return a.astype(_dtype_bits(kind, m))
        elif n == m:
            return a.copy() if copy else a
        elif n > m:
            # downscale with precision loss
            prec_loss()
            if copy:
                b = np.empty(a.shape, _dtype_bits(kind, m))
                np.floor_divide(a, 2**(n - m), out=b, dtype=a.dtype,
                                casting='unsafe')
                return b
            else:
                a //= 2**(n - m)
                return a
        elif m % n == 0:
            # exact upscale to a multiple of `n` bits
            if copy:
                b = np.empty(a.shape, _dtype_bits(kind, m))
                np.multiply(a, (2**m - 1) // (2**n - 1), out=b, dtype=b.dtype)
                return b
            else:
                a = a.astype(_dtype_bits(
                    kind, m, a.dtype.itemsize), copy=False)
                a *= (2**m - 1) // (2**n - 1)
                return a
        else:
            # upscale to a multiple of `n` bits,
            # then downscale with precision loss
            prec_loss()
            o = (m // n + 1) * n
            if copy:
                b = np.empty(a.shape, _dtype_bits(kind, o))
                np.multiply(a, (2**o - 1) // (2**n - 1), out=b, dtype=b.dtype)
                b //= 2**(o - m)
                return b
            else:
                a = a.astype(_dtype_bits(
                    kind, o, a.dtype.itemsize), copy=False)
                a *= (2**o - 1) // (2**n - 1)
                a //= 2**(o - m)
                return a

    if kind_in in 'ui':
        imin_in = np.iinfo(dtype_in).min
        imax_in = np.iinfo(dtype_in).max
    if kind_out in 'ui':
        imin_out = np.iinfo(dtype_out).min
        imax_out = np.iinfo(dtype_out).max

    # any -> binary
    if kind_out == 'b':
        if kind_in in "fi":
            sign_loss()
        prec_loss()
        return image > dtype_in(dtype_range[dtype_in][1] / 2)

    # binary -> any
    if kind_in == 'b':
        result = image.astype(dtype_out)
        if kind_out != 'f':
            result *= dtype_out(dtype_range[dtype_out][1])
        return result

    # float -> any
    if kind_in == 'f':
        if np.min(image) < -1.0 or np.max(image) > 1.0:
            raise ValueError("Images of type float must be between -1 and 1.")
        if kind_out == 'f':
            # float -> float
            if itemsize_in > itemsize_out:
                prec_loss()
            return image.astype(dtype_out)

        # floating point -> integer
        prec_loss()
        # use float type that can represent output integer type
        image = image.astype(_dtype_itemsize(itemsize_out, dtype_in,
                                             np.float32, np.float64))
        if not uniform:
            if kind_out == 'u':
                image *= imax_out
            else:
                image *= imax_out - imin_out
                image -= 1.0
                image /= 2.0
            np.rint(image, out=image)
            np.clip(image, imin_out, imax_out, out=image)
        elif kind_out == 'u':
            image *= imax_out + 1
            np.clip(image, 0, imax_out, out=image)
        else:
            image *= (imax_out - imin_out + 1.0) / 2.0
            np.floor(image, out=image)
            np.clip(image, imin_out, imax_out, out=image)
        return image.astype(dtype_out)

    # signed/unsigned int -> float
    if kind_out == 'f':
        if itemsize_in >= itemsize_out:
            prec_loss()
        # use float type that can exactly represent input integers
        image = image.astype(_dtype_itemsize(itemsize_in, dtype_out,
                                             np.float32, np.float64))
        if kind_in == 'u':
            image /= imax_in
            # DirectX uses this conversion also for signed ints
            # if imin_in:
            #     np.maximum(image, -1.0, out=image)
        else:
            image *= 2.0
            image += 1.0
            image /= imax_in - imin_in
        return image.astype(dtype_out)

    # unsigned int -> signed/unsigned int
    if kind_in == 'u':
        if kind_out == 'i':
            # unsigned int -> signed int
            image = _scale(image, 8 * itemsize_in, 8 * itemsize_out - 1)
            return image.view(dtype_out)
        else:
            # unsigned int -> unsigned int
            return _scale(image, 8 * itemsize_in, 8 * itemsize_out)

    # signed int -> unsigned int
    if kind_out == 'u':
        sign_loss()
        image = _scale(image, 8 * itemsize_in - 1, 8 * itemsize_out)
        result = np.empty(image.shape, dtype_out)
        np.maximum(image, 0, out=result, dtype=image.dtype, casting='unsafe')
        return result

    # signed int -> signed int
    if itemsize_in > itemsize_out:
        return _scale(image, 8 * itemsize_in - 1, 8 * itemsize_out - 1)

    image = image.astype(_dtype_bits('i', itemsize_out * 8))
    image -= imin_in
    image = _scale(image, 8 * itemsize_in, 8 * itemsize_out, copy=False)
    image += imin_out
    return image.astype(dtype_out)


def structure_tensor_eigvals(Axx, Axy, Ayy):
    """Compute Eigen values of structure tensor.

    Parameters
    ----------
    Axx : ndarray
        Element of the structure tensor for each pixel in the input image.
    Axy : ndarray
        Element of the structure tensor for each pixel in the input image.
    Ayy : ndarray
        Element of the structure tensor for each pixel in the input image.

    Returns
    -------
    l1 : ndarray
        Larger eigen value for each input matrix.
    l2 : ndarray
        Smaller eigen value for each input matrix.

    Examples
    --------
    >>> from skimage.feature import structure_tensor, structure_tensor_eigvals
    >>> square = np.zeros((5, 5))
    >>> square[2, 2] = 1
    >>> Axx, Axy, Ayy = structure_tensor(square, sigma=0.1)
    >>> structure_tensor_eigvals(Axx, Axy, Ayy)[0]
    array([[ 0.,  0.,  0.,  0.,  0.],
           [ 0.,  2.,  4.,  2.,  0.],
           [ 0.,  4.,  0.,  4.,  0.],
           [ 0.,  2.,  4.,  2.,  0.],
           [ 0.,  0.,  0.,  0.,  0.]])

    """

    return _image_orthogonal_matrix22_eigvals(Axx, Axy, Ayy)


def _image_orthogonal_matrix22_eigvals(M00, M01, M11):
    l1 = (M00 + M11) / 2 + np.sqrt(4 * M01 ** 2 + (M00 - M11) ** 2) / 2
    l2 = (M00 + M11) / 2 - np.sqrt(4 * M01 ** 2 + (M00 - M11) ** 2) / 2
    return l1, l2
