import numpy as np
from strtens import StructureTensor
from strtens.util import imread
import strtens.odftools as odftools
from glob import glob


def get_FOD(fn, bit, ID):

    path = 'results_{}/'.format(bit)

    print(ID)
    im = imread(fn)

    FA, vectors = StructureTensor(im).results()
    np.save(path + '{}_FA'.format(ID), FA)
    np.save(path + '{}_vectors'.format(ID), vectors)

    c = odftools.get_SH_coeffs(vectors)
    np.save(path + '{}_coeffs'.format(ID), c)


fns8 = sorted(glob('./samples_8/*.tif'))
fns32 = sorted(glob('./samples_32/*.tif'))

# print('Getting FOD from 8-bit')
# for fn in fns8:
#     ID = fn.split('.tif')[0].split('/')[-1]
#     get_FOD(fn, 8, ID)

print('Getting FOD from 32-bit')
for fn in fns32:
    ID = fn.split('.tif')[0].split('/')[-1]
    get_FOD(fn, 32, ID)
