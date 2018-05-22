import math
import numpy as np
from scipy.special import sph_harm
from strtens.util import split_comps, make_sphere, imread
from strtens import StructureTensor
from dipy.data import get_sphere
from dipy.viz import window, actor
from dipy.reconst.shm import sph_harm_ind_list, real_sph_harm
from dipy.direction.peaks import peak_directions
from time import perf_counter


def get_directions(fn='../../data/sample_vectors_d2.5_n5.npy'):
    vectors = np.load(fn)
    vz, vy, vx = split_comps(vectors)
    r = np.sqrt(vz**2 + vy**2 + vx**2)
    theta = np.arccos(vz / r)
    phi = np.arctan2(vy, vx)
    phi[phi < 0] += 2 * np.pi  # sph_harm requires [0,2pi]

    return theta, phi


def get_SH_ind_fast(order):

    mn = [(m, n) for n in range(0, order + 1, 2)
          for m in range(0, n + 1)]
    return mn


def my_sph_harm_fast(m, n, theta, phi):
    # Assumes m is positive, calculates sph_harm for +m and -m using
    # conjugate symmetry
    sh = sph_harm(m, n, phi, theta)
    if m != 0:
        real_neg = sh.real
        real_pos = sh.imag
        return real_neg, real_pos
    else:
        return sh.real


def sh_fast(order, theta, phi):
    mn = get_SH_ind_fast(order)
    c = []
    app = c.append
    K = theta.size
    for m, n in mn:
        if m == 0:
            app(my_sph_harm_fast(m, n, theta, phi).sum() / K)
        else:
            neg, pos = my_sph_harm_fast(m, n, theta, phi)
            app(math.sqrt(2) * neg.sum() / K)
            app(math.sqrt(2) * pos.sum() / K)

    return c


def test(theta):
    mn = get_SH_ind_fast(20)
    c = []
    capp = c.append
    K = theta.size
    for m, n in mn:
        if m == 0:
            capp((m + n) / K)
        else:
            capp(m / K)
            capp(n / K)
    return c


def get_SH_ind(order):

    mn = np.array([(m, n) for n in range(0, order + 1, 2)
                   for m in range(0, n + 1)])
    return mn[:, 0], mn[:, 1]


def my_sph_harm(m, n, theta, phi):
    # Assumes m is positive, calculates sph_harm for +m and -m using
    # conjugate symmetry
    sh = sph_harm(abs(m), n, phi, theta)
    if m != 0:
        sh *= math.sqrt(2)
        real_neg = sh.real
        real_pos = sh.imag
        return real_neg, real_pos
    else:
        return sh.real


def sh_old(order, theta, phi):
    m, n = get_SH_ind(order)
    c = []
    app = c.append
    for m, n in zip(m, n):
        if m == 0:
            app(my_sph_harm(m, n, theta, phi).sum())
        else:
            neg, pos = my_sph_harm(m, n, theta, phi)
            app(neg.sum())
            app(pos.sum())
    return np.array(c) / theta.size


def odf_fast(order, theta, phi, sphere):
    m, n = get_SH_ind(order)
    odf = np.zeros(sphere.phi.size)
    coeffs = []
    app = coeffs.append
    for m, n in zip(m, n):
        print(n, m)
        if m == 0:
            c = my_sph_harm(m, n, theta, phi).sum()
            app(c)
            odf += c * my_sph_harm(m, n, sphere.theta, sphere.phi)
        else:
            c_neg, c_pos = my_sph_harm(m, n, theta, phi)
            Y_neg, Y_pos = my_sph_harm(m, n, sphere.theta, sphere.phi)
            c_neg = c_neg.sum()
            app(c_neg)
            c_pos = c_pos.sum()
            app(c_pos)

            odf += c_neg * Y_neg
            odf += c_pos * Y_pos
    return np.array(coeffs) / theta.size, odf / theta.size


def odf_from_coeffs(order, coeffs, sphere):
    m, n = get_SH_ind(order)
    odf = np.zeros(sphere.phi.size)
    i = 0
    for m, n in zip(m, n):
        if m == 0:
            odf += c[i] * my_sph_harm(m, n, sphere.theta, sphere.phi)
            i += 1
        else:
            Y_neg, Y_pos = my_sph_harm(m, n, sphere.theta, sphere.phi)
            odf += c[i] * Y_neg
            i += 1
            odf += c[i] * Y_pos
            i += 1
    return odf


def sh_coeffs(order, theta, phi):
    m, n = sph_harm_ind_list(order)
    c = np.zeros(m.size)
    for i, (m_i, n_i) in enumerate(zip(m, n)):
        c[i] = real_sph_harm(m_i, n_i, theta, phi).sum()
    return c / theta.size


def get_odf(order, data_theta, data_phi, sphere):
    m, n = sph_harm_ind_list(order)
    odf = np.zeros(sphere.phi.size)
    c = np.zeros(m.size)
    K = data_theta.size
    for i, (m_i, n_i) in enumerate(zip(m, n)):
        c[i] = 1 / K * real_sph_harm(m_i, n_i, data_theta, data_phi).sum()
        odf += c[i] * real_sph_harm(m_i, n_i, sphere.theta, sphere.phi)

    return c, odf


from strtens.vis import show_ODF
# sphere = make_sphere(10000)
# theta, phi = get_directions()
# start = perf_counter()
# c, odf = odf_fast(18, theta, phi, sphere)
# dirs, values, inds = peak_directions(odf, sphere)
# print('That took ', np.round(perf_counter() - start, 2), ' seconds')
# odf = odf_from_coeffs(18, c, sphere)
# show_ODF(odf, sphere)  # , peaks=(dirs, values))
