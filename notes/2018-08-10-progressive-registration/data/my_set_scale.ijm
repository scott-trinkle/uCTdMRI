vox_id=150
vox_size = vox_id / 1000 // mm
slices=106

selectWindow("recon_" + vox_id + "um.nii");
run("Properties...", "channels=1 slices="+slices+" frames=1 unit=mm pixel_width=" + vox_size + " pixel_height="+vox_size+" voxel_depth="+vox_size+" global");

selectWindow("mri_"+vox_id+"um_bilinear.nii");
run("NIfTI-1", "save=/Users/scotttrinkle/GoogleDrive/Current/uCTdMRI/notes/2018-08-10-progressive-registration/data/mri_"+vox_id+"um_bilinear.nii");
close();

selectWindow("mri_"+vox_id+"um_bicubic.nii");
run("NIfTI-1", "save=/Users/scotttrinkle/GoogleDrive/Current/uCTdMRI/notes/2018-08-10-progressive-registration/data/mri_"+vox_id+"um_bicubic.nii");
close();

selectWindow("mri_"+vox_id+"um_no_interp.nii");
run("NIfTI-1", "save=/Users/scotttrinkle/GoogleDrive/Current/uCTdMRI/notes/2018-08-10-progressive-registration/data/mri_"+vox_id+"um_no_interp.nii");
close();

selectWindow("recon_" + vox_id + "um.nii");
run("NIfTI-1", "save=/Users/scotttrinkle/GoogleDrive/Current/uCTdMRI/notes/2018-08-10-progressive-registration/data/recon_"+vox_id+"um.nii");
close();