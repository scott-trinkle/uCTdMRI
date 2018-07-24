import numpy as np
from strtens import odftools
from dipy.viz import window, actor
from dipy.data import get_sphere

sphere = get_sphere('symmetric724')
names = ['AC1', 'AC2', 'CB1', 'CC1', 'CC2', 'CC3', 'UK1']
hardi_names = ['CSD', 'DTI', 'SF']

inds = {'AC1': [2, 5, 6, 9],
        'AC2': [4, 7, 2, 5],
        'CB1': [4, 7, 6, 9],
        'CC1': [6, 9, 3, 6],
        'CC2': [7, 10, 3, 6],
        'CC3': [6, 9, 3, 6],
        'UK1': [6, 9, 1, 4]}


for name in names:
    print(name)
    x1, x2, y1, y2 = inds[name]
    for i, hardi_name in enumerate(hardi_names):
        print(hardi_name)

        odf = np.load('./hardi_odfs/{}_{}.npy'.format(name, hardi_name)
                      ).reshape((10, 10, 1, 724))

        odf = odf[x1:x2, y1:y2]

        ren = window.Renderer()
        ren.SetBackground(255, 255, 255)
        ren.add(actor.odf_slicer(odf, sphere=sphere, scale=0.4))
        ren.set_camera(position=(1, 1, 5.5),
                       focal_point=(1, 1, 0),
                       view_up=(0, 11, 0))
        # window.show(ren, reset_camera=True)
        window.snapshot(
            ren, fname='hardi_FOD_plots/{}_{}.png'.format(name, hardi_name), size=(5000, 5000))
