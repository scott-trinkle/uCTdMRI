from strtens.util import make_sphere, make_rgb
import numpy as np
from mayavi import mlab

n = 500
x, y, z, T, P = make_sphere(n)

colors = np.zeros((n**2, 4)).astype(np.uint8)
colors[:, 0] = make_rgb(x.flatten())
colors[:, 1] = make_rgb(y.flatten())
colors[:, 2] = make_rgb(z.flatten())
colors[:, 3] = 255

s = np.arange(x.flatten().size).reshape(x.shape)
fig = mlab.figure(1,
                  bgcolor=(1, 1, 1),
                  fgcolor=(0, 0, 0),
                  size=(800, 700))
sphere = mlab.mesh(x, y, z, scalars=s)
sphere.module_manager.scalar_lut_manager.lut.table = colors
mlab.orientation_axes()
mlab.outline()
mlab.savefig('../figs/colormap_sphere.png')
