'''
XRAY REGISTRATION WAS BAD
'''

import numpy as np
import st_tools as st
import nibabel as nib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


def MSE(dti, tens, axis=None):
    return np.round(((dti - tens) ** 2).mean(axis=axis) / dti.mean() * 100, 3)


def plot_comparison(dti, tensor, slicenum=80, diffnum=0, tensnum=0):

    element = ['x', 'y', 'z']

    dti = dti[:, slicenum, :, diffnum]
    tensor = tensor[:, slicenum, :, tensnum]

    # vmin = np.array([dti.min(), tensor.min()]).min()
    # vmax = np.array([dti.max(), tensor.max()]).max()

    mse = ((dti - tensor)**2) / dti.mean() * 100

    fig = plt.figure(1, figsize=(12, 8))

    ax1 = fig.add_subplot(131)
    # ax1.imshow(dti, vmin=vmin, vmax=vmax, cmap='gray')
    ax1.imshow(dti, cmap='gray')
    ax1.axis('off')
    ax1.set_title('{} - DTI'.format(element[diffnum]))

    ax2 = fig.add_subplot(132)
    # ax2.imshow(tensor, vmin=vmin, vmax=vmax, cmap='gray')
    ax2.imshow(tensor, cmap='gray')
    ax2.axis('off')
    ax2.set_title('{} - Structure Tensor'.format(element[tensnum]))

    ax3 = fig.add_subplot(133)
    diff = ax3.imshow(mse, cmap='gray')

    ax3.axis('off')
    ax3.set_title('MSE: {} %'.format(MSE(dti, tensor)))

    divider = make_axes_locatable(ax3)
    cax = divider.append_axes("right", size="5%", pad=0.05)

    fig.colorbar(diff, cax=cax)

    plt.tight_layout()
    plt.show()


def threshold_FA(vects, FA, thresh=0.0):

    for i in range(3):
        vects[..., i][FA < thresh] = 0

    return vects


# Import tensor data
dti = nib.load('../data/dti_tensor_2.nii.gz').get_data()
# dti = np.moveaxis(dti, [1, 2], [2, 1]).astype(np.float32)
dti = dti.astype(np.float32)
mask = dti != 0

dti_mat = np.moveaxis(np.array([[dti[..., 0], dti[..., 1], dti[..., 2]],
                                [dti[..., 1], dti[..., 3], dti[..., 4]],
                                [dti[..., 2], dti[..., 4], dti[..., 5]]]), [0, 1], [3, 4])

dti_evals, dti_evects = np.linalg.eigh(dti_mat)

dti_evects = dti_evects[..., 2]

dti_FA = np.where(np.linalg.norm(dti_evals, axis=-1) **
                  2 != 0, st._FA(dti_evals), np.zeros_like(dti[..., 0]))

dti_evects = threshold_FA(dti_evects, dti_FA)


# Import structural data
# b0 = nib.load('../data/diffdata_b0.nii.gz').get_data()
b0 = nib.load(
    '../register/deformable_150/deformable_150Warped.nii.gz').get_data().squeeze()
b0 = np.moveaxis(b0, [1, 2], [2, 1])
b0 = np.flip(b0, axis=1) * mask[..., 0]

b0_FA, b0_evects = st.st_3D(b0,
                            d_sigma=1,
                            n_sigma=2)

b0_evects = threshold_FA(b0_evects, b0_FA)

# b0_evects *= mask[...,0:3]

plot_comparison(dti, b0_evects,
                slicenum=40,
                diffnum=0,
                tensnum=0)

dtiavg = [dti_evects[..., 0].mean(), dti_evects[..., 1].mean(),
          dti_evects[..., 2].mean()]
b0avg = [b0_evects[..., 0].mean(), b0_evects[..., 1].mean(),
         b0_evects[..., 2].mean()]
