import numpy as np
from strtens import StructureTensor
from strtens.util import imread, make_ODF
from mayavi import mlab

print('Reading image')
im = imread('../../../data/xray/recon_2x_stack-1.tif')

print('Calculating structure tensor')
AI, vectors = StructureTensor(im,
                              d_sigma=2,
                              n_sigma=7).results()


def plot_ODF(x, y, z, s, fignum=1):
    fig = mlab.figure(fignum,
                      bgcolor=(1, 1, 1),
                      fgcolor=(0, 0, 0),
                      size=(1200, 800))
    mlab.mesh(x, y, z, scalars=s)
    mlab.outline()
    mlab.orientation_axes()
    return fig


print('Making First ODF')
mlab.close(all=True)
n = 800
x, y, z, s = make_ODF(n, vectors)
fig = plot_ODF(x, y, z, s, fignum=1)
mlab.savefig('../figs/ODF_full_d2n7_view1.png')
v2 = mlab.view(azimuth=-30,
               elevation=84)
mlab.savefig('../figs/ODF_full_d2n7_view2.png')

print('Making next ODF')
mlab.close(all=True)
mask = np.where(AI <= 0.5*AI.max(), False, True)
masked_vectors = vectors * np.expand_dims(mask, -1)
x, y, z, s = make_ODF(n, masked_vectors)
fig2 = plot_ODF(x, y, z, s, fignum=2)
mlab.savefig('../figs/ODF_masked_d2n7_view1.png')
v2 = mlab.view(azimuth=-28.8,
               elevation=90.5)
mlab.savefig('../figs/ODF_masked_d2n7_view2.png')
