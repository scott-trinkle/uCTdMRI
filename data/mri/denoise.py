'''
This script imports the raw dMRI data and denoises it using
local PCA. 
'''
import nibabel as nib
from dipy.io import read_bvals_bvecs
from dipy.core.gradients import gradient_table
from dipy.denoise.localpca import localpca
from dipy.denoise.pca_noise_estimate import pca_noise_estimate

# Load data
print('Loading data')
img = nib.load('raw_data.nii.gz')
data = img.get_data()
bvals, bvecs = read_bvals_bvecs('bvals', 'bvecs')
gtab = gradient_table(bvals, bvecs, b0_threshold=30)  # b0 is actually 26?

# Denoise using PCA
print('Denoising using Local PCA')
affine = img.affine
print('Estimating sigma')
sigma = pca_noise_estimate(data, gtab, correct_bias=True, smooth=2)
print('Denoising')
denoised_arr = localpca(data, sigma=sigma, patch_radius=2)
nib.save(nib.Nifti1Image(denoised_arr, affine),
         'denoised_localpca.nii.gz')
