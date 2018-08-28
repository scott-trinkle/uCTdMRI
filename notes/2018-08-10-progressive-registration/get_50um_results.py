from comparison_funcs import *

res = 50
bins = 1024
outfn = './results/data/warp_50.csv'
warped_data = np.squeeze(
    nib.load('./registrations/50um/reg_50umWarped.nii.gz').get_data())
MRI_data = np.squeeze(nib.load('./data/mri_50um.nii.gz').get_data())

with open(outfn, 'w') as f:
    f.write('Resolution,Kind,Interp-pair,MSE,CC,MI\n')
    for interp in ['bicubic', 'bilinear', 'no_interp']:
        f.write('{0},{1},{2},{3},{4},{5}\n'.format(res,
                                                   'warped',
                                                   interp,
                                                   MSE(warped_data,
                                                       MRI_data),
                                                   CC(warped_data,
                                                      MRI_data),
                                                   MI(warped_data,
                                                       MRI_data,
                                                       bins=bins)))
