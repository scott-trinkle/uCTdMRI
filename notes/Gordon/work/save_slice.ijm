name = "UK1"
fn = name + ".tif"
open("/Users/scotttrinkle/GoogleDrive/Current/uCTdMRI/data/xray/samples/" + fn);
run("Duplicate...", "duplicate range=32-32");
run("Size...", "width=5000 height=5000 constrain average interpolation=None");
run("Enhance Contrast", "saturated=0.35");
saveAs("PNG", "/Users/scotttrinkle/GoogleDrive/Current/uCTdMRI/notes/Gordon/work/poster_slices/data_" + name + ".png");
close();
close();
