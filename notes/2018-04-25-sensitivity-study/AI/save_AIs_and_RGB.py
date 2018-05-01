import numpy as np
from strtens.util import imread, imsave
from strtens import StructureTensor


def write_csv(fn, sds, sns, im, metric, rgbpath):
    with open(fn, 'w+') as f:
        f.write(
            'S_d, S_n, Mean, Max, Mask Mean, Mask Max, Inv Mask Mean, Inv Mask Max\n')
        for sd in sds:
            for sn in sns:
                print(sd, sn)
                ai, vectors = StructureTensor(im,
                                              d_sigma=sd,
                                              n_sigma=sn,
                                              gaussmode='nearest').results(metric)
                f.write('{:.2f}, {:.2f}, {:.3f}, '.format(sd, sn, ai.mean()) +
                        '{:.3f}, {:.3f}, {:.3f}, '.format(ai.max(),
                                                          ai[mask == 1].mean(),
                                                          ai[mask == 1].max()) +
                        '{:.3f}, {:.3f}\n'.format(ai[mask == 0].mean(),
                                                  ai[mask == 0].max()))

                imsave(fn=rgbpath + 'd{:.2f}_n{:.2f}.tif'.format(sd, sn),
                       im=vectors,
                       rgb=True,
                       scalar=ai)


print('Reading image')
im = imread('../../data/xray/recon_2x_stack-1.tif')
mask = imread('../../data/xray/recon1mask.tif')

# 1.2 um / vox, so this converts um to voxels
sds = np.arange(1, 11) / 1.2
sns = np.arange(1, 11) / 1.2

write_csv('AIs_westin.csv', sds=sds, sns=sns,
          im=im, metric='westin', rgbpath='../RGB/RGBs_westin/')
write_csv('AIs_FA.csv', sds=sds, sns=sns,
          im=im, metric='fa', rgbpath='../RGB/RGBs_FA/')
