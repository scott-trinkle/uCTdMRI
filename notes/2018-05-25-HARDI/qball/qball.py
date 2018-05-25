import numpy as np
from strtens.hardi import get_data
from dipy.data import get_sphere
from dipy.reconst.shm import CsaOdfModel
from dipy.direction import peaks_from_model

datapath = '../../../data/mri/'
img, data, mask, gtab = get_data(datapath)

qballmodel = CsaOdfModel(gtab, sh_order=6)
sphere = get_sphere('symmetric724')

qballfit = peaks_from_model(model=qballmodel,
                            data=data,
                            mask=mask,
                            sphere=sphere,
                            relative_peak_threshold=0.2,
                            min_separation_angle=25,
                            return_odf=True,
                            parallel=True)

# Remove negative values
odfs = np.clip(qballfit.odf, 0, np.max(qballfit.odf, -1)[..., None])

np.save('results/qball_shm_coeff', qballfit.shm_coeff)
np.save('results/qball_odf', odfs)
np.save('results/qball_peak_directions', qballfit.peak_dirs)
np.save('results/qball_peak_values', qballfit.peak_values)
np.save('results/qball_peak_indices', qballfit.peak_indices)
