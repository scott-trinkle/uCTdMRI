import numpy as np
import tifffile as tf
from glob import glob

vox_size = 125
buf = 50
n = 1873

real_starts = vox_size * np.arange(int(n / vox_size + 0.5))
np.save('inds/starts', real_starts)
real_stops = real_starts + vox_size - 1
np.save('inds/stops', real_stops)

calc_starts = real_starts - buf
calc_starts[calc_starts < 0] = 0
np.save('inds/buf_starts', calc_starts)
calc_stops = real_stops + buf
calc_stops[calc_stops > n] = n
np.save('inds/buf_stops', calc_stops)
