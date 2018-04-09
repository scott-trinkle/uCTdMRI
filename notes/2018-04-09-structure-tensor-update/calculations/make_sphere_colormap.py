from strtens.util import make_sphere, colormap
from mayavi import mlab

n = 500
x, y, z, T, P = make_sphere(n)

colors, s = colormap(x, y, z)

fig = mlab.figure(1,
                  bgcolor=(1, 1, 1),
                  fgcolor=(0, 0, 0),
                  size=(800, 700))
sphere = mlab.mesh(x, y, z, scalars=s)
sphere.module_manager.scalar_lut_manager.lut.table = colors
mlab.orientation_axes()
mlab.outline()
# mlab.savefig('../figs/colormap_sphere.png')
