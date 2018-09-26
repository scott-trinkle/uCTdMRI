import matplotlib.pyplot as plt
import numpy as np
from glob import glob

path = '../../../Data/2018_04_03_WholeBrainMRI1_retake_newfocus/recon_flatcorr_1x/recon_crop8_new/*.tiff'
fns = glob(path)
nums = np.sort([int(fn.split('.tiff')[0].split('_')[-1]) for fn in fns])
diff = np.setdiff1d(range(0, 13310), nums)

plot = False
if plot:
    fig = plt.figure(figsize=(20, 6))
    plt.plot(diff[:100], np.diff(diff)[:100], 'k.:')
    plt.xlabel('Slice number')
    plt.ylabel('Distance to next missing slice')
    plt.title('Missing slices')
    plt.tight_layout()
    plt.show()
