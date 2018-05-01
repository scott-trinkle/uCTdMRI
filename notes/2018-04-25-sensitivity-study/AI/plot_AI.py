import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('default')
plt.close()


class AI_data(object):
    def __init__(self, csvfn, metric, plotall=False):
        self.data = pd.read_csv(csvfn, header=0, index_col=[
                                0, 1], skipinitialspace=True)
        self.metric = metric

        if plotall:
            self.boxplot()
            self.plot_AI_vs_sn()
            self.plot_AI_vs_sd()
            self.plot_diff()

    def boxplot(self, fn=None):
        '''
        Boxplots of all four values
        '''
        fig, ax = plt.subplots(figsize=(10, 8))
        ax = self.data.boxplot(grid=False, ax=ax)
        ax.set_title('AI ({} Measure)'.format(self.metric))
        if fn is None:
            fn = '{}_boxplots.pdf'.format(self.metric)
        fig.savefig(fn, bbox_inches='tight')

    def plot_AI_vs_sn(self, fn=None):
        '''
        Plots AI vs. s_n for each s_d
        '''
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes = axes.flatten()

        for i, ax in enumerate(axes):
            lines = np.empty(self.data.index.levels[0].size, dtype=object)
            ax.set_xlabel('$\sigma_N$')
            ax.set_ylabel('AI')
            ax.set_title(self.data.columns[i+2])
            for j, s_d in enumerate(self.data.index.levels[0]):
                lines[j], = ax.plot(self.data.loc[s_d][self.data.columns[i+2]])

        labels = [r'$\sigma_D$ = {:.2f}'.format(
            s_d) for s_d in self.data.index.levels[0]]
        fig.suptitle('AI ({} Metric) vs. $\sigma_N$'.format(self.metric))
        fig.legend(lines, labels, loc='right')
        fig.tight_layout(w_pad=2, h_pad=2)
        fig.subplots_adjust(top=0.9, right=0.88)
        if fn is None:
            fn = '{}_AI_vs_sn.pdf'.format(self.metric)
        fig.savefig(fn, bbox_inches='tight')

    def plot_AI_vs_sd(self, fn=None):
        '''
        Plots AI vs s_d for each s_n
        '''

        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes = axes.flatten()

        for i, ax in enumerate(axes):
            lines = np.empty(self.data.index.levels[1].size, dtype=object)
            ax.set_xlabel('$\sigma_D$')
            ax.set_ylabel('AI')
            ax.set_title(self.data.columns[i+2])
            for j, s_n in enumerate(self.data.index.levels[1]):
                lines[j], = ax.plot(self.data.xs(s_n, level=1)[
                                    self.data.columns[i+2]])

        labels = [r'$\sigma_N$ = {:.2f}'.format(
            s_n) for s_n in self.data.index.levels[1]]
        fig.suptitle(
            'AI ({} Metric) for constant $\sigma_N$'.format(self.metric))
        fig.legend(lines, labels, loc='right')
        plt.tight_layout(w_pad=2, h_pad=2)
        fig.subplots_adjust(top=0.9, right=0.88)
        if fn is None:
            fn = '{}_AI_vs_sd.pdf'.format(self.metric)
        fig.savefig(fn, bbox_inches='tight')

    def plot_diff(self, fn=None):
        '''
        Difference curves
        '''

        fig, axes = plt.subplots(1, 2, figsize=(14, 8))
        axes = axes.flatten()
        lines = np.empty(self.data.index.levels[1].size, dtype=object)

        for j, s_d in enumerate(self.data.index.levels[0]):
            diff = self.data.loc[s_d]['Mask Mean'] - \
                self.data.loc[s_d]['Inv Mask Mean']
            lines[j], = axes[0].plot(diff)

        axes[0].set_xlabel('$\sigma_N$')
        axes[0].set_ylabel(r'$\bar{AI}_{mask} - \bar{AI}_{inv mask}$')
        axes[0].set_title(
            '(Mean mask AI - mean inverse mask AI) vs. $\sigma_N$')

        for j, s_n in enumerate(self.data.index.levels[1]):
            diff = self.data.xs(s_n, level=1)['Mask Mean'] - \
                self.data.xs(s_n, level=1)['Inv Mask Mean']
            lines[j], = axes[1].plot(diff)

        axes[1].set_xlabel('$\sigma_D$')
        axes[1].set_ylabel(r'$\bar{AI}_{mask} - \bar{AI}_{inv mask}$')
        axes[1].set_title(
            '(Mean mask AI - mean inverse mask AI) vs. $\sigma_D$')

        fig.suptitle('AI Improvement in Mask ({} Metric)'.format(self.metric))

        labels = [r'$\sigma$ = {:.2f}'.format(
            s_n) for s_n in self.data.index.levels[1]]
        fig.legend(lines, labels, loc='right')

        plt.tight_layout(w_pad=2, h_pad=2)
        fig.subplots_adjust(top=0.9, right=0.88)
        if fn is None:
            fn = '{}_difference.pdf'.format(self.metric)
        fig.savefig(fn, bbox_inches='tight')


FA = AI_data('AIs_FA.csv', 'FA', plotall=True)
Westin = AI_data('AIs_westin.csv', 'Westin', plotall=True)
