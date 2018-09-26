import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from glob import glob
import strtens.odftools as odftools
from strtens.vis import show_ODF

ids8 = ['sample_8_{}'.format(i) for i in range(1, 10)]
sphere = odftools.make_sphere(1200)

df = pd.DataFrame(columns=['ACC', 'JSD', 'MSE'])
for ID in range(1, 10):
    print(ID)
    print('Calculating metrics')
    c32 = np.load('results/sample_32_{}_coeffs.npy'.format(ID))
    c8 = np.load('results/sample_8_{}_coeffs.npy'.format(ID))
    ACC = odftools.calc_ACC(c32, c8)
    JSD = odftools.calc_JSD(c32, c8, sphere)
    MSE = ((c32 - c8) ** 2).mean()
    df.loc[ID] = [ACC, JSD, MSE]

    print('Saving ODFs')
    odf32 = odftools.get_odf(c32, sphere)
    odf8 = odftools.get_odf(c8, sphere)
    show_ODF(odf32, sphere, save=True, interactive=False,
             fn='results/odfs/sample_32_{}.png'.format(ID))
    show_ODF(odf8, sphere, save=True, interactive=False,
             fn='results/odfs/sample_8_{}.png'.format(ID))


df.loc['Mean'] = df.mean()
df = df.iloc[:-1]

acc = df.ACC
jsd = 1 / df.JSD
jsd = jsd - jsd.min()
jsd = jsd / jsd.max()
mse = 1 / df.MSE
mse = mse - mse.min()
mse = mse / mse.max()
plt.plot(acc, label='acc')
plt.plot(jsd, label='jsd')
plt.plot(mse, label='mse')
plt.legend()
plt.show()
