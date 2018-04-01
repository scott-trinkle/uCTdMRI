import numpy as np

x, y, z = np.mgrid[-2:3, -2:3, -2:3]

r = np.sqrt(x ** 2 + y ** 2 + z ** 4)
xy = np.sqrt(x**2 + y**2)
# u = y * np.sin(r) / (r + 0.001)
# v = -x * np.sin(r) / (r + 0.001)
# w = np.zeros_like(z)

sinphi = xy / (r + 0.0000001)
cosphi = z / (r + 0.0000001)
costhet = x / (xy + 0.0000001)
sinthet = y / (xy + 0.0000001)

u = r * sinphi * costhet
v = r * sinphi * sinthet
w = r * cosphi

norm = np.sqrt(u**2 + v**2 + w**2)
u = np.where(norm != 0, u / norm, np.zeros_like(u))
v = np.where(norm != 0, v / norm, np.zeros_like(v))
w = np.where(norm != 0, w / norm, np.zeros_like(w))

cond = (w < 0) | ((w == 0) & (v < 0)) | ((w == 0) & (v == 0) & (u < 0))

u = np.where(cond, -1 * u, u)
v = np.where(cond, -1 * v, v)
w = np.where(cond, -1 * w, w)


def toRGB(a):
    scaled = a - a.min()
    scaled = scaled / scaled.max() * 255
    return scaled.astype(np.uint8)


r = toRGB(u)
g = toRGB(v)
b = toRGB(w)


from pyevtk.hl import pointsToVTK
pointsToVTK('quiver',
            x.astype('float'), y.astype('float'), z.astype('float'),
            data={'uvw': (u, v, w), 'rgb': (r, g, b)})


# from paraview.simple import *

# # paraview.simple._DisableFirstRenderCameraReset()

# # Create a new 'Render View'
# view = CreateView('RenderView')
# view.ViewSize = [1000, 700]
# view.AnnotationColor = [0.0, 0.0, 0.0]
# view.AxesGrid = 'GridAxes3DActor'
# view.OrientationAxesVisibility = 0
# view.OrientationAxesLabelColor = [0.0, 0.0, 0.0]
# view.OrientationAxesOutlineColor = [0.0, 0.0, 0.0]
# view.CenterOfRotation = [43.5, 49.5, 19.5]
# view.StereoType = 0
# view.CameraPosition = [-92.82, -99.84, 104.75]
# view.CameraFocalPoint = [43.5, 49.5, 19.5]
# view.CameraViewUp = [0.36, 0.18, 0.91]
# view.CameraParallelScale = 68.72
# view.Background = [1.0, 1.0, 1.0]

# # Create a new 'XML Unstructured Grid Reader'
# data = XMLUnstructuredGridReader(FileName=['test.vtu'])
# data.PointArrayStatus = ['FA', 'uvw', 's']

# # Show data from data
# dataDisplay = Show(data, view)

# # Glyph settings
# dataDisplay.Representation = '3D Glyphs'
# dataDisplay.DiffuseColor = [0.66, 0.0, 0.0]
# dataDisplay.GlyphType = 'Arrow'
# dataDisplay.ScaleFactor = 1.0
# dataDisplay.GlyphType.TipResolution = 1
# dataDisplay.GlyphType.TipRadius = 0.0
# dataDisplay.GlyphType.TipLength = 0.0
# dataDisplay.GlyphType.ShaftResolution = 32
# dataDisplay.GlyphType.ShaftRadius = 0.1
# dataDisplay.Orient = 1
# dataDisplay.SelectOrientationVectors = 'uvw'
# dataDisplay.Scaling = 1
# dataDisplay.ScaleMode = 'Magnitude'
# dataDisplay.SelectScaleArray = 'uvw'


# # Outline
# data_1 = XMLUnstructuredGridReader(FileName=['test.vtu'])
# data_1.PointArrayStatus = ['FA', 'uvw', 's']
# data_1Display = Show(data_1, view)
# data_1Display.Representation = 'Outline'
# data_1Display.AmbientColor = [0.0, 0.0, 0.0]
# Render()

# test = raw_input('Enter any key to quit: ')
