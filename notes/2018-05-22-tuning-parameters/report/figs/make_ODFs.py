import numpy as np
from strtens.vis import show_ODF
from strtens import odftools
from dipy.viz import window, actor

deg45_c = np.load(
    '../../phantoms/crossing_fibers/true_coeffs/z_phantom_nfib9x4_r8_45deg_coeffs.npy')
r8_c = np.load(
    '../../phantoms/different_size/true_coeffs/x_phantom_nfib9_r8_coeffs.npy')

sphere = odftools.make_sphere(1500)
deg45_odf = odftools.get_odf(deg45_c, sphere)
r8_odf = odftools.get_odf(r8_c, sphere)

interactive = True
save = False

ren45 = window.Renderer()
ren45 = show_ODF(deg45_odf, sphere, interactive=interactive, ren=ren45,
                 save=save, fn='deg45_ODF.png')

camera = ren45.GetActiveCamera()
camera.SetUseExplicitProjectionTransformMatrix(False)
# camera.SetViewAngle(10.)
# camera.SetPosition(10, 10, 10)
# ren45.SetActiveCamera(camera)
# window.show(ren45)


ren8 = window.Renderer()
ren8 = show_ODF(r8_odf, sphere, interactive=interactive,
                ren=ren8, save=save, fn='r8_ODF.png')
ren8.SetActiveCamera(camera)
window.show(ren8)
