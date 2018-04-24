import numpy as np
from strtens import StructureTensor
from strtens.util import imread, make_ODF, colormap
from mayavi import mlab

print('Reading image')
im = imread('../../../data/xray/recon_2x_stack-1.tif')

d = 1
N = 3

print('Calculating structure tensor')
AI, vectors = StructureTensor(im,
                              d_sigma=d,
                              n_sigma=N).results()


def plot_ODF(x, y, z, s, colors, fignum=1):
    fig = mlab.figure(fignum,
                      bgcolor=(1, 1, 1),
                      fgcolor=(0, 0, 0),
                      size=(1920, 1080))
    ODF = mlab.mesh(x, y, z, scalars=s)
    ODF.module_manager.scalar_lut_manager.lut.table = colors
    mlab.outline()
    mlab.orientation_axes()
    return fig


n = 800
print('Making First ODF')
mlab.close(all=True)
x, y, z = make_ODF(n, vectors)
colors, s = colormap(x, y, z)
fig = plot_ODF(x, y, z, s, colors, fignum=1)
mlab.savefig('../figs/ODF_full_d{}n{}_view1.png'.format(d, N))

print('Making next ODF')
mlab.close(all=True)
mask = np.where(AI <= AI.mean(), False, True)
masked_vectors = vectors * np.expand_dims(mask, -1)
x, y, z = make_ODF(n, masked_vectors)
colors, s = colormap(x, y, z)
fig2 = plot_ODF(x, y, z, s, colors, fignum=2)
mlab.savefig('../figs/ODF_masked_d{}n{}_view1.png'.format(d, N))
