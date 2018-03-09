import numpy as np
from skimage import io
import st_tools as st
from mayavi import mlab as m

commissure = io.imread('data/anterior_commissure_8x_sub_sample.tif')
im = commissure
im = commissure[0:23, 46:121, 39:245]
im = np.moveaxis(im, [0, 2], [2, 0])  # getting in shape (x,y,z)

print('Running STA...')
FA, vects = st.st_3D(im, 2)

u, v, w = st.make_comps(vects, im)

bit = 50
s = bit**2 * u + bit * v + w

print('Plotting...')
m.figure()
field = m.quiver3d(u, v, w,
                   scalars=s,
                   line_width=1.5,
                   scale_factor=0.5,
                   colormap='jet')

field.glyph.color_mode = 'color_by_scalar'
field.glyph.glyph_source.glyph_source.center = [0, 0, 0]
m.colorbar()
m.orientation_axes()
