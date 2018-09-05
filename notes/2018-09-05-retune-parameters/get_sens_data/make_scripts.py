for deg in range(15, 86, 10):
    with open('deg{}.py'.format(deg), 'w') as f:
        f.write('from sensitivity_funcs import crossing_sensitivity\n')
        f.write('import numpy as np\n\n')

        f.write('sds = np.arange(1, 21) / 1.2\n')
        f.write('sns = np.arange(1, 21) / 1.2\n\n')

        f.write(
            'imfn = "../phantoms/crossing_fibers/phants/z_phantom_nfib9x4_r8_{}deg.tif"\n'.format(deg))
        f.write(
            'maskfn = "../phantoms/crossing_fibers/masks/z_phantom_mask_nfib9x4_r8_{}deg.tif"\n'.format(deg))
        f.write(
            'resultspath = "../phantoms/crossing_fibers/results/deg{}"\n\n'.format(deg))

        f.write('peak_data=crossing_sensitivity(imfn, maskfn, resultspath, sds, sns)')

    with open('deg{}.sh'.format(deg), 'w') as f:
        f.write('#!/bin/sh\n')
        f.write('#$ -j y\n')
        f.write('#$ -cwd\n')
        f.write('#$ -V\n\n')

        f.write('python < deg{}.py'.format(deg))

for r in range(4, 17, 4):
    with open('r{}.py'.format(r), 'w') as f:
        f.write('from sensitivity_funcs import sensitivity\n')
        f.write('import numpy as np\n\n')

        f.write('sds = np.arange(1, 21) / 1.2\n')
        f.write('sns = np.arange(1, 21) / 1.2\n\n')

        f.write(
            'imfn = "../phantoms/different_size/phants/x_phantom_nfib9_r{}.tif"\n'.format(r))
        f.write(
            'maskfn = "../phantoms/different_size/masks/x_phantom_nfib9_r{}.tif"\n'.format(r))
        f.write(
            'resultspath = "../phantoms/different_size/results/r{}"\n'.format(r))

        f.write('peak_data=sensitivity(imfn, maskfn, resultspath, sds, sns)')

    with open('r{}.sh'.format(r), 'w') as f:
        f.write('#!/bin/sh\n')
        f.write('#$ -j y\n')
        f.write('#$ -cwd\n')
        f.write('#$ -V\n\n')

        f.write('python < r{}.py'.format(r))
