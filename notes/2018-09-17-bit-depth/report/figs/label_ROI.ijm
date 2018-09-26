selectWindow("recon_crop_8_06250.tiff");
run("RGB Color");
run("Line Width...", "line=15");


xs = newArray(2173, 3791, 3504, 4092, 5670, 6768, 6864, 8028, 8874, 5358);
ys = newArray(2950, 1145, 2886, 4170, 2472, 2802, 1452, 1254, 3714, 2256);
cs = newArray("red", "green", "blue", "magenta", "cyan", "yellow", "orange");
r = newArray(93, 0, 255);
g = newArray(255, 93, 185);
b = newArray(170, 9, 235);

for (i=0; i<7; i++){
	run("Colors...", "foreground="+cs[i]+" background="+cs[i]+" selection="+cs[i]);
	makeRectangle(xs[i], ys[i], 125, 125);
	run("Draw", "slice");
}
/*for (i = 0; i < 3; i++){
	setForegroundColor(r[i],g[i],b[i]);
	makeRectangle(xs[i + 7], ys[i+7], 125, 125);
	run("Draw", "slice");
}	
	*/

/*
x0 = 2173;
y0 = 2950;
c='purple';

93 255 170
0 93 9
255 185 235


