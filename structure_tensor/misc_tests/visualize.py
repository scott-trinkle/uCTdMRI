import numpy as np
from skimage import io
import st_tools as st
# from mayavi import mlab as m


commissure = io.imread(
    '../data/anterior_commissure/anterior_commissure_8x_sub_sample.tif')
#im = commissure
# im = commissure[0:23, 46:121, 39:245]
im = commissure[0:30, 75:100, 30:100]
im = np.moveaxis(im, [0, 2], [2, 0])  # getting in shape (x,y,z)

print('Running STA...')
FA, vects = st.st_3D(im,
                     d_sigma=1,
                     n_sigma=2)

x_ind, y_ind, z_ind = im.shape
x, y, z = np.mgrid[0:x_ind, 0:y_ind, 0:z_ind]
u, v, w = st.make_comps(vects, im, reorient=True)


def toRGB(a):
    scaled = a - a.min()
    scaled = scaled / scaled.max() * 255
    return scaled.astype(np.uint8)


r = toRGB(u)
g = toRGB(v)
b = toRGB(w)


print('Saving')
from pyevtk.hl import pointsToVTK
pointsToVTK('results/anterior_commissure_sub_sample',
            x.astype('float'), y.astype('float'), z.astype('float'),
            data={'uvw': (u, v, w), 'FA': FA, 'rgb': (r, g, b)})


# print('Plotting...')

# m.figure()
# field = m.quiver3d(x, y, z, u, v, w,
#                    scalars=s,
#                    line_width=2.0,
#                    scale_factor=0.5,
#                    colormap='jet')

# field.glyph.color_mode = 'color_by_scalar'
# field.glyph.glyph_source.glyph_source.center = [0, 0, 0]
# m.colorbar()
# m.orientation_axes()
