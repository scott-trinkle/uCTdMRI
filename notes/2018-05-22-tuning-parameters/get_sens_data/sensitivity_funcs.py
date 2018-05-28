import numpy as np
from strtens.util import imread
from strtens import odftools
from strtens import StructureTensor
from sklearn import metrics


def sensitivity(imfn, maskfn, resultspath, sds, sns):
    im = imread(imfn)
    mask = imread(maskfn)
    peak_data = []
    inds = []
    with open(resultspath + 'results.csv', 'w+') as f:
        f.write(
            'S_d, S_n, Mask Mean FA, AUC, Theta Mask Mean, Theta Mask Std, Phi Mask Mean, Phi Mask Std, npeaks, Mask Fraction\n')
        for sd in sds:
            for sn in sns:
                print(sd, sn)
                ai, vectors = StructureTensor(im,
                                              d_sigma=sd,
                                              n_sigma=sn).results('fa')
                auc = metrics.roc_auc_score(mask.flatten(), ai.flatten())
                f.write('{:.6f}, {:.6f}, {:.6f}, {:.6f}, '.format(
                    sd, sn, ai[mask == 1].mean(), auc))
                theta, phi = odftools.cart_to_spherical(vectors)
                f.write('{:.16f}, {:.16f}, {:.16f}, {:.16f},'.format(
                    theta[mask == 1].mean(), theta[mask == 1].std(),
                    phi[mask == 1].mean(), phi[mask == 1].std()))

                coeffs = odftools.get_SH_coeffs(20, theta, phi)
                sphere = odftools.make_sphere(1500)
                odf = odftools.get_odf(coeffs, sphere)
                peak_dirs, _, _ = odftools.get_peaks(odf, sphere)
                f.write('{:.2f}, {:.16f}\n'.format(peak_dirs.shape[0],
                                                   mask[mask == 1].size / mask.size))

                inds.append([sd, sn])
                peak_data.append(peak_dirs)
    np.save(resultspath + 'peak_data', peak_data)
    np.save(resultspath + 'inds', inds)
    return np.array(peak_data)


def crossing_sensitivity(imfn, maskfn, resultspath, sds, sns):
    im = imread(imfn)
    mask = imread(maskfn)
    binmask = mask > 0
    fib1mask = mask == 1
    fib2mask = mask == 2
    peak_data = []
    inds = []
    with open(resultspath + 'results.csv', 'w+') as f:
        f.write(
            'S_d, S_n, Mask Mean FA, AUC, Theta 1 Mask Mean, Theta 1 Mask Std, Phi 1 Mask Mean, Phi 1 Mask Std, Theta 2 Mask Mean, Theta 2 Mask Std, Phi 2 Mask Mean, Phi 2 Mask Std, npeaks, Mask Fraction\n')
        for sd in sds:
            for sn in sns:
                print(sd, sn)
                ai, vectors = StructureTensor(im,
                                              d_sigma=sd,
                                              n_sigma=sn).results('fa')

                auc = metrics.roc_auc_score(binmask.flatten(), ai.flatten())
                f.write('{:.6f}, {:.6f}, {:.6f}, {:.6f}, '.format(
                    sd, sn, ai[binmask].mean(), auc))

                theta, phi = odftools.cart_to_spherical(vectors)
                f.write('{:.16f}, {:.16f}, {:.16f}, {:.16f},'.format(
                    theta[fib1mask].mean(), theta[fib1mask].std(),
                    phi[fib1mask].mean(), phi[fib1mask].std()))
                f.write('{:.16f}, {:.16f}, {:.16f}, {:.16f},'.format(
                    theta[fib2mask].mean(), theta[fib2mask].std(),
                    phi[fib2mask].mean(), phi[fib2mask].std()))

                coeffs = odftools.get_SH_coeffs(20, theta, phi)
                sphere = odftools.make_sphere(1500)
                odf = odftools.get_odf(coeffs, sphere)
                peak_dirs, _, _ = odftools.get_peaks(odf, sphere)
                f.write('{:.2f}, {:.16f}\n'.format(peak_dirs.shape[0],
                                                   binmask.sum() / binmask.size))

                inds.append([sd, sn])
                peak_data.append(peak_dirs)
    np.save(resultspath + 'peak_data', peak_data)
    np.save(resultspath + 'inds', inds)
    return np.array(peak_data)


def get_odfs(imfn, resultspath, sds, sns):
    im = imread(imfn)
    coeffs = []
    coeffsapp = coeffs.append
    for sd in sds:
        for sn in sns:
            print(sd, sn)
            vectors = StructureTensor(im,
                                      d_sigma=sd,
                                      n_sigma=sn).get_orientations()

            theta, phi = odftools.cart_to_spherical(vectors)
            coeffsapp(odftools.get_SH_coeffs(20, theta, phi))
    np.save(resultspath + 'coeffs', coeffs)
