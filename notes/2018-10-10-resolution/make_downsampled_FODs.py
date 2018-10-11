import numpy as np
from strtens import StructureTensor
from strtens.util import imread
import strtens.odftools as odftools
from scipy.ndimage import zoom
from glob import glob


def get_FOD_zoom(fn, factor, ID):

    d_sig = 15 / 1.2
    n_sig = 13 / 1.2

    path = 'results_{}x/'.format(factor)

    im = imread(fn)
    im = zoom(im, 1 / factor, order=3, mode='nearest')

    FA, vectors = StructureTensor(im,
                                  d_sigma=d_sig / factor,
                                  n_sigma=n_sig / factor).results()
    np.save(path + '{}_FA'.format(ID), FA)
    np.save(path + '{}_vectors'.format(ID), vectors)

    c = odftools.get_SH_coeffs(vectors)
    np.save(path + '{}_coeffs'.format(ID), c)


fns = sorted(glob('../2018-09-17-bit-depth/samples_32/*.tif'))

for i, fn in enumerate(fns):
    ID = fn.split('.tif')[0].split('/')[-1]
    print()
    print('{}/{}'.format(i + 1, len(fns)))
    for factor in range(2, 6):
        print('{}x'.format(factor))
        get_FOD_zoom(fn, factor, ID)
