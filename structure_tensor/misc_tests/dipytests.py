import numpy as np
import nibabel as nib
import dipy.reconst.dti as dti

print()
print('Reading Data')
from dipy.data import read_stanford_hardi
img, gtab = read_stanford_hardi()
data = img.get_data()

print('Masking')
from dipy.segment.mask import median_otsu
maskdata, mask = median_otsu(data, 3, 1, True,
                             vol_idx=range(10, 50), dilate=2)

print('Fitting tensor')
tenmodel = dti.TensorModel(gtab)
tenfit = tenmodel.fit(maskdata)

# print('Calculating FA')
# FA = dti.fractional_anisotropy(tenfit.evals)
# FA[np.isnan(FA)] = 0
# FA = np.clip(FA, 0, 1)
# RGB = dti.color_fa(FA, tenfit.evecs)

# print('Getting sphere')
# from dipy.data import get_sphere
# sphere = get_sphere('symmetric724')

# print('Loading vtk')
# from dipy.viz import fvtk
# ren = fvtk.ren()

# print('Prepping CFA')
# evals = tenfit.evals[13:43, 44:74, 28:29]
# evecs = tenfit.evecs[13:43, 44:74, 28:29]

# cfa = RGB[13:43, 44:74, 28:29]
# cfa /= cfa.max()

# print('Plotting ellipsoids')
# fvtk.add(ren, fvtk.tensor(evals, evecs, cfa, sphere))
# print('Saving ellipsoids')
# fvtk.record(ren, n_frames=1, out_path='tensor_ellipsoids.png', size=(600, 600))
# fvtk.clear(ren)

# print('Calculating ODFs')
# tensor_odfs = tenmodel.fit(data[20:50, 55:85, 38:39]).odf(sphere)

# print('Plotting odfs')
# fvtk.add(ren, fvtk.sphere_funcs(tensor_odfs, sphere, colormap=None))
# print('Saving odfs')
# fvtk.record(ren, n_frames=1, out_path='tensor_odfs.png', size=(600, 600))
