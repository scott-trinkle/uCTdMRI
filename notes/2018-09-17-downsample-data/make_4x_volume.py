import numpy as np
import tifffile as tf
from scipy.ndimage import zoom
from glob import glob

fns = sorted(glob(
    '../../../Data/2018_04_03_WholeBrainMRI1_retake_newfocus/recon_flatcorr_1x/recon_4x/*.tiff'))

vol = np.zeros((len(fns), 1490, 2289), dtype=np.uint8)
for i, fn in enumerate(fns):
    print(i)
    vol[i] = tf.imread(fn)

vol_small = zoom(vol, [1 / 4, 1, 1], order=1)
tf.imsave('../../../Data/2018_04_03_WholeBrainMRI1_retake_newfocus/recon_flatcorr_1x/recon_4x.tif', vol_small)
