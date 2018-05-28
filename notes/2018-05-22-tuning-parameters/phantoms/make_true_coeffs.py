import numpy as np
from strtens.util import imread
from strtens import odftools


def get_true_odf_angle(deg):
    mask = imread('./crossing_fibers/masks/z_phantom_mask_nfib9x4_r8_{}deg.tif'.format(
        deg))

    fibvoxels = mask[mask > 0]
    n_angle = (fibvoxels == 1).sum()
    n_straight = (fibvoxels == 2).sum()

    straight_theta = 0
    straight_phi = np.pi
    angle_theta = deg * np.pi / 180
    angle_phi = np.pi

    theta = [straight_theta] * n_straight + [angle_theta] * n_angle
    phi = [straight_phi] * n_straight + [angle_phi] * n_angle
    return np.array(theta), np.array(phi)


def get_true_odf_radius(r):
    mask = imread('./different_size/masks/x_phantom_nfib9_r{}.tif'.format(r))

    n = mask[mask > 0].size

    theta = n * [np.pi / 2]
    phi = n * [0]
    return np.array(theta), np.array(phi)


for deg in range(15, 86, 10):
    print(deg)
    theta, phi = get_true_odf_angle(deg)

    true_c = odftools.get_SH_coeffs(20, theta, phi)
    np.save('./crossing_fibers/true_coeffs/z_phantom_nfib9x4_r8_{}deg_coeffs'.format(deg),
            true_c)

for r in range(4, 17, 4):
    print(r)
    theta, phi = get_true_odf_radius(r)
    true_c = odftools.get_SH_coeffs(20, theta, phi)
    np.save('./different_size/true_coeffs/x_phantom_nfib9_r{}_coeffs'.format(r),
            true_c)
