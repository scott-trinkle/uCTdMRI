# import the simple module from the paraview
from paraview.simple import *
# disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get active source.
vector_fieldvtu = GetActiveSource()

# set active source
SetActiveSource(vector_fieldvtu)

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1939, 1124]

# show data in view
vector_fieldvtuDisplay = Show(vector_fieldvtu, renderView1)

# trace defaults for the display properties.
vector_fieldvtuDisplay.Representation = 'Surface'
vector_fieldvtuDisplay.ColorArrayName = [None, '']
vector_fieldvtuDisplay.OSPRayScaleArray = 'FA'
vector_fieldvtuDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
vector_fieldvtuDisplay.SelectOrientationVectors = 'FA'
vector_fieldvtuDisplay.ScaleFactor = 7.300000000000001
vector_fieldvtuDisplay.SelectScaleArray = 'FA'
vector_fieldvtuDisplay.GlyphType = 'Arrow'
vector_fieldvtuDisplay.GlyphTableIndexArray = 'FA'
vector_fieldvtuDisplay.DataAxesGrid = 'GridAxesRepresentation'
vector_fieldvtuDisplay.PolarAxes = 'PolarAxesRepresentation'
vector_fieldvtuDisplay.ScalarOpacityUnitDistance = 3.34270181164882
vector_fieldvtuDisplay.GaussianRadius = 3.6500000000000004
vector_fieldvtuDisplay.SetScaleArray = ['POINTS', 'FA']
vector_fieldvtuDisplay.ScaleTransferFunction = 'PiecewiseFunction'
vector_fieldvtuDisplay.OpacityArray = ['POINTS', 'FA']
vector_fieldvtuDisplay.OpacityTransferFunction = 'PiecewiseFunction'

# reset view to fit data
renderView1.ResetCamera()

# change representation type
vector_fieldvtuDisplay.SetRepresentationType('3D Glyphs')

# Properties modified on vector_fieldvtuDisplay
vector_fieldvtuDisplay.SelectOrientationVectors = 'uvw'

# Properties modified on vector_fieldvtuDisplay
vector_fieldvtuDisplay.Orient = 1

# Properties modified on vector_fieldvtuDisplay
vector_fieldvtuDisplay.ScaleMode = 'Magnitude'

# Properties modified on vector_fieldvtuDisplay
vector_fieldvtuDisplay.SelectScaleArray = 'uvw'

# Properties modified on vector_fieldvtuDisplay
vector_fieldvtuDisplay.ScaleFactor = 1.0

# Properties modified on vector_fieldvtuDisplay
vector_fieldvtuDisplay.Scaling = 1

# set scalar coloring
ColorBy(vector_fieldvtuDisplay, ('POINTS', 'rgb', 'Magnitude'))

# rescale color and/or opacity maps used to include current data range
vector_fieldvtuDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
vector_fieldvtuDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'rgb'
rgbLUT = GetColorTransferFunction('rgb')
rgbLUT.RGBPoints = [83.84509526501833, 0.231373, 0.298039, 0.752941, 219.10747927174307,
                    0.865003, 0.865003, 0.865003, 354.36986327846785, 0.705882, 0.0156863, 0.14902]
rgbLUT.ScalarRangeInitialized = 1.0

# Properties modified on vector_fieldvtuDisplay
vector_fieldvtuDisplay.MapScalars = 0

# hide color bar/color legend
vector_fieldvtuDisplay.SetScalarBarVisibility(renderView1, False)

# saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [81.59306415074786,
                              137.46499235364047, -139.53255248888263]
renderView1.CameraFocalPoint = [29.5, 36.5, 2.0]
renderView1.CameraViewUp = [-0.6214790978394182, -
                            0.5113565356242468, -0.5935303062380819]
renderView1.CameraParallelScale = 46.97339672623218

# uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
