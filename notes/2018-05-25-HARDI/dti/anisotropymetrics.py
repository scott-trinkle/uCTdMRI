import numpy as np
import nibabel as nib
import dipy.reconst.dti as dti
from dipy.data import get_sphere
from dipy.viz import window, actor
from strtens.hardi import get_data
from strtens.util import imsave

# Load data
datapath = '../../../data/mri/'
img, data, mask, gtab = get_data(datapath)

# Fit tensor
tenmodel = dti.TensorModel(gtab)
tenfit = tenmodel.fit(data)

# Compute anisotropy measures
FA = dti.fractional_anisotropy(tenfit.evals)  # Fractional anisotropy
FA[np.isnan(FA)] = 0
MD = tenfit.md  # Mean diffusivity

# FA/RGB-map
FA = np.clip(FA, 0, 1)
RGB = dti.color_fa(FA, tenfit.evecs)
imsave('fa_rgb.tif', np.moveaxis(RGB, [0, 2], [2, 0]), rgb=True)
nib.save(nib.Nifti1Image(np.array(255 * RGB, 'uint8'),
                         img.affine), 'tensor_rgb.nii.gz')

# Visualize color ellipsoids
evals = tenfit.evals[25:42, 100:116, 20:21]
evecs = tenfit.evecs[25:42, 100:116, 20:21]
cfa = RGB[25:42, 100:116, 20:21]
cfa /= cfa.max()

sphere = get_sphere('symmetric724')
ren = window.Renderer()
ren.add(actor.tensor_slicer(evals, evecs,
                            scalar_colors=cfa, sphere=sphere, scale=0.3))
window.show(ren)
window.clear(ren)
