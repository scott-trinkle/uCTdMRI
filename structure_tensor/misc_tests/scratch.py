import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from mayavi import mlab
import sys
sys.path.append('..')
import st_tools as st
import tifffile as tf

phantom = 'xray'
log = False
scaled = False
mayavi = True

# constants
pi = np.pi
n = int(1e6)
nbins = 100
res = 100
theta = np.random.uniform(0, pi, n)  # random polar angles
phi = np.random.uniform(0, 2 * pi, n)  # random azimuthal angles

# Defining the angular locations of the patches
nspots = 5
tangs = np.linspace(20, 160, nspots) * pi / 180
pangs = np.linspace(90, 90, nspots) * pi / 180
d_angle = 15
d = np.ones(nspots) * d_angle / 2 * pi / 180


# Returns center bin values
n_grid = res if phantom == 'fixed' else nbins
tbin = np.linspace(0, pi, n_grid)
pbin = np.linspace(0, 2 * pi, n_grid)

# Create a sphere
T, P = np.meshgrid(tbin, pbin, indexing='ij')
r = 0.3
x = r * np.sin(T) * np.cos(P)
y = r * np.sin(T) * np.sin(P)
z = r * np.cos(T)

if phantom == 'xray':
    print('Reading image')
    im = io.imread('../../data/recon_2x_stack-1.tif')

    print('Running ST analysis')
    FA, vects = st.st_3D(im,
                         d_sigma=2,
                         n_sigma=5,
                         westin=True)
    print('saving')
    fig, axs = plt.subplots(1, 2)

    sl = 25
    axs[0].imshow(FA[sl], cmap='gray')
    axs[0].set_title('FA')
    axs[0].axis('off')
    axs[1].imshow(im[sl], cmap='gray')
    axs[1].set_title('Im')
    axs[1].axis('off')
    plt.show()

    # r = np.sqrt(vects[..., 0]**2 + vects[..., 1]**2 + vects[..., 2]**2)
    # theta = np.arccos(vects[..., 2] / r)
    # phi = np.arctan2(vects[..., 1], vects[..., 0]) + np.pi

    # norm = False if log else True

    # H, _, _ = np.histogram2d(theta.flatten(), phi.flatten(), bins=nbins,
    #                          normed=norm)


if phantom == 'pairwise':
    '''
    This method generates an actual histogram based on simulated "paired" angle
    coordinates. The background is less uniform due to how the hot spots are
    defined, but the methodology is closer to the actual data.
    '''

    for i in range(nspots):
        cond = (theta > tangs[i] - d[i]) & (theta < tangs[i] + d[i])
        size = (np.where(cond))[0].size
        phi[cond] = np.random.uniform(pangs[i] - d[i], pangs[i] + d[i], size)

    H, _, _ = np.histogram2d(theta, phi, bins=nbins, normed=False)


if phantom == 'fixed':
    H = np.random.random((res, res))
    for i in range(nspots):
        for row in range(res):
            if (tbin[row] > tangs[i] - d[i]) & (tbin[row] < tangs[i] + d[i]):
                for col in range(res):
                    if (pbin[col] > pangs[i] - d[i]) & (pbin[col] < pangs[i] + d[i]):
                        H[row, col] += 0.75


if log:
    H = np.log(H, where=H > 0)
if scaled:
    x *= H
    y *= H
    z *= H

# if mayavi:
#     mlab.figure()
#     mlab.mesh(x, y, z, scalars=H, colormap='jet')

#     if phantom == 'xray':
#         mlab.figure()
#         u, w, v = st.make_comps(vects, im)
#         field = mlab.quiver3d(u, w, v,
#                               scalars=FA,
#                               line_width=2.0,
#                               scale_factor=0.5,
#                               colormap='jet')
#         field.glyph.color_mode = 'color_by_scalar'
#         field.glyph.glyph_source.glyph_source.center = [0, 0, 0]
#         mlab.colorbar()

#     mlab.show()
# else:
#     plt.imshow(H)
#     plt.colorbar()
#     plt.xlabel('phi')
#     plt.ylabel('theta')
#     ticks = np.linspace(0, nbins - 1, 5)
#     tlabels = np.linspace(0, 180, 5, dtype=int)
#     plabels = np.linspace(0, 360, 5, dtype=int)
#     plt.xticks(ticks, plabels)
#     plt.yticks(ticks, tlabels)
#     plt.show()
