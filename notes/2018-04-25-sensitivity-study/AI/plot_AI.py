import matplotlib.pyplot as plt
from ai_data import AI_data

plt.close('all')

FA = AI_data('AIs_FA.csv', 'FA')
FA.saveall(path='figs/FA/')
FA.plot_AUC(save=True, path='figs/')

westin = AI_data('AIs_westin.csv', 'Westin')
westin.saveall(path='figs/westin/')
