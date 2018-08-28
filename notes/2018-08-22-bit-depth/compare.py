import numpy as np
import pandas as pd
from glob import glob
import strtens.odftools as odftools

ids = ['sample{}'.format(i) for i in range(1, 4)]
sphere = odftools.make_sphere(1200)

df = pd.DataFrame(columns=['ACC', 'JSD', 'MSE'])
for ID in ids:
    c32 = np.load('results/{}_coeffs.npy'.format(ID))
    c8 = np.load('results/{}_8_coeffs.npy'.format(ID))
    ACC = odftools.calc_ACC(c32, c8)
    JSD = odftools.calc_JSD(c32, c8, sphere)
    MSE = ((c32 - c8) ** 2).mean()
    df.loc[ID] = [ACC, JSD, MSE]

df.loc['Mean'] = df.mean()
