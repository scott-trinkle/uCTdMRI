import numpy as np
import pandas as pd
from strtens import vis, odftools


def save_odf(fn, c):
    sphere = odftools.make_sphere(1200)
    odf = odftools.get_odf(c, sphere)
    vis.show_ODF(odf, sphere, interactive=False, save=True, fn=fn)


def peaks(c, thresh=0.20, sep=10):
    sphere = odftools.make_sphere(1200)
    odf = odftools.get_odf(c, sphere)
    return odftools.get_peaks(odf, sphere, threshold=thresh, minsep=sep)


def ang_dist(c1, c2, thresh=0.95, sep=20):
    p1 = peaks(c1, thresh=thresh, sep=sep)[0]
    p2 = peaks(c2, thresh=thresh, sep=sep)[0]
    return odftools.get_ang_distance(p1, p2)


df = pd.read_pickle('../df_raw.pkl')
# 2 196: 0.85
# 2 197: 0.90
# 2 205: 0.95


c85 = np.load('../results_2x/sample_32_196_x6993_y1488_coeffs.npy')
c85t = np.load(
    '../../2018-09-17-bit-depth/results_32/sample_32_196_x6993_y1488_coeffs.npy')

c90 = np.load('../results_2x/sample_32_197_x6993_y1729_coeffs.npy')
c90t = np.load(
    '../../2018-09-17-bit-depth/results_32/sample_32_197_x6993_y1729_coeffs.npy')

c95 = np.load('../results_2x/sample_32_205_x6993_y3659_coeffs.npy')
c95t = np.load(
    '../../2018-09-17-bit-depth/results_32/sample_32_205_x6993_y3659_coeffs.npy')

fns = ['odf_2x_sample_{}.png'.format(
    ID, acc) for ID, acc in zip([196, 197, 205], [0.85, 0.90, 0.95])]
fns_t = ['odf_1x_sample_{}.png'.format(ID) for ID in [196, 197, 205]]

save = False
if save:
    for i, c in enumerate([c85, c90, c95]):
        print(fns[i])
        save_odf(fns[i], c)

    for i, c in enumerate([c85t, c90t, c95t]):
        print(fns_t[i])
        save_odf(fns_t[i], c)
