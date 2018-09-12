import numpy as np
import matplotlib.pyplot as plt
from strtens import odftools


def calc_rmses(ns, vectors, c_true):

    rmses = []
    for n in ns:
        print(n)
        sphere = odftools.make_sphere(n)
        c_est = odftools.get_SH_coeffs(20, vectors, sphere)
        rmses.append(np.sqrt(np.mean((c_true - c_est)**2)))
    rmses = np.array(rmses)
    np.save('data/rmses', rmses)
    return rmses


vectors = np.load('../data/sample_8_4_vectors.npy')
c_true = np.load('../data/sample_8_4_coeffs.npy')

ns = np.arange(500, 10001, 500)
calc = False
if calc:
    rmses = calc_rmses(ns, vectors, c_true)
else:
    rmses = np.load('data/rmses.npy')

fig, ax = plt.subplots()
ax.plot(ns, rmses, 'k:o', ms=4)
ax.set_xlabel('Number of sample points')
ax.set_ylabel('Root Mean squared error')
ax.set_title('RMSE')
plt.tight_layout()
plt.savefig('rmse.pdf')
