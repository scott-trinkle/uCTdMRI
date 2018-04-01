import numpy as np
import matplotlib.pyplot as plt
from skimage import io
import sys
sys.path.append('..')
import st_tools as st

im = io.imread('../../data/recon_2x_stack-1.tif')


FA, vects = st.st_3D(im,
                     d_sigma=1,
                     n_sigma=2)

r = np.sqrt(vects[..., 0]**2 + vects[..., 1]**2 + vects[..., 2]**2)
theta = np.arccos(vects[..., 2] / r)
phi = np.arctan2(vects[..., 1], vects[..., 0]) + np.pi

H, theta_bin, phi_bin = np.histogram2d(theta.flatten(), phi.flatten(), bins=100,
                                       normed=True)

a = np.random.rand(1000) * np.linspace(0, np.pi, 1000)
b = np.random.rand(1000) * np.linspace(0, 2 * np.pi, 1000)

H, theta_bin, phi_bin = np.histogram2d(a, b, bins=100,
                                       normed=True)


# from matplotlib.colors import LogNorm

# h, xs, ys, im = plt.hist2d(pol.flatten(), azim.flatten(), bins=[
#                            180, 360], norm=LogNorm())
# plt.colorbar()
# plt.xlabel(r'Polar angle, $\theta$')
# plt.ylabel(r'Azimuthal angle, $\phi$')
# plt.show()

# from mayavi import mlab
# from scipy.special import sph_harm

# theta_bin = np.delete(theta_bin, -1)
# phi_bin = np.delete(phi_bin, -1)
# THETA, PHI = np.meshgrid(theta_bin, phi_bin)

# # Create a sphere
# r = 0.3
# x = r * np.sin(THETA) * np.cos(PHI)
# y = r * np.sin(THETA) * np.sin(PHI)
# z = r * np.cos(THETA)

# mlab.mesh(x, y, z, scalars=H, colormap='jet')
# # mlab.mesh(H * x, H * y, H * z, scalars=H, colormap='jet')
# mlab.colorbar()
# mlab.show()

# mlab.figure(1, bgcolor=(1, 1, 1), fgcolor=(0, 0, 0), size=(400, 300))
# mlab.clf()
# # Represent spherical harmonics on the surface of the sphere
# for n in range(1, 6):
#     for m in range(n):
#         s = sph_harm(m, n, theta, phi).real

#         mlab.mesh(x - m, y - n, z, scalars=s, colormap='jet')

#         s[s < 0] *= 0.97

#         s /= s.max()
#         mlab.mesh(s * x - m, s * y - n, s * z + 1.3,
#                   scalars=s, colormap='Spectral')

# mlab.view(90, 70, 6.2, (-1.3, -2.9, 0.25))
# mlab.show()
