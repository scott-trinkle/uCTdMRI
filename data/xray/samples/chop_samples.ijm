id = "UK1"
name = id + ".tif"
selectWindow(name);
makeRectangle(20, 19, 68, 66);

run("Specify...", "width=63 height=63 x=0 y=0 slice=0");
run("Duplicate...", "duplicate");
saveAs("Tiff", "/Users/scotttrinkle/GoogleDrive/Current/uCTdMRI/data/xray/samples/" + id + "-1.tif");
close();

selectWindow(name);
run("Specify...", "width=63 height=63 x=63 y=0 slice=0");
run("Duplicate...", "duplicate");
saveAs("Tiff", "/Users/scotttrinkle/GoogleDrive/Current/uCTdMRI/data/xray/samples/" + id + "-2.tif");
close();

selectWindow(name);
run("Specify...", "width=63 height=63 x=126 y=0 slice=0");
run("Duplicate...", "duplicate");
saveAs("Tiff", "/Users/scotttrinkle/GoogleDrive/Current/uCTdMRI/data/xray/samples/" + id + "-3.tif");
close();

selectWindow(name);
run("Specify...", "width=63 height=63 x=0 y=63 slice=0");
run("Duplicate...", "duplicate");
saveAs("Tiff", "/Users/scotttrinkle/GoogleDrive/Current/uCTdMRI/data/xray/samples/" + id + "-4.tif");
close();

selectWindow(name);
run("Specify...", "width=63 height=63 x=63 y=63 slice=0");
run("Duplicate...", "duplicate");
saveAs("Tiff", "/Users/scotttrinkle/GoogleDrive/Current/uCTdMRI/data/xray/samples/" + id + "-5.tif");
close();

selectWindow(name);
run("Specify...", "width=63 height=63 x=126 y=63 slice=0");
run("Duplicate...", "duplicate");
saveAs("Tiff", "/Users/scotttrinkle/GoogleDrive/Current/uCTdMRI/data/xray/samples/" + id + "-6.tif");
close();

selectWindow(name);
run("Specify...", "width=63 height=63 x=0 y=126 slice=0");
run("Duplicate...", "duplicate");
saveAs("Tiff", "/Users/scotttrinkle/GoogleDrive/Current/uCTdMRI/data/xray/samples/" + id + "-7.tif");
close();

selectWindow(name);
run("Specify...", "width=63 height=63 x=63 y=126 slice=0");
run("Duplicate...", "duplicate");
saveAs("Tiff", "/Users/scotttrinkle/GoogleDrive/Current/uCTdMRI/data/xray/samples/" + id + "-8.tif");
close();

selectWindow(name);
run("Specify...", "width=63 height=63 x=126 y=126 slice=0");
run("Duplicate...", "duplicate");
saveAs("Tiff", "/Users/scotttrinkle/GoogleDrive/Current/uCTdMRI/data/xray/samples/" + id + "-9.tif");
close();