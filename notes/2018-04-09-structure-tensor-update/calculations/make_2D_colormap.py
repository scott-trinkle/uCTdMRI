from strtens.util import make_rgb, make_sphere
import numpy as np
import matplotlib.pyplot as plt

n = 1000
x, y, z, _, _ = make_sphere(n)  # Don't need T or P

rgb = np.dstack((make_rgb(x),
                 make_rgb(y),
                 make_rgb(z)))


ticks = np.linspace(0, n-1, 5)
xticklabels = [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$\pi/2$', r'$\pi$']
yticklabels = [r'0', r'$\pi/4$', r'$\pi/2$', r'$3\pi/4$', r'$\pi$']

fig, ax = plt.subplots()

ax.imshow(rgb)

ax.xaxis.set_ticks(ticks)
ax.xaxis.set_ticklabels(xticklabels)
ax.set_xlabel(r'Azimuthal, $\phi$')

ax.yaxis.set_ticks(ticks)
ax.yaxis.set_ticklabels(yticklabels)
ax.set_ylabel(r'Polar, $\theta$')

plt.tight_layout()
plt.savefig('../figs/colormap.pdf',
            dpi=300)
