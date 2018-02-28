import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color
from skimage.feature import structure_tensor, structure_tensor_eigvals
import tifffile
from st3d import structure_tensor_3D

commissure = io.imread('data/anterior_commissure_8x_sub_sample.tif')
fibers = io.imread('data/artificial-fibers.tif')


def st_analysis_2D(im, sigma=2):

    fxx, fxy, fyy = structure_tensor(im, sigma)
    theta = 1 / 2 * np.arctan2(2 * fxy, fyy - fxx)

    l1, l2 = structure_tensor_eigvals(fxx, fxy, fyy)
    AI = np.where(l1 + l2 > 0, (l1 - l2) / (l1 + l2), np.zeros(l1.shape))

    hsv = np.zeros((im.shape[0], im.shape[1], 3), dtype=np.float64)
    hsv[..., 0] = rescale(theta)
    hsv[..., 1] = rescale(AI)
    hsv[..., 2] = rescale(im)

    rgb = color.hsv2rgb(hsv)

    return rgb


def st_analysis_3D(im, sigma):
    fxx, fxy, fxz, fyy, fyz, fzz = structure_tensor_3D(im, sigma)
    F = np.array([[fxx, fxy, fxz],
                  [fxy, fyy, fyz],
                  [fxz, fyz, fzz]])
    F = np.moveaxis(F, [0, 1], [3, 4])

    evals, evectors = np.linalg.eigh(F)
    evectors = evectors[..., 0]

    # t1 = 2  largest
    # t2 = 1  middle
    # t3 = 0  smallest

    FA = np.where(np.linalg.norm(evals, axis=-1) ** 2 != 0,
                  np.sqrt(0.5 * ((evals[..., 2] - evals[..., 1])**2 +
                                 (evals[..., 1] - evals[..., 0])**2 +
                                 (evals[..., 2] - evals[..., 0])**2) / (np.linalg.norm(evals, axis=-1)**2)), np.zeros(im.shape))

    return FA, evectors


def rescale(a):
    return (a - a.min()) / a.max()


def save(fn, im):
    rescaled = (im * 255).astype(np.uint8)
    tifffile.imsave(fn, rescaled)


# 23, 70, 250
FA, vects = st_analysis_3D(commissure, 2)

from mpl_toolkits.mplot3d import axes3d

# p0 = [0.799319, -3.477045e-01, 0.490093]
# p1 = [0.852512, 9.113778e-16, -0.522708]
# p2 = [0.296422, 9.376042e-01, 0.181748]

# origin = [0, 0, 0]
# X, Y, Z = zip(origin, origin, origin)
# U, V, W = zip(p0, p1, p2)

z, y, x = commissure.shape

Z, Y, X = np.meshgrid(np.arange(z),
                      np.arange(y),
                      np.arange(y))

U = vects[..., 0]
V = vects[..., 1]
W = vects[..., 2]


# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.quiver(X, Y, Z, U, V, W, arrow_length_ratio=0.01)
# plt.show()
