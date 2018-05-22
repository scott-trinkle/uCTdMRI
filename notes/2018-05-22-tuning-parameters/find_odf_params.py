import numpy as np
import matplotlib.pyplot as plt
import angular_dist_phantoms as phantom
from strtens import odftools
from strtens.vis import show_ODF, show_peaks
from dipy.direction.peaks import peak_directions


def get_peaks(theta, phi, order, sphere):
    c = odftools.get_SH_coeffs(order, theta, phi)
    odf = odftools.get_odf(c, sphere)
    dirs, _, _ = peak_directions(odf, sphere, relative_peak_threshold=0.2,
                                 min_separation_angle=10)
    return dirs


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


def check_error(degree, sphere_size):
    '''
    Returns average of angular error for both peaks as a function of
    separation angle.

    Input is a given SH degree and sphere_size
    '''
    sphere = odftools.make_sphere(sphere_size)
    ang_distances = []
    for deg in range(15, 86, 10):
        theta, phi, dirs0 = phantom.make_2peak_deg_phantom(
            deg, k=[0.0, 0.5, 0.5])
        dirs_est = get_peaks(theta, phi, degree, sphere)
        if dirs_est.shape == dirs0.shape:
            ang_distances.append(get_ang_distance(dirs0, dirs_est).mean())
    return ang_distances


def by_SH_plot():
    SH_degs = np.arange(2, 20, 2)
    by_SH = [np.mean(check_error(deg, 5000)) for deg in SH_degs]
    plt.plot(SH_degs[2:], by_SH[2:])
    plt.xlabel('Max SH degree')
    plt.ylabel('Average angular error (degrees)')
    plt.title('Average angular error for two fibers from 15 - 85 degrees')
    plt.tight_layout()
    plt.savefig('figs/by_sh.pdf')


def by_sph_size_plot():
    sph_size = np.arange(500, 5001, 250)
    by_ss = [np.mean(check_error(20, size)) for size in sph_size]
    plt.plot(sph_size, by_ss)
    plt.xlabel('Number of spherical sampling points')
    plt.ylabel('Average angular error (degrees)')
    plt.title('Average angular error for two fibers from 15 - 85 degrees')
    plt.tight_layout()
    plt.savefig('figs/by_ss.pdf')
    return by_ss


# def check_degsep_vs_SH(tol, k=[0.34, 0.33, 0.33]):
#     sphere = odftools.make_sphere(8000)
#     final_order = []
#     ang_distances = []
#     for deg in range(15, 86, 10):
#         print('\nDeg = {}'.format(deg))
#         theta, phi, dirs0 = make_2peak_deg_phantom(deg, k=k)
#         for order in range(2, 51, 2):
#             dirs_est = get_peaks(theta, phi, order, sphere)
#             if dirs_est.shape[0] == 2:  # identified both peaks
#                 print('Found both peaks with order: {}'.format(order))
#                 ang_dist = get_ang_distance(dirs0, dirs_est)
#                 if np.all(ang_dist < tol):
#                     print('And they ARE within {} degrees'.format(tol))
#                     final_order.append(order)
#                     ang_distances.append(ang_dist)
#                     break
#                 else:
#                     print('But they are not within {} degrees'.format(tol))
#                     if order == 50:
#                         final_order.append(-1)
#                         ang_distances.append(-1)
#             else:
#                 print('Did not find both peaks with order: {}'.format(order))

#     return final_order, ang_distances


# def check_degsep_vs_sphere_size(tol, k=[0.34, 0.33, 0.33]):
#     order = 20
#     final_sph_size = []
#     ang_distances = []
#     for deg in range(15, 86, 10):
#         print('\nDeg = {}'.format(deg))
#         theta, phi, dirs0 = make_2peak_deg_phantom(deg, k=k)
#         for sph_size in range(50, 2001, 50):
#             sphere = odftools.make_sphere(sph_size)
#             dirs_est = get_peaks(theta, phi, order, sphere)
#             if dirs_est.shape[0] == 2:  # identified both peaks
#                 print('Found both peaks with sph size: {}'.format(sph_size))
#                 ang_dist = get_ang_distance(dirs0, dirs_est)
#                 if np.all(ang_dist < tol):
#                     print('And they ARE within {} degrees'.format(tol))
#                     final_sph_size.append(sph_size)
#                     ang_distances.append(ang_dist)
#                     break
#                 else:
#                     print('But they are not within {} degrees'.format(tol))
#                     if sph_size == 8000:
#                         final_sph_size.append(-1)
#                         ang_distances.append(-1)

#     return final_sph_size, ang_distances


# def check_npeaks_vs_SH(tol):
#     sphere = odftools.make_sphere(8000)
#     final_order = []
#     ang_distances = []
#     for n in range(1, 8):  # loop through number of peaks
#         print('\nN = {}'.format(n))
#         theta, phi, dirs0 = make_npeak_phantom(n)
#         for order in range(2, 51, 2):  # find lowest order to resolve peaks
#             dirs_est = get_peaks(theta, phi, order, sphere)
#             if dirs_est.shape[0] == n:  # identified all peaks
#                 print('Found {} peaks with order: {}'.format(n, order))
#                 ang_dist = get_ang_distance(dirs0, dirs_est)
#                 if np.all(ang_dist < tol):
#                     print('And they ARE within {} degrees'.format(tol))
#                     final_order.append(order)
#                     ang_distances.append(ang_dist)
#                     break
#                 else:
#                     print('But they are not with {} degrees'.format(tol))
#                     if order == 50:
#                         final_order.append(-1)
#                         ang_distances.append(-1)
#     return final_order, ang_distances

# # ^ Conclusion: You only need SH up to 20 to resolve 7 peaks within 5 degrees


# def check_npeaks_vs_sphere_size(tol):
#     order = 20
#     final_sphere_size = []
#     ang_distances = []
#     for n in range(1, 8):  # loop through number of peaks
#         print('\nN = {}'.format(n))
#         theta, phi, dirs0 = make_npeak_phantom(n)

#         # find lowest sph_size to resolve peaks
#         for sph_size in np.linspace(500, 5000, 15):
#             sphere = odftools.make_sphere(int(sph_size))
#             dirs_est = get_peaks(theta, phi, order, sphere)
#             if dirs_est.shape[0] == n:  # identified all peaks
#                 print('Found {} peaks with order: {}'.format(n, order))
#                 ang_dist = get_ang_distance(dirs0, dirs_est)
#                 if np.all(ang_dist < tol):
#                     print('And they ARE within {} degrees'.format(tol))
#                     final_sphere_size.append(sph_size)
#                     ang_distances.append(ang_dist)
#                     break
#                 else:
#                     print('But they are not with {} degrees'.format(tol))
#                     if order == 30:
#                         final_sphere_size.append(-1)
#                         ang_distances.append(-1)
#     return final_sphere_size, ang_distances
