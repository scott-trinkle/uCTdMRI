angle = 85
run("Reslice [/]...", "output=1.000 start=Top avoid");
run("Size...", "width=250 height=250 depth=250 interpolation=None");
run("Rotate... ", "angle=angle grid=1 interpolation=None stack");
makeRectangle(61, 54, 132, 126);
run("Specify...", "width=125 height=125 x=62.5 y=62.5 slice=15");
run("Crop");
run("Size...", "width=125 height=125 depth=125 interpolation=None");
run("Reslice [/]...", "output=1.000 start=Top avoid");
selectWindow("Reslice of z_base_mask_nfib16_r8");
close();
saveAs("Tiff", "/Users/scotttrinkle/GoogleDrive/Current/uCTdMRI/notes/2018-05-22-tuning-parameters/phantoms/crossing_fibers/masks/z_phantom_mask_nfib9x4_r8_85deg.tif");