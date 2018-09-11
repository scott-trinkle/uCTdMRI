import numpy as np
import matplotlib.pyplot as plt
from strtens.util import imread, imsave, segment_ROI
from glob import glob

fns = glob('../samples_8/*.tif')
# for fn in fns:
#     print(fn)
#     im = imread(fn)
#     mask = segment_ROI(im)
#     outfn = 'masks/' + fn.split('.tif')[0].split('/')[-1] + '_mask.tif'
#     imsave(outfn, mask)


# im = imread(fns[1])
# labels = segment_ROI(im)

sl = 100
fig, ax = plt.subplots(1, 2)
ax[0].imshow(labels[sl], cmap='gray')
ax[1].imshow(im[sl], cmap='gray')
plt.tight_layout()
plt.show()
