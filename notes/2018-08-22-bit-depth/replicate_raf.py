import numpy as np
import matplotlib.pyplot as plt
from tifffile import imread, imsave

print('Reading')
im = imread('./recon_orig_06890.tiff')

print('Cropping')
im = im[2064:2063 + 6720, 1104: 1104 + 10096]

print('Calculating percentiles')
thresh_low = 50
thresh_high = 60
# low = np.percentile(im, thresh_low)
# high = np.percentile(im, thresh_high)

hist, edges = np.histogram(im.flatten(), bins=1000)
hist = hist / hist.max()
edges = edges[:-1]

thresh = 0.01
low = edges[hist > thresh][0]  # finds first edge value greater than thresh
postlow = hist[edges > low]  # all hist values after low
histhigh = postlow[postlow < thresh][0]  # first hist value
high = edges[hist == histhigh]


# plt.plot(edges, hist)
# plt.plot([low, low], [0, 1], 'k:')
# plt.plot([high, high], [0, 1], 'k:')
# plt.show()


print('Clipping')
# im = np.clip(im, low, high).astype(np.float32)
im = im - low
im[im <= 0] = 0
# im[im <= low] = 0
im[im >= (high-low)] = (high-low)


print('Shifting')
# shifted = im - low
# scaled = ((shifted / shifted.max()) * 255).astype(np.uint8)
scaled = ((im / im.max()) * 255).astype(np.uint8)

# imsave('test_clip.tif', scaled)

fig, ax = plt.subplots(1, 2, figsize=(12, 6))

print('Plotting image')
ax[0].imshow(scaled, cmap='gray')

print('Plotting histogram')
ax[1].hist(scaled.flatten(), bins=256, log=False)
plt.show()
