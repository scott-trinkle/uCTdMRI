import numpy as np
from strtens import odftools
from dipy.viz import window, actor

n = 8000
sphere = odftools.make_sphere(n)
names = ['AC1', 'AC2', 'AC3', 'CB1', 'CB2', 'CC1', 'CC2', 'CC3', 'CC4', 'UK1']
for name in names:
    print(name)
    odfs = np.zeros((9, 1, n))
    cs = []
    for i in range(9):
        print(i)
        c = np.load('coeffs/' + name + '-{}_coeffs.npy'.format(i + 1))
        odfs[i, 0, :] = odftools.get_odf(c, sphere)
        cs.append(c)

    odfs = odfs.reshape((3, 3, 1, n))

    print('Displaying')
    ren = window.Renderer()
    ren.SetBackground(255, 255, 255)
    ren.add(actor.odf_slicer(odfs, sphere=sphere, scale=0.4))
    ren.set_camera(position=(0, 0, -5.5),
                   focal_point=(1, 1, 0),
                   view_up=(0, -1, 0))
    if name in ['CC2', 'CC3']:
        ren.set_camera(position=(0, 0, -5.85),
                       focal_point=(1, 1, 0),
                       view_up=(0, -1, 0))

    # window.show(ren, reset_camera=False)
    window.snapshot(ren, fname='FODs/FOD_' + name + '.png', size=(5000, 5000))
