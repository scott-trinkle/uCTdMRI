import numpy as np
from skimage import io
import sys
sys.path.append('..')
import st_tools as st
import tifffile as tf
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1 import make_axes_locatable

print('Reading\n')
im = io.imread('../../data/recon_2x_stack-1.tif')

print('Running STA\n')
sl = 35
dsigs = [2]
nsigs = np.arange(1, 11)
nbins = [180, 360]
counter = 1


for dsig in dsigs:
    for nsig in nsigs:
        print('Counter: {}'.format(counter))
        print('dsig: {}\nnsig: {}'.format(dsig, nsig))

        print('Running STA')
        FA, vects = st.st_3D(im,
                             d_sigma=dsig,
                             n_sigma=nsig,
                             westin=True)

        r = np.sqrt(vects[..., 0]**2 + vects[..., 1]**2 + vects[..., 2]**2)
        theta = np.arccos(vects[..., 2] / r)
        phi = np.arctan2(vects[..., 1], vects[..., 0]) + np.pi

        H, _, _ = np.histogram2d(theta.flatten(), phi.flatten(), bins=nbins)
        
        fig, ax = plt.subplots()

        hist = ax.imshow(H, norm=LogNorm(vmin=1, vmax=H.max()))
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)

        ax.set_xlabel(r'$\phi$')
        ax.set_ylabel(r'$\theta$')
        ax.set_title(r'$\sigma_d$ = {}, $\sigma_n$ = {}'.format(
            dsig, nsig))
        phi_ticks = np.linspace(0, 360, 5)
        theta_ticks = np.linspace(0, 180, 5)
        theta_labels = np.linspace(0, 180, 5, dtype=int)
        phi_labels = np.linspace(0, 360, 5, dtype=int)
        plt.xticks(phi_ticks, phi_labels)
        plt.yticks(theta_ticks, theta_labels)
        fig.colorbar(hist, cax=cax)


        print('Saving...\n')
        plt.savefig('hists/d{}_n{}.tif'.format(dsig, nsig), dpi=300)

print('Done!')
