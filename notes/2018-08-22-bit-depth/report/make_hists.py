import numpy as np
import matplotlib.pyplot as plt
from tifffile import imread

recon = imread('../recons/recon_06250.tiff').flatten()
recon8 = imread('../recons/recon_crop_8_06250.tiff').flatten()

plt.figure(1)
plt.hist(recon.flatten(), bins=512, color='black')
y1, y2 = plt.ylim()
plt.plot([-3.62e-4, -3.62e-4], [y1, y2], 'k:')
plt.plot([9.48e-4, 9.49e-4], [y1, y2], 'k:')
plt.ylim([y1, y2])
plt.savefig('figs/recon_orig_hist.png')

plt.figure(2)
plt.hist(recon8.flatten(), bins=256, color='black')
plt.savefig('figs/recon_crop8_hist.png')
