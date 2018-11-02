
import numpy as np
import matplotlib.pyplot as plt

for i in range(14, 15):
    fn = './FA/FA_{}.npy'.format(i)
    if i == 0:
        start = 0
        stop = -50
    elif i == 14:
        start = 50
        stop = -1
    else:
        start = 50
        stop = -50

    print(i)
    print('Reading')
    im = np.load(fn)
    im = im[start:stop]
    print('Saving')
    np.save('FA_chopped/FA_chopped_{}'.format(i), im)

for i in range(14, 15):
    fn = './vectors/vectors_{}.npy'.format(i)
    if i == 0:
        start = 0
        stop = -50
    elif i == 14:
        start = 50
        stop = -1
    else:
        start = 50
        stop = -50

    print(i)
    print('Reading')
    im = np.load(fn)
    im = im[start:stop]
    print('Saving')
    np.save('vectors_chopped/vectors_chopped_{}'.format(i), im)
