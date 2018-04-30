import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.close()
df = pd.read_csv('AIs.csv', header=0, index_col=[0, 1], skipinitialspace=True)

'''
Boxplots of all four values
'''

with plt.style.context('ggplot'):
    boxfig, boxax = plt.subplots()
    boxax = df.boxplot(column=['Mean', 'Max', 'Mask Mean', 'Mask Max'],
                       grid=False, ax=boxax)
boxax.set_title('AI (Westin Measure)')
boxfig.savefig('boxplots.pdf', bbox_inches='tight')

'''
Constant s_d curves
'''
with plt.style.context('ggplot'):
    sd_fig, sd_axes = plt.subplots(2, 2, figsize=(12, 10))
sd_axes = sd_axes.flatten()


for i, ax in enumerate(sd_axes):
    lines = np.empty(df.index.levels[0].size, dtype=object)
    ax.set_xlabel('$\sigma_N$')
    ax.set_title(df.columns[i])
    for j, s_d in enumerate(df.index.levels[0]):
        lines[j], = ax.plot(df.loc[s_d][df.columns[i]])

labels = [r'$\sigma_D$ = {:.2f}'.format(s_d) for s_d in df.index.levels[0]]
sd_fig.suptitle('AI (Westin Metric) for constant $\sigma_D$')
sd_fig.legend(lines, labels, loc='right')
sd_fig.tight_layout(w_pad=2, h_pad=2)
sd_fig.subplots_adjust(top=0.9, right=0.88)
sd_fig.savefig('constant_s_d.pdf', bbox_inches='tight')

'''
Constant s_N curves
'''
with plt.style.context('ggplot'):
    sn_fig, sn_axes = plt.subplots(2, 2, figsize=(12, 10))
sn_axes = sn_axes.flatten()

for i, ax in enumerate(sn_axes):
    lines = np.empty(df.index.levels[1].size, dtype=object)
    ax.set_xlabel('$\sigma_D$')
    ax.set_title(df.columns[i])
    for j, s_n in enumerate(df.index.levels[1]):
        lines[j], = ax.plot(df.xs(s_n, level=1)[df.columns[i]])

labels = [r'$\sigma_N$ = {:.2f}'.format(s_n) for s_n in df.index.levels[1]]
sn_fig.suptitle('AI (Westin Metric) for constant $\sigma_N$')
sn_fig.legend(lines, labels, loc='right')
plt.tight_layout(w_pad=2, h_pad=2)
sn_fig.subplots_adjust(top=0.9, right=0.88)
sn_fig.savefig('constant_s_n.pdf', bbox_inches='tight')
