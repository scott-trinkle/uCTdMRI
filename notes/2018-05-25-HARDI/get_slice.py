import numpy as np
from dipy.viz import window, actor
from dipy.data import get_sphere

fns = ['csd/results/auto_odf.npy',
       './dti/results/dti_odf.npy',
       './qball/results/qball_odf.npy',
       './sf/results/sf_odf.npy']
odfs = np.load(fn)

odfs = odfs[:, :, 23:24, :]
np.save('csd_slice_23', odfs)
