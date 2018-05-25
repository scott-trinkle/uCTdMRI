import numpy as np
from strtens.util import imread, imsave
from strtens import StructureTensor
from sklearn import metrics


def write_csv(fn, sds, sns, im, mask, metric, saveim=False, impath=None, rgb=False):
    with open(fn, 'w+') as f:
        f.write(
            'S_d, S_n, Mean, Max, Mask Mean, Mask Max, Inv Mask Mean, Inv Mask Max, AUC\n')
        for sd in sds:
            for sn in sns:
                print(sd, sn)
                ai, vectors = StructureTensor(im,
                                              d_sigma=sd,
                                              n_sigma=sn,
                                              gaussmode='nearest',
                                              fast=True).results(metric)
                auc = metrics.roc_auc_score(mask.flatten(), ai.flatten())
                f.write('{:.2f}, {:.2f}, {:.3f}, '.format(sd, sn, ai.mean()) +
                        '{:.3f}, {:.3f}, {:.3f}, '.format(ai.max(),
                                                          ai[mask == 1].mean(),
                                                          ai[mask == 1].max()) +
                        '{:.3f}, {:.3f}, {:.3f}\n'.format(ai[mask == 0].mean(),
                                                          ai[mask == 0].max(),
                                                          auc))
                if saveim:
                    if rgb:
                        imsave(fn=impath + 'd{:.2f}_n{:.2f}_RGB.tif'.format(sd, sn),
                               im=vectors,
                               rgb=True,
                               scalar=ai)
                    else:
                        imsave(fn=impath + 'd{:.2f}_n{:.2f}_RGB.tif'.format(sd, sn),
                               im=ai,
                               dtype=np.float32)
