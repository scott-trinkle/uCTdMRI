import numpy as np
import tifffile as tf
from skimage import io
from strtens.util import imread, imsave, rescale
from libtiff import TIFF


def test_tf(fn):
    im = tf.imread(fn)
    outfn = 'out/' + fn.split('/')[1].split('.')[0] + '_tf_out.tif'
    # tf.imsave(outfn, im)
    return im


def test_io(fn):
    im = tf.imread(fn)
    outfn = 'out/' + fn.split('/')[1].split('.')[0] + '_io_out.tif'
    # io.imsave(outfn, im)
    return im


def test_str(fn):
    im = tf.imread(fn)
    outfn = 'out/' + fn.split('/')[1].split('.')[0] + '_str_out.tif'
    # imsave(outfn, im)
    return im


def test_TIFF(fn):
    tiff = TIFF.open(fn, 'r')
    im = tiff.read_image(fn)
    tiff.close()

    outfn = 'out/' + fn.split('/')[1].split('.')[0] + '_tiff_out.tif'
    tiff_out = TIFF.open(outfn, 'w')
    tiff_out.write_image(im)
    tiff_out.close()


fn = 'recon_44/recon_04470.tiff'
outfn = ['out/' + fn.split('/')[1].split('.')[0] + '_{}_out.tif'.format(pack)
         for pack in ['tf', 'io', 'str', 'tiff']]

im_tf = tf.imread(outfn[0])
im_io = tf.imread(outfn[1])
im_str = tf.imread(outfn[2])
im_tiff = tf.imread(outfn[3])

labels = ['im_tf', 'im_io', 'im_str', 'im_tiff']

for i, im1 in enumerate([im_tf, im_io, im_str, im_tiff]):
    for j, im2 in enumerate([im_tf, im_io, im_str, im_tiff]):
        print(labels[i], labels[j], end='\n')
        print('Mean diff: ', (im1-im2).mean())
        print('Std diff: ', (im1-im2).std(), end='\n\n')
