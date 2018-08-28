import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import rescale, resize, downscale_local_mean
import tifffile as tf
from scipy.misc import imresize
from scipy.ndimage import zoom

image = tf.imread('./recon_8bit/recon_8bit_04472.tiff')

image_downscaled = downscale_local_mean(image, (8, 8))

im_sp = imresize(image, size=1/8, interp='bilinear')
im_zoom = zoom(image, zoom=1/8, order=1)
