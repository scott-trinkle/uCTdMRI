import numpy as np
import matplotlib.pyplot as plt
from tifffile import imread

recon = imread('../slice_samples/recon_full_07000.tiff').flatten()
recon8 = imread('../slice_samples/recon_07000.tiff').flatten()

plt.figure(1)
plt.hist(recon.flatten(), bins=512, color='black')
y1 = 0
y2 = 0.65e7
plt.plot([-6.68e-4, -6.68e-4], [y1, y2], 'k:')
plt.plot([0.001, 0.001], [y1, y2], 'k:')
plt.ylim([y1, y2])
plt.savefig('figs/recon_orig_hist.png')

plt.figure(2)
plt.hist(recon8.flatten(), bins=256, color='black')
plt.ylim([0, 6e5])
plt.savefig('figs/recon_crop8_hist.png')
