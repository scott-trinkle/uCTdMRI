import numpy as np
from strtens.util import imread, imsave
from strtens import StructureTensor

print('Reading image')
im = imread('../../data/xray/recon_2x_stack-1.tif')
mask = imread('./recon1mask.tif')

sds = np.arange(1, 11) / 1.2
sns = np.arange(1, 11) / 1.2
with open('AI/AIs.csv', 'w+') as f:
    f.write('S_d, S_n, Mean, Max, Mask Mean, Mask Max\n')
    for sd in sds:
        for sn in sns:
            print(sd, sn)
            ai, vectors = StructureTensor(im,
                                          d_sigma=sd,
                                          n_sigma=sn,
                                          gaussmode='nearest').results()
            f.write('{:.2f}, {:.2f}, {:.3f}, '.format(sd, sn, ai.mean()) +
                    '{:.3f}, {:.3f}, {:.3f}\n'.format(ai.max(),
                                                      ai[mask == 1].mean(),
                                                      ai[mask == 1].max()))

            imsave(fn='RGBs/d{:.2f}_n{:.2f}.tif'.format(sd, sn),
                   im=vectors,
                   rgb=True,
                   scalar=ai)
