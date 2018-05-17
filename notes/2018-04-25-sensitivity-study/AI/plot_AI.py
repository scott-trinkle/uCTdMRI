import numpy as np
import matplotlib.pyplot as plt
from ai_data import AI_data

plt.close('all')

FA = AI_data('AIs_FA.csv', 'FA')
FA.saveall(path='figs/FA/')

westin = AI_data('AIs_westin.csv', 'Westin')
westin.saveall(path='figs/westin/')
