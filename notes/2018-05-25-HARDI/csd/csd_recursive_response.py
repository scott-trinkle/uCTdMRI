import numpy as np
import nibabel as nib
import multiprocessing
from dipy.io import read_bvals_bvecs
from dipy.core.gradients import gradient_table
from dipy.reconst.csdeconv import (
    recursive_response, ConstrainedSphericalDeconvModel)
from dipy.reconst.dti import (
    TensorModel, fractional_anisotropy, mean_diffusivity)
from dipy.data import get_sphere
from dipy.direction import peaks_from_model

datapath = '../../../data/mri/'

print('Loading data')
img = nib.load(datapath + 'raw_data_masked.nii.gz')
data = img.get_data()
mask = nib.load(datapath + 'raw_data_binary_mask.nii.gz').get_data()
bvals, bvecs = read_bvals_bvecs(datapath + 'bvals', datapath + 'bvecs')
gtab = gradient_table(bvals, bvecs, b0_threshold=30)  # b0 is actually 26?


# Get fiber response function with recursive algorithm:
print('Getting response function')

# Shorten computation time with a WM mask from DTI
tenmodel = TensorModel(gtab)
tenfit = tenmodel.fit(data, mask=mask)
FA = fractional_anisotropy(tenfit.evals)
MD = mean_diffusivity(tenfit.evals)
wm_mask = (np.logical_or(FA >= 0.4, (np.logical_and(FA >= 0.15, MD >= 0.0011))))

rec_response = recursive_response(gtab, data, mask=wm_mask, sh_order=6,
                                  peak_thr=0.01, init_fa=0.08,
                                  init_trace=0.0021, iter=16, convergence=0.001,
                                  parallel=True)


# Fit data to csd model
print('Fitting to csd model')
sphere = get_sphere('symmetric724')
csd_model = ConstrainedSphericalDeconvModel(gtab, rec_response, sh_order=6)


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


np.save('results/recursive_shm_coeff', csd_fit.shm_coeff)
np.save('results/recursive_odf', csd_fit.odf)
np.save('results/recursive_peak_directions', csd_fit.peak_dirs)
np.save('results/recursive_peak_values', csd_fit.peak_values)
np.save('results/recursive_peak_indices', csd_fit.peak_indices)
