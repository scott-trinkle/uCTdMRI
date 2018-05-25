import numpy as np
import nibabel as nib
import multiprocessing
from dipy.io import read_bvals_bvecs
from dipy.core.gradients import gradient_table
from dipy.reconst.csdeconv import (
    auto_response, ConstrainedSphericalDeconvModel)
from dipy.data import get_sphere
from dipy.direction import peaks_from_model

datapath = '../../../data/mri/'

img = nib.load(datapath + 'raw_data_masked.nii.gz')
data = img.get_data()
mask = nib.load(datapath + 'raw_data_binary_mask.nii.gz').get_data()
bvals, bvecs = read_bvals_bvecs(datapath + 'bvals', datapath + 'bvecs')
gtab = gradient_table(bvals, bvecs, b0_threshold=30)  # b0 is actually 26?


# Getting fiber response function from center of brain
auto_response, ratio = auto_response(gtab, data, roi_radius=10, fa_thr=0.7)
if auto_response[0][1] != auto_response[0][2] or (ratio > 0.25):
    raise ValueError('Might want to find a different response function')


# Fit data to csd model
sphere = get_sphere('symmetric724')
csd_model = ConstrainedSphericalDeconvModel(gtab, auto_response, sh_order=6)

# Calculate odf and peaks
csd_fit = peaks_from_model(model=csd_model,
                           data=data,
                           mask=mask,
                           return_odf=True,
                           sh_order=6,
                           sphere=sphere,
                           relative_peak_threshold=0.2,
                           min_separation_angle=25,
                           parallel=True)


np.save('results/auto_shm_coeff', csd_fit.shm_coeff)
np.save('results/auto_odf', csd_fit.odf)
np.save('results/auto_peak_directions', csd_fit.peak_dirs)
np.save('results/auto_peak_values', csd_fit.peak_values)
np.save('results/auto_peak_indices', csd_fit.peak_indices)
