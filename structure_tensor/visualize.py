import numpy as np
from skimage import io
import st_tools as st
from mayavi import mlab


commissure = io.imread('data/anterior_commissure_8x_sub_sample.tif')
im = commissure
im = commissure[0:23, 46:121, 39:245]
# im = io.imread('data/artificial-fibers.tif')


print('Running STA...')
FA, vects = st.st_3D(im, 2)

print('Importing mlab...')
from mayavi import mlab as m

u, v, w = st.make_comps(vects, im)

bit = 50
s = bit**2 * u.T + bit * v.T + w.T

print('Plotting...')
m.figure()
field = m.quiver3d(u.T, v.T, w.T, scalars=s, line_width=1.5, scale_factor=0.5,
                   colormap='jet')
field.glyph.color_mode = 'color_by_scalar'
field.glyph.glyph_source.glyph_source.center = [0, 0, 0]
m.orientation_axes()
