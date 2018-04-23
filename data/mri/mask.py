'''
This script imports the denoised dMRI data and thresholds the brain
using a median otsu method, and saves the masked result and the binary mask.
'''
import numpy as np
import nibabel as nib
from dipy.segment.mask import median_otsu

# Load data
img = nib.load('denoised_localpca.nii.gz')
data = img.get_data()
affine = img.affine

# Segment brain
print('Segmenting brain')
data_masked, mask = median_otsu(data, 1, 1, dilate=2)
nib.save(nib.Nifti1Image(data_masked, affine),
         'raw_data_masked.nii.gz')
nib.save(nib.Nifti1Image(mask.astype(np.float32), affine),
         'raw_data_binary_mask.nii.gz')
