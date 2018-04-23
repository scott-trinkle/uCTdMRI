'''
This script reconstructs the fODF from a sample slice using CSD, with
a fiber response function automatically generated from a center ROI in the
image.

Check out warning about number of parameters for the fit more than the
actual data points.

^this warning is generated after calling ConstrainedSphericalDeconvModel

csd_odf.shape = (66, 101, 1, 724)
724 comes from number of sphere vertices
(generating sphere with 'symmetric724' argument)
'''
import numpy as np
import nibabel as nib
import multiprocessing
from dipy.io import read_bvals_bvecs
from dipy.core.gradients import gradient_table
from dipy.reconst.csdeconv import auto_response
from dipy.viz import fvtk
from dipy.data import get_sphere
from dipy.sims.voxel import single_tensor_odf
from dipy.reconst.csdeconv import ConstrainedSphericalDeconvModel
from dipy.direction import peaks_from_model

print('Loading processed data')
img = nib.load('../data/mri/raw_data_masked.nii.gz')
data = img.get_data()
mask = nib.load('../data/mri/raw_data_binary_mask.nii.gz').get_data()
bvals, bvecs = read_bvals_bvecs('../data/mri/bvals', '../data/mri/bvecs')
gtab = gradient_table(bvals, bvecs, b0_threshold=30,
                      atol=0.01)  # b0 is actually 26?


# Getting fiber response function from center of brain (CC?)
response, ratio = auto_response(gtab, data, roi_radius=10, fa_thr=0.7)
if response[0][1] != response[0][2] or (ratio > 0.25):
    print('Might want to find a different response function')

# Visualize response function:
ren = fvtk.ren()
evals = response[0]
evecs = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]]).T
sphere = get_sphere('symmetric724')
response_odf = single_tensor_odf(sphere.vertices, evals, evecs)
# response_actor = fvtk.sphere_funcs(response_odf, sphere)
# fvtk.add(ren, response_actor)
# print('Saving response ODF')
# fvtk.record(ren, out_path='results/csd_response.png', size=(200, 200))
# fvtk.rm(ren, response_actor)
# Looks good!

# Work with a sample at first
# data_small = data[:, 45:146, 17:18]
# mask_small = mask[:, 45:146, 17:18]
# data_small = data[30:34, 45:60, 17:18]
# mask_small = mask[30:34, 45:60, 17:18]
data_small = data[30:32, 45:60, 17:18]
mask_small = mask[30:32, 45:60, 17:18]

# Running CSD
print('Creating model')
csd_model = ConstrainedSphericalDeconvModel(gtab, response)
print('Fitting model')
csd_peaks = peaks_from_model(model=csd_model,
                             data=data_small,
                             sphere=sphere,
                             relative_peak_threshold=0.5,
                             min_separation_angle=25,
                             mask=mask_small,
                             return_sh=True,
                             return_odf=True,
                             normalize_peaks=True,
                             npeaks=5,
                             parallel=True,
                             nbr_processes=None)
print('Getting odfs')
csd_odf = csd_peaks.odf
print('Adding to fvtk')
fodf_spheres = fvtk.sphere_funcs(csd_odf, sphere, scale=1.3, norm=False)
fodf_peaks = fvtk.peaks(csd_peaks.peak_dirs, csd_peaks.peak_values, scale=1.3)
# fvtk.add(ren, fodf_spheres)
fvtk.add(ren, fodf_peaks)
fvtk.show(ren)
# print('Saving as csd_odfs.png')
# fvtk.record(ren, out_path='results/csd_odfs.png', size=(1200, 1200))
# fvtk.rm(ren, fodf_spheres)
