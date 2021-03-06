import math
import numpy as np
from scipy.special import sph_harm
from sklearn.neighbors import NearestNeighbors
from dipy.core.sphere import Sphere
from dipy.direction.peaks import peak_directions
from .util import split_comps
import pkg_resources
data_path = pkg_resources.resource_filename('strtens', 'data/')


def make_sphere(n):
    '''
    Fibonacci Sampling:
    Returns "equally" spaced points on a unit sphere in spherical coordinates.
    http://stackoverflow.com/a/26127012/5854689
    '''

    z = np.linspace(1 - 1 / n, -1 + 1 / n, num=n)
    polar = np.arccos(z)
    azim = np.mod((np.pi * (3.0 - np.sqrt(5.0))) *
                  np.arange(n), 2 * np.pi) - np.pi
    azim[azim < 0] += 2 * np.pi  # sph_harm functions require azim in [0, 2pi]

    sphere = Sphere(theta=polar, phi=azim)
    return sphere


def cart_to_spherical(vectors, FA=None, FA_threshold=0.69, im=None, im_threshold=83):
    '''
    Takes [...,3] ndarray of vectors and returns flat lists of
    polar and azim values in spherical coordinates.

    Note:
    polar is in [0, pi]
    azim is in [0, 2pi]
    '''

    # Always threshold by FA, NOT always threshold by im
    if FA is not None and im is None:
        vectors = vectors[FA > FA_threshold]
    elif FA is not None and im is not None:
        vectors = vectors[(FA > FA_threshold) & (im > im_threshold)]

    v0, v1, v2 = split_comps(vectors)
    r = np.sqrt(v0**2 + v1**2 + v2**2)
    polar = np.arccos(v2 / r)  # z / r
    azim = np.arctan2(v1, v0)  # y / x
    azim[azim < 0] += 2 * np.pi  # sph_harm functions require azim in [0,2pi]

    return polar, azim


def check_even(degree):
    if degree % 2 != 0:
        raise ValueError('SH Degree must be even')


def check_vectors(vectors):
    if (vectors.ndim != 2) | (vectors.shape[-1] != 3):
        return vectors.reshape((-1, 3))
    else:
        return vectors


def get_SH_loop_ind(degree, even=True):
    '''
    Get indices for looping the even-n, positive-m SHs
    '''
    if even:
        check_even(degree)
        mn = [(m, n) for n in range(0, degree + 1, 2)
              for m in range(0, n + 1)]
    else:
        mn = [(m, n) for n in range(0, degree + 1, 1) for m in range(0, n + 1)]
    return mn


def real_sph_harm(m, n, polar, azim):
    '''
    Assumes m is positive, calculates sph_harm for +m and -m using
    conjugate symmetry
    '''
    sh = sph_harm(m, n, azim, polar)
    if m != 0:
        # Implements conjugate symmetry as in Dipy.
        # Note: it is faster to include sqrt(2) factor when
        # calculating the coefficients.
        real_neg = sh.real
        real_pos = sh.imag
        return real_neg, real_pos
    else:
        return sh.real


def _precompute_SH(N=6500, degree=20):
    sphere = make_sphere(N)
    mn = get_SH_loop_ind(degree)
    num_coeffs = int(((degree * 2 + 3)**2 - 1) / 8)
    sh = np.zeros((num_coeffs, N))
    count = 0
    for m, n in mn:
        if m == 0:
            sh[count] = real_sph_harm(m, n, sphere.theta, sphere.phi)
            count += 1
        else:
            neg, pos = real_sph_harm(m, n, sphere.theta, sphere.phi)
            sh[count] = math.sqrt(2) * neg
            count += 1
            sh[count] = math.sqrt(2) * pos
            count += 1
    np.save(data_path + 'sh_deg{}_n{}'.format(degree, N), sh)


def make_hist(vectors, sphere):

    hist_points = np.stack((sphere.x, sphere.y, sphere.z), axis=-1)
    nbrs = NearestNeighbors(n_neighbors=1,
                            algorithm='ball_tree',
                            leaf_size=5).fit(hist_points)
    indices = nbrs.kneighbors(vectors, return_distance=False)
    hist = np.bincount(indices.flatten(), minlength=sphere.theta.size)
    return hist


