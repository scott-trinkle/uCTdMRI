import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from strtens import odftools


def c_ST_fn(deg):
    return '../../../2018-05-22-tuning-parameters/phantoms/crossing_fibers/results/deg{}coeffs.npy'.format(deg)


def c_true_fn(deg):
    return '../../../2018-05-22-tuning-parameters/phantoms/crossing_fibers/true_coeffs/z_phantom_nfib9x4_r8_{}deg_coeffs.npy'.format(deg)


# sphere = odftools.make_sphere(1500)
# with open('sens_results.csv', 'w') as f:
#     f.write('Deg, ACC, Peak_Diff\n')
#     for deg in range(25, 86, 10):
#         print(deg)
#         c_ST = np.load(c_ST_fn(deg))
#         c_true = np.load(c_true_fn(deg))

#         odf_ST = odftools.get_odf(c_ST[282], sphere)

#         peaks_ST, _, _ = odftools.get_peaks(odf_ST, sphere)

#         offset_theta = deg * np.pi / 180
#         actual_peaks = np.array([[0, 0, 1],
#                                  [np.sin(offset_theta), 0, -np.cos(offset_theta)]])

#         diff_ST = odftools.get_ang_distance(actual_peaks, peaks_ST)

#         acc = odftools.calc_ACC(c_ST[282], c_true)

#         f.write('{}, {:.6f}, {:.6f}\n'.format(deg, acc, diff_ST.mean()))


df = pd.read_csv('sens_results.csv', index_col=0, skipinitialspace=True)
c1 = 'C0'
c2 = 'C3'

with plt.style.context('seaborn-poster'):
    fig, ax1 = plt.subplots()
    ax1.set_title('Structure Tensor FOD Sensitivity')
    ax1.set_xticks(range(25, 86, 10))

    ax1.plot(df['Peak_Diff'], 'o', color=c1)
    ax1.set_xlabel('Crossing angle (degrees)')
    ax1.set_ylabel('Average angular error (degrees)', color=c1)
    ax1.tick_params('y', colors=c1)
    ax1.set_ylim([0, 10])

    ax2 = ax1.twinx()
    ax2.plot(df['ACC'], 's', color=c2)
    ax2.set_ylabel('Angular Correlation Coefficient', color=c2)
    ax2.tick_params('y', colors=c2)
    ax2.set_ylim([0, 1])

    plt.tight_layout()
    plt.savefig('st_fod_sensitivity.pdf')
