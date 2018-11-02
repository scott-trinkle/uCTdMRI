for i in range(15):
    with open('save_vectors_{}.py'.format(i), 'w') as f:
        f.write('''
import numpy as np
from strtens import StructureTensor
from skimage import io

bunch_num={}'''.format(i))
        f.write('''
start_slice=10000

starts=np.load('inds/starts.npy')
stops=np.load('inds/stops.npy')
buf_starts=np.load('inds/buf_starts.npy')
buf_stops=np.load('inds/buf_stops.npy')

start=starts[bunch_num] + start_slice
stop=stops[bunch_num] + start_slice
buf_start=buf_starts[bunch_num] + start_slice
buf_stop=buf_stops[bunch_num] + start_slice

print('Reading image')
im=[]
app=im.append
for i in range(buf_start, buf_stop + 1):
    fn='./data_AC_crop/crop_recon_' + str(i) + '.tiff'
    temp=io.imread(fn)
    app(temp)
im=np.array(im)

FA, vectors=StructureTensor(im, verbose=True).results()

print('Saving FA')
np.save('FA/FA_{}'.format(bunch_num), FA)
print('Saving vectors')
np.save('vectors/vectors_{}'.format(bunch_num), vectors)''')

    with open('calc_coeffs_{}.py'.format(i), 'w') as f:
        f.write('''
import numpy as np
from strtens import odftools

batch_num = {}'''.format(i))
        f.write('''

print('Reading FA')
FA = np.load('./FA_chopped/FA_chopped_{}.npy'.format(batch_num))
print('FA shape: {}'.format(FA.shape))

print('Reading vectors')
vecs = np.load('./vectors_chopped/vectors_chopped_{}.npy'.format(batch_num))
print('Vectors shape: {}'.format(vecs.shape))

threshold = 0.69

vox_size = 125
nz, ny, nx = np.array(vecs.shape[:-1]) // vox_size
ny += 1  # empirical, have one normal and one small voxel, rather than one big

coeff_array = []
app = coeff_array.append
for i in range(ny):
    for j in range(nx):
        print(i, j)
        y0 = vox_size * i
        yf = y0 + vox_size
        x0 = vox_size * j
        xf = x0 + vox_size
        if i == ny - 1:
            yf = -1
        if j == nx - 1:
            xf = -1
        temp_vec = vecs[:, y0:yf, x0:xf]
        temp_vec = temp_vec[FA[:, y0:yf, x0:xf] > threshold]
        app(odftools.get_SH_coeffs(temp_vec))
coeff_array = np.array(coeff_array).reshape((ny, nx, -1))
np.save('./coeffs/coeffs_{}'.format(batch_num), coeff_array)''')
