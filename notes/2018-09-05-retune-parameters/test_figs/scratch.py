import numpy as np
from strtens.util import imread, imsave
from strtens import StructureTensor
from strtens import odftools
from strtens.vis import show_ODF
from scipy.ndimage import gaussian_filter
from skimage import img_as_float
import temp_ST as ST

im = imread('./sample_8_0.tif')


def get_FOD(fn, ID, func):
    print(ID)
    print('Reading image')
    im = imread(fn)

    print('Calculating vectors')
    FA, vectors = func(im).results()
    imsave(ID + 'FA.tif', FA, dtype=np.float32)
    imsave(ID + 'vecs.tif', vectors, rgb=True, scalar=FA)

    print('Calculating coefficients')
    theta, phi = odftools.cart_to_spherical(vectors)
    c = odftools.get_SH_coeffs(20, theta, phi)

    print('Making ODF')
    sphere = odftools.make_sphere(1200)
    odf = odftools.get_odf(c, sphere)

    return odf


sphere = odftools.make_sphere(1200)
odf_o = get_FOD('sample_8_0.tif', 'old', func=StructureTensor)
show_ODF(odf_o, sphere, interactive=False, save=True, fn='FOD_old.png')
odf_n = get_FOD('sample_8_0.tif', 'new', func=ST.StructureTensor)
show_ODF(odf_n, sphere, interactive=False, save=True, fn='FOD_new.png')
