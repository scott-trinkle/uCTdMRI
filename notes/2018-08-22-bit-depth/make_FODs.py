import numpy as np
from strtens import StructureTensor
from strtens.util import imread
import strtens.odftools as odftools
from glob import glob


def get_FOD(fn, ID):
    print(ID)
    print('Reading image')
    im = imread(fn)

    print('Calculating vectors')
    FA, vectors = StructureTensor(im,
                                  d_sigma=15 / 2.4,
                                  n_sigma=13 / 2.4).results()
    np.save('results/{}_FA'.format(ID), FA)
    np.save('results/{}_vectors'.format(ID), vectors)

    print('Calculating coefficients')
    theta, phi = odftools.cart_to_spherical(vectors)
    c = odftools.get_SH_coeffs(20, theta, phi)
    np.save('results/{}_coeffs'.format(ID), c)

    print('Making ODF')
    sphere = odftools.make_sphere(1200)
    odf = odftools.get_odf(c, sphere)
    np.save('results/{}_odf'.format(ID), odf)


fns = glob('./samples/*.tif')
