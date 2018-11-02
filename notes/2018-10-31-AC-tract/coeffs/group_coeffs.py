import numpy as np
fns = ['./coeffs_{}.npy'.format(i) for i in range(15)]

c = []
for fn in fns:
    print(fn)
    c.append(np.load(fn))
c = np.array(c)
np.save('coeffs_full', c)
