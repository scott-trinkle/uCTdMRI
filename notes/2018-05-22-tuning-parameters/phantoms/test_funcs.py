import numpy as np
from strtens import StructureTensor
from strtens.util import imread
from strtens import odftools
from strtens.vis import show_ODF, show_peaks


def full_pipeline(im, d_sigma, n_sigma, aithresh, metric='fa'):
    print('Running ST')
    AI, vectors = StructureTensor(im,
                                  d_sigma=d_sigma,
                                  n_sigma=n_sigma).results(metric)

    print('Thresholding')
    vectors_thresh = vectors[AI > aithresh]

    print('Converting to spherical coordinates')
    theta, phi = odftools.vectors_to_spherical(vectors_thresh)

    print('Getting SH coefficients')
    coeffs = odftools.get_SH_coeffs(20, theta, phi)

    print('Making odf')
    sphere = odftools.make_sphere(1500)
    odf = odftools.get_odf(coeffs, sphere)

    print('Getting peaks')
    peak_dirs, vals, inds = odftools.get_peaks(odf, sphere)

    return peak_dirs, AI, vectors, coeffs


true_dirs = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
for i, orient in enumerate(['x', 'y', 'z']):
    print('reading im: {}'.format(orient))
    fn = '../phantoms/generic_xyz/phants/{}_phantom_nfib16_r8.tif'.format(
        orient)
    im = imread(fn)
    for d, n in [[1, 1], [2.5, 5], [5, 8]]:
        print('starting pipeline: d{} n{}'.format(d, n))
        dirs, ai, vectors, coeffs = full_pipeline(im,
                                                  d_sigma=d,
                                                  n_sigma=n,
                                                  aithresh=0)
        path = '../phantoms/generic_xyz/results/{}'.format(orient)
        tail = 'd{}_n{}'.format(d, n)
        np.save(path + 'dirs' + tail, dirs)
        np.save(path + 'ai' + tail, dirs)
        np.save(path + 'vectors' + tail, vectors)
        np.save(coeffs + 'coeffs' + tail, coeffs)
        dirs = np.random.random((1, 3))
        diff = odftools.get_ang_distance(dirs, np.array([true_dirs[i]]))
