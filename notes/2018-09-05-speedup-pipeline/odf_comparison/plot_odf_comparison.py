import numpy as np
from strtens.vis import show_ODF
from strtens import odftools
from dipy.data import Sphere

sphere = odftools.make_sphere(4000)

print('Loading data')
vectors = np.load('../data/sample_8_8_vectors.npy').reshape((-1, 3))
c_true = np.load('../data/sample_8_8_coeffs.npy')

print('Making hist')
hist = odftools.make_hist(vectors, sphere)

print('Making even hist')
new_points = []
new_odf = []
for point, val in zip(sphere.vertices, hist):
    new_points.append(point)
    new_odf.append(val)
    new_points.append(-point)
    new_odf.append(val)
new_sphere = Sphere(xyz=np.array(new_points))
new_odf = np.array(new_odf).astype('float')

print('Saving hist odfs')
show_ODF(hist.astype('float'), sphere, save=True, interactive=False,
         fn='raw_odf.png')
show_ODF(new_odf, new_sphere, save=True, interactive=False,
         fn='raw_odf_even.png')

print('Calculating hist coeffs')
c_hist = odftools.get_SH_coeffs(20, vectors, sphere)
odf_hist = odftools.get_odf(c_hist, sphere)

print('Saving hist SH odfs')
show_ODF(odf_hist, sphere, save=True, interactive=False,
         fn='hist_odf_sh.png')

print('Saving delta SH odf')
delta_odf = odftools.get_odf(c_true, sphere)
show_ODF(delta_odf, sphere, save=True, interactive=False,
         fn='delta_odf_sh.png')
