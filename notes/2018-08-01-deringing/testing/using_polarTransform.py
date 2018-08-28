import numpy as np
import tifffile as tf
import polarTransform as pT

print('Reading image')
fxy = tf.imread('./recon_10122.tiff')

print('Converting to polar')
frt, settings = pT.convertToPolarImage(fxy, center=[4887, 3922], radiusSize=10096,
                                       angleSize=10096, finalRadius=6520.4114134002311)
print('Saving...')
tf.imsave('pT_polar_6520.tiff', frt)

print('Converting back to cartesian')
fxy_pt, settings2 = pT.convertToCartesianImage(frt, settings=settings)

print('Saving')
tf.imsave('pT_cart_6520.tiff', fxy_pt)
