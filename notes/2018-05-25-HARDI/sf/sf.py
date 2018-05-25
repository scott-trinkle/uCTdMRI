import numpy as np
from strtens.hardi import get_data
import dipy.reconst.sfm as sfm
from dipy.reconst.csdeconv import auto_response
from dipy.data import get_sphere
from dipy.direction.peaks import peaks_from_model

datapath = '../../../data/mri/'
img, data, mask, gtab = get_data(datapath)


# Getting fiber response function from center of brain
center_response, ratio = auto_response(gtab, data, roi_radius=10, fa_thr=0.7)
if center_response[0][1] != center_response[0][2] or (ratio > 0.25):
    raise ValueError('Might want to find a different response function')

sphere = get_sphere('symmetric724')
sf_model = sfm.SparseFascicleModel(gtab,
                                   sphere=sphere,
                                   l1_ratio=0.5,
                                   alpha=0.001,
                                   response=center_response[0])

sf_fit = peaks_from_model(sf_model,
                          data=data,
                          mask=mask,
                          return_odf=True,
                          sh_order=6,
                          sphere=sphere,
                          relative_peak_threshold=0.2,
                          min_separation_angle=25,
                          parallel=True)

np.save('results/sf_shm_coeff', sf_fit.shm_coeff)
np.save('results/sf_odf', sf_fit.odf)
np.save('results/sf_peak_directions', sf_fit.peak_dirs)
np.save('results/sf_peak_values', sf_fit.peak_values)
np.save('results/sf_peak_indices', sf_fit.peak_indices)
