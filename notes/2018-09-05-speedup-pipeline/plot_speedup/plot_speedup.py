import numpy as np
import matplotlib.pyplot as plt
from strtens import odftools
import timeit


def my_timeit(code, setup, r, n):
    results = timeit.repeat(code, setup, repeat=r, number=n)
    mean = np.mean(results) / n
    std = np.std(results) / n
    return mean, std


def calc_speedup(ns, vectors):
    setup = '''
    from __main__ import vectors, sphere
    from strtens import odftools
    import numpy as np
    '''

    setup_delta = '''
    from __main__ import theta, phi
    from strtens import odftools
    '''

    code = '''
    c = odftools.get_SH_coeffs(20, vectors, sphere)
    '''

    print('Calculating delta method')
    sphere = None
    theta, phi = odftools.cart_to_spherical(vectors)
    m0, s0 = my_timeit(
        'c = odftools.get_SH_coeffs_delta(20, theta, phi)', setup=setup_delta, r=10, n=3)

    np.save('data/m0', m0)
    np.save('data/s0', s0)

    means = []
    stds = []

    for n in ns:
        print(n)
        sphere = odftools.make_sphere(n)
        m, s = my_timeit(code, setup, r=10, n=3)
        means.append(m)
        stds.append(s)

    np.save('data/means', means)
    np.save('data/stds', stds)
    return np.array(means), np.array(stds), np.array(m0), np.array(s0)


vectors = np.load('../data/sample_8_4_vectors.npy')
ns = np.arange(500, 10001, 500)

calc = False
if calc:
    means, stds, m0, s0 = calc_speedup(ns, vectors)
else:
    means = np.load('data/means.npy')
    stds = np.load('data/stds.npy')
    m0 = np.load('data/m0.npy')
    s0 = np.load('data/s0.npy')

speedup = means / m0
perc_err = ((stds / means) + (s0/m0))
err = speedup * perc_err

fig, ax = plt.subplots()
ax.errorbar(ns, 100 - speedup*100, yerr=err*100, fmt='k:o', ms=3)
ax.set_xlabel('Number of sample points')
ax.set_ylabel('Percent speed-up')
ax.set_title('Speed-up')
plt.tight_layout()
plt.savefig('speedup.pdf')
