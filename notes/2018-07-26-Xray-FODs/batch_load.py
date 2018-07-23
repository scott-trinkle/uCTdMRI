import numpy as np
import matplotlib.pyplot as plt
from libtiff import TIFF
from strtens.util import read_tif_stack, imread

xray_res = 2.4
mri_res = 150

sd = 15 / 2.4 * 4
sn = 13 / 2.4 * 4
pad = max(sd, sn)

num_slices = int(mri_res / xray_res + 2*pad)

# im = read_tif_stack('sample_data/recon_2x_', start=3000)

im = read_tif_stack('/Users/scotttrinkle/Downloads/test/recon_2x_', start=0)
