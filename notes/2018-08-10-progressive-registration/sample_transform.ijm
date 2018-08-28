res=15
w=666;
h=466;
d=1233;
vox_size = res / 1000;


//run("NIfTI-Analyze", "open=/home/trinkle/Research/uCTdMRI/notes/2018-08-10-progressive-registration/registrations/reg_50um/reg_50um1Warp.nii.gz");

interp='no_interp';
Interp='None';
run("Duplicate...", "title=sampled_"+interp+"_"+res+"1Warp.nii.gz duplicate");
run("Size...", "width="+w+" height="+h+" depth="+d+" constrain average interpolation="+Interp);
run("Properties...", "channels=3 slices=d frames=1 unit=mm pixel_width=vox_size pixel_height=vox_size voxel_depth=vox_size");
run("NIfTI-1", "save=/home/trinkle/Research/uCTdMRI/notes/2018-08-10-progressive-registration/registrations/"+interp+"_"+res+"/sampled_"+interp+"_"+res+"1Warp.nii");
close();

interp='bicubic';
Interp='Bicubic';
run("Duplicate...", "title=sampled_"+interp+"_"+res+"1Warp.nii.gz duplicate");
run("Size...", "width="+w+" height="+h+" depth="+d+" constrain average interpolation="+Interp);
run("Properties...", "channels=3 slices="+d+" frames=1 unit=mm pixel_width=vox_size pixel_height=vox_size voxel_depth=vox_size");
run("NIfTI-1", "save=/home/trinkle/Research/uCTdMRI/notes/2018-08-10-progressive-registration/registrations/"+interp+"_"+res+"/sampled_"+interp+"_"+res+"1Warp.nii");
close();

interp='bilinear';
Interp='Bilinear';
run("Duplicate...", "title=sampled_"+interp+"_"+res+"1Warp.nii.gz duplicate");
run("Size...", "width="+w+" height="+h+" depth="+d+" constrain average interpolation="+Interp);
run("Properties...", "channels=3 slices=d frames=1 unit=mm pixel_width=vox_size pixel_height=vox_size voxel_depth=vox_size");
run("NIfTI-1", "save=/home/trinkle/Research/uCTdMRI/notes/2018-08-10-progressive-registration/registrations/"+interp+"_"+res+"/sampled_"+interp+"_"+res+"1Warp.nii");