def get_SH_coeffs(vectors, K, pre=True, n_bins=6500, degree=20):
    '''
    Calculate even-degree SH coefficients up to 'degree'
    Order of output is given by:

    (m, n)
    ______
    (0, 0)
    (0, 2)
    (-1, 2)
    (1, 2)
    (-2, 2)
    (2, 2)
    (0, 3)
      .
      .
      .
    '''

    vectors = check_vectors(vectors)
    sphere = make_sphere(n_bins)
    hist = make_hist(vectors, sphere)
    if pre:
        sh = np.load(data_path + 'sh_deg20_n6500.npy')
        c = (sh * hist[None, :]).sum(axis=1) / K
    else:
        mn = get_SH_loop_ind(degree)
        c = []
        app = c.append

        for m, n in mn:
            if m == 0:
                app((hist * real_sph_harm(m, n, sphere.theta, sphere.phi)).sum() / K)
            else:
                neg, pos = real_sph_harm(m, n, sphere.theta, sphere.phi)
                app(math.sqrt(2) * (hist * neg).sum() / K)
                app(math.sqrt(2) * (hist * pos).sum() / K)
    return c


def get_SH_coeffs_delta(vectors, K, even=True, degree=20):
    '''
    Calculate even-degree SH coefficients up to 'degree'
    Order of output is given by:

    (n, m)
    ______
    (0, 0)
    (2, 0)
    (2, -1)
    (2, 1)
    (2, -2)
    (2, 2)
    (3, 0)
      .
      .
      .
    '''
    polar, azim = cart_to_spherical(vectors)
    mn = get_SH_loop_ind(degree, even)
    c = []
    app = c.append
    K = polar.size
    for m, n in mn:
        if m == 0:
            app(real_sph_harm(m, n, polar, azim).sum() / K)
        else:
            neg, pos = real_sph_harm(m, n, polar, azim)
            app(math.sqrt(2) * neg.sum() / K)
            app(math.sqrt(2) * pos.sum() / K)

    return c


def get_odf(coeffs, sphere, degree, even=True):
    '''
    Calculates odf as linear combination of real SH using coeffs,
    evaluated on sample points defined by sphere.
    '''
    mn = get_SH_loop_ind(degree, even)
    odf = np.zeros(sphere.phi.size)
    i = 0
    for m, n in mn:
        if m == 0:
            odf += coeffs[i] * real_sph_harm(m, n, sphere.theta, sphere.phi)
            i += 1
        else:
            Y_neg, Y_pos = real_sph_harm(m, n, sphere.theta, sphere.phi)
            odf += coeffs[i] * Y_neg
            i += 1
            odf += coeffs[i] * Y_pos
            i += 1
    odf = np.clip(odf, 1e-16, odf.max())
    return odf


def get_peaks(odf, sphere, threshold=0.2, minsep=10):
    dirs, vals, inds = peak_directions(odf, sphere,
                                       relative_peak_threshold=threshold,
                                       min_separation_angle=minsep)
    return dirs, vals, inds


def prep_dirs(dirs):
    # Takes in Nx3 array of direction coordinates
    # makes all x-coordinates positive and sorts by x-coordinate
    dirs[dirs[..., 0] < 0] *= -1  # make all x's positive
    if dirs.ndim > 1:
        dirs = dirs[dirs[..., 0].argsort()]  # sort by x
    return dirs


def get_ang_distance(dirs0, dirs1):
    # Takes two direction coordinate arrays and returns angular distance
    # between each unique direction

    # Sort peaks
    dirs0 = prep_dirs(dirs0)
    dirs1 = prep_dirs(dirs1)

    # Calculate angle in degrees
    ang = np.arccos((dirs0 * dirs1).sum(axis=-1)) * 180 / np.pi

    # Restrict to being between 0-90 degrees
    ang = np.where(ang > 90, 180 - ang, ang)
    return ang


def calc_ACC(c1, c2):
    '''
    Takes in two SH coefficients and calculates the
    angular correlation coefficient 
    '''

    c1_norm = np.sqrt((abs(c1)**2).sum())
    c2_norm = np.sqrt((abs(c2)**2).sum())

    ACC = (c1 * c2).sum() / (c1_norm * c2_norm)
    return ACC


def calc_JSD(c1, c2, sphere):
    P = get_odf(c1, sphere)
    P /= P.sum()
    Q = get_odf(c2, sphere)
    Q /= Q.sum()
    M = (P + Q) / 2
    D_PM = (P * np.log(P / M)).sum()
    D_QM = (Q * np.log(Q / M)).sum()
    JSD = (D_PM + D_QM) / 2
    return JSD


def APS(c):
    num_coeffs = c.shape[-1]
    degree = int((np.sqrt(8 * num_coeffs + 1) - 3) // 2)

    even_mns = get_SH_loop_ind(20)
    l_inds = []
    for mn in even_mns:
        m, l = mn
        if l == 0:
            l_inds.append(l)
        elif m == 0:
            l_inds.append(l)
        if m != 0:
            l_inds.append(l)
            l_inds.append(l)

    l_inds = np.array(l_inds)
    l_labs = np.unique(l_inds)

    aps = []
    for l in l_labs:
        aps.append((c[l_inds == l]**2).sum())

    return np.array(aps)
