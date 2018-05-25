import numpy as np
import dipy.reconst.dti as dti
from dipy.data import get_sphere
from dipy.direction import peaks_from_model
from strtens.hardi import get_data


# Load data
datapath = '../../../data/mri/'
img, data, mask, gtab = get_data(datapath)

# Fit tensor
tenmodel = dti.TensorModel(gtab)
sphere = get_sphere('symmetric724')
tenfit = peaks_from_model(model=tenmodel,
                          data=data,
                          mask=mask,
                          return_odf=True,
                          sh_order=6,
                          sphere=sphere,
                          relative_peak_threshold=0.2,
                          min_separation_angle=25,
                          parallel=True)

np.save('results/dti_shm_coeff', tenfit.shm_coeff)
np.save('results/dti_odf', tenfit.odf)
np.save('results/dti_peak_directions', tenfit.peak_dirs)
np.save('results/dti_peak_values', tenfit.peak_values)
np.save('results/dti_peak_indices', tenfit.peak_indices)
