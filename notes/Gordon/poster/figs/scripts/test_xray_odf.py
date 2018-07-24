import numpy as np
from strtens import odftools
from dipy.viz import window, actor

sphere = odftools.make_sphere(8000)
c = np.load('../../../../scratch/demo/c1.npy')
odf = odftools.get_odf(c, sphere)[None, None, None, :]

ren = window.Renderer()
ren.SetBackground(255, 255, 255)
ren.add(actor.odf_slicer(odf, sphere=sphere))
ren.set_camera(position=(0, 0, -8),
               focal_point=(0, 0, 0),
               view_up=(0, -1, 0))
window.snapshot(ren, fname='sample_data_1_odf.png', size=(5000, 5000))
