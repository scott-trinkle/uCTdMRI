import numpy as np
import pandas as pd
from glob import glob


size_AUCs = []
for fn in glob('../../phantoms/different_size/results/*.csv'):
    df = pd.read_csv(fn, skipinitialspace=True)
    size_AUCs.append(df.AUC.min())
    size_AUCs.append(df.AUC.max())

size_ACCs = []
for fn in glob('radius_*_ACC.npy'):
    acc = np.load(fn)
    size_ACCs.append(acc.max())
    size_ACCs.append(acc.min())

size_JSDs = []
for fn in glob('radius_*_JSD.npy'):
    jsd = np.load(fn)
    size_JSDs.append(jsd.max())
    size_JSDs.append(jsd.min())

size_PEs = []
for fn in glob('radius_*_PE.npy'):
    pe = np.load(fn)
    size_PEs.append(pe.max())
    size_PEs.append(pe.min())


with open('size_max_mins.csv', 'w') as f:
    f.write('Max/min,AUC,ACC,JSD,ODF Peak Error\n')
    f.write('max,{auc},{acc},{jsd},{pe}\n'.format(auc=max(size_AUCs),
                                                  acc=max(size_ACCs),
                                                  jsd=max(size_JSDs),
                                                  pe=max(size_PEs)))
    f.write('min,{auc},{acc},{jsd},{pe}\n'.format(auc=min(size_AUCs),
                                                  acc=min(size_ACCs),
                                                  jsd=min(size_JSDs),
                                                  pe=min(size_PEs)))

for deg in range(15, 86, 10):
    if (deg == 15) | (deg == 35):
        break
    print(deg)


angle_AUCs = []
for fn in glob('../../phantoms/crossing_fibers/results/*.csv'):
    df = pd.read_csv(fn, skipinitialspace=True)
    angle_AUCs.append(df.AUC.min())
    angle_AUCs.append(df.AUC.max())

angle_ACCs = []
for fn in glob('angle_*_ACC.npy'):
    acc = np.load(fn)
    angle_ACCs.append(acc.max())
    angle_ACCs.append(acc.min())

angle_JSDs = []
for fn in glob('angle_*_JSD.npy'):
    jsd = np.load(fn)
    angle_JSDs.append(jsd.max())
    angle_JSDs.append(jsd.min())

angle_PEs = []
for fn in glob('angle_*_PE.npy'):
    pe = np.load(fn)
    angle_PEs.append(pe.max())
    angle_PEs.append(pe.min())


with open('angle_max_mins.csv', 'w') as f:
    f.write('Max/min,AUC,ACC,JSD,ODF Peak Error\n')
    f.write('max,{auc},{acc},{jsd},{pe}\n'.format(auc=max(angle_AUCs),
                                                  acc=max(angle_ACCs),
                                                  jsd=max(angle_JSDs),
                                                  pe=max(angle_PEs)))
    f.write('min,{auc},{acc},{jsd},{pe}\n'.format(auc=min(angle_AUCs),
                                                  acc=min(angle_ACCs),
                                                  jsd=min(angle_JSDs),
                                                  pe=min(angle_PEs)))
