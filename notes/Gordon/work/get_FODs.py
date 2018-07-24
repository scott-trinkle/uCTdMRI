import numpy as np
from strtens.util import imread
from strtens import odftools, StructureTensor


def save_coeffs(fn, path='../../../data/xray/samples/'):
    im = imread(path + fn + '.tif')
    FA, vectors = StructureTensor(im).results('fa')
    theta, phi = odftools.cart_to_spherical(vectors=vectors, FA=FA, im=im)
    c = odftools.get_SH_coeffs(20, theta, phi)
    np.save(fn + 'coeffs_test', c)


names = ['AC1', 'AC2', 'AC3', 'CB1', 'CB2', 'CC1', 'CC2', 'CC3', 'CC4', 'UK1']

for name in names:
    for i in range(1, 10):
        fn = name + '-' + str(i)
        print(fn)
        save_coeffs(fn)
