import numpy as np
import nibabel as nib
from glob import glob
from scipy.io import loadmat
import itertools


def MI(im1, im2, bins):
    # Mutual information for joint histogram

    hgram, _, _ = np.histogram2d(im1.ravel(), im2.ravel(), bins=bins)

    # Convert bins counts to probability values
    pxy = hgram / hgram.sum()

    px = pxy.sum(axis=1)  # marginal for x over y
    py = pxy.sum(axis=0)  # marginal for y over x
    px_py = px[:, None] * py[None, :]  # Broadcast to multiply marginals
    # Now we can do the calculation using the pxy, px_py 2D arrays
    nzs = pxy > 0  # Only non-zero pxy values contribute to the sum
    return np.sum(pxy[nzs] * np.log(pxy[nzs] / px_py[nzs]))


def MSE(arr1, arr2):
    return ((arr1-arr2)**2).mean()


def CC(arr1, arr2):
    return np.corrcoef(arr1.flatten(), arr2.flatten())[0, 1]


def affine_results(res):
    outfn = 'results/affine_{}.csv'.format(res)
    tr = 'AffineTransform_double_3_3'
    fi = 'fixed'
    affines = glob(
        'registrations/*_{res}/*{res}0GenericAffine.mat'.format(res=res))

    data = {}
    interps = ['bicubic', 'bilinear', 'no_interp']
    for aff in affines:
        for interp in interps:
            if interp in aff:
                data[interp] = loadmat(aff)

    with open(outfn, 'w') as f:
        f.write('Resolution,Interp-pair,MSE_t,CC_t,MSE_f,CC_f\n')
        for int1, int2 in itertools.combinations(interps, 2):
            MSE_t = MSE(data[int1][tr], data[int2][tr])
            CC_t = CC(data[int1][tr], data[int2][tr])
            MSE_f = MSE(data[int1][fi], data[int2][fi])
            CC_f = CC(data[int1][fi], data[int2][fi])
            f.write('{0},{1}_{2},{3},{4},{5},{6}\n'.format(res,
                                                           int1,
                                                           int2,
                                                           MSE_t,
                                                           CC_t,
                                                           MSE_f,
                                                           CC_f))


res = 150


def warp_results(res, bins=1024):

    outfn = 'results/warp_{}.csv'.format(res)
    warp_fns = glob('registrations/*_{res}/*{res}1Warp.nii.gz'.format(res=res))
    warped_fns = glob(
        'registrations/*_{res}/*{res}Warped.nii.gz'.format(res=res))

    data = {}
    interps = ['bicubic', 'bilinear', 'no_interp']
    for interp in interps:
        data[interp] = {}
    for warp_fn, warped_fn in zip(warp_fns, warped_fns):
        for interp in interps:
            if interp in warp_fn and warped_fn:
                warp_img = nib.load(warp_fn)
                data[interp]['warp'] = np.squeeze(warp_img.get_data())
                warped_img = nib.load(warped_fn)
                data[interp]['warped'] = np.squeeze(warped_img.get_data())

    MRI_data = {}
    for interp in interps:
        MRI_data[interp] = np.squeeze(
            nib.load('data/mri_{0}um_{1}.nii.gz'.format(res, interp)).get_data())

    with open(outfn, 'w') as f:
        f.write('Resolution,Kind,Interp-pair,MSE,CC,MI\n')
        for int1, int2 in itertools.combinations(interps, 2):
            f.write('{0},{1},{2}_{3},{4},{5},{6}\n'.format(res,
                                                           'warp',
                                                           int1,
                                                           int2,
                                                           MSE(data[int1]['warp'],
                                                               data[int2]['warp']),
                                                           CC(data[int1]['warp'],
                                                              data[int2]['warp']),
                                                           MI(data[int1]['warp'],
                                                              data[int2]['warp'],
                                                              bins=bins)))
        for interp in interps:
            f.write('{0},{1},{2},{3},{4},{5}\n'.format(res,
                                                       'warped',
                                                       interp,
                                                       MSE(data[interp]['warped'],
                                                           MRI_data[interp]),
                                                       CC(data[interp]['warped'],
                                                          MRI_data[interp]),
                                                       MI(data[interp]['warped'],
                                                          MRI_data[interp],
                                                          bins=bins)))
