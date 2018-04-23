import numpy as np
import nibabel as nib
from dipy.segment.mask import median_otsu

img = nib.load('xray_150um.nii.gz')
data = np.squeeze(img.get_data())

b0_mask, mask = median_otsu(data, 1, 1, dilate=1)

mask_img = nib.Nifti1Image(mask.astype(np.float32), img.affine)
b0_img = nib.Nifti1Image(b0_mask.astype(np.float32), img.affine)
fname = 'xray_150um'
nib.save(mask_img, fname + '_binary_mask.nii.gz')
nib.save(b0_img, fname + '_masked.nii.gz')

# Also, median_otsu can crop outputs to remove background voxels
# b0_mask_crop, mask_crop = median_otsu(data, 4, 4, autocrop=True)
# mask_img_crop = nib.Nifti1Image(mask_crop.astype(np.float32), img.affine)
# b0_img_crop = nib.Nifti1Image(
#     b0_mask_crop.astype(np.float32), img.affine)
# nib.save(mask_img_crop, fname + '_binary_mask_crop.nii.gz')
# nib.save(b0_img_crop, fname + '_mask_crop.nii.gz')
