import numpy as np
from strtens import odftools
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import timeit


def calc_hist(vectors, sphere, leaf=30, n_jobs=1):

    hist_points = np.stack((sphere.z, sphere.y, sphere.x), axis=-1)
    nbrs = NearestNeighbors(n_neighbors=1,
                            algorithm='ball_tree',
                            leaf_size=leaf,
                            n_jobs=n_jobs).fit(hist_points)
    indices = nbrs.kneighbors(vectors, return_distance=False)
    return indices
    # hist, _ = np.histogram(indices, bins=range(sphere.theta.size + 1))


def my_timeit(code, setup, r, n):
    results = timeit.repeat(code, setup, repeat=r, number=n)
    mean = np.mean(results) / n
    std = np.std(results) / n
    return mean, std


setup = '''
from __main__ import vectors, sphere, calc_hist, leaf
'''

code = '''
inds = calc_hist(vectors, sphere, leaf=leaf)
'''
vectors = np.load('./data/sample_8_4_vectors.npy').reshape((-1, 3))
sphere = odftools.make_sphere(6500)

leafs = np.arange(1, 11, 1)
means = []
stds = []
for leaf in leafs:
    print(leaf)
    m, s = my_timeit(code, setup, r=8, n=2)
    means.append(m)
    stds.append(s)

plt.errorbar(leafs, means, yerr=stds, fmt='k:o')
plt.xlabel('Leaf size')
plt.ylabel('Run time (s)')
plt.savefig('leaf_size_speed.pdf')
