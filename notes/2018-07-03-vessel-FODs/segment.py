import numpy as np
from strtens.util import imread, imsave
from sklearn import cluster
from scipy.ndimage import binary_dilation
from glob import glob


def get_mask(im):
    kmeans = cluster.KMeans(n_clusters=3,
                            random_state=48).fit(im.reshape((-1, 1)))
    labels = kmeans.labels_.reshape(im.shape)
    mask = np.zeros_like(labels)
    mask[labels == 2] = 1
    mask = binary_dilation(mask, iterations=1).astype(mask.dtype)
    return mask


fns = glob('../../data/xray/samples/*-*.tif')

for i, fn in enumerate(fns):
    print('Segmenting: {}/{}'.format(i+1, len(fns)))
    im = imread(fn)
    mask = get_mask(im)
    outfn = 'masks/' + fn.split('/')[-1].split('.tif')[0] + '_mask.tif'
    imsave(outfn, mask)
    print('Done!\n')
