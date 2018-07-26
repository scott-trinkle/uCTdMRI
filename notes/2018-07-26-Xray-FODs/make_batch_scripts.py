import numpy as np

starts = np.insert(np.arange(75, 6576, 100), 0, 0)
stops = np.append(np.arange(125, 6626, 100), 6640)


for i, (start, stop) in enumerate(zip(starts, stops)):
    py_fn = 'ST_batch_{:0>2d}_sl_{}-{}.py'.format(i + 1, start, stop)
    with open('scripts/' + py_fn, 'w') as f:
        f.write('import numpy as np\n')
        f.write('from strtens import StructureTensor\n')
        f.write('from strtens.util import read_tif_stack\n\n')
        f.write('i = {}\n'.format(i + 1))
        f.write('start = {}\n'.format(start))
        f.write('stop = {}\n\n'.format(stop))
        f.write('print("Reading image")\n')
        f.write(
            'im = read_tif_stack("../../../data/xray/recon_2x/recon_2x_", start=start, stop=stop)\n')
        f.write('print("Calculating Structure Tensor")\n')
        f.write('FA, orientations = StructureTensor(im).results()\n\n')
        f.write('print("Saving")\n')
        f.write(
            'np.save("../FA/FA_batch_{:0>2d}_sl_{}-{}".format(i, start, stop), FA)\n')
        f.write(
            'np.save("../orientations/orientations_batch_{:0>2d}_sl_{}-{}".format(i, start, stop), orientations)\n')

    sh_fn = 'ST_batch_{:0>2d}.sh'.format(i + 1)
    with open('scripts/' + sh_fn, 'w') as f:
        f.write('#!/bin/sh\n')
        f.write('#$ -j y\n')
        f.write('#$ -cwd\n')
        f.write('#$ -V\n\n')
        f.write('outfile={}\n\n'.format(sh_fn.split(".")[0] + ".out"))
        f.write('runhost="$(hostname | cut -f1 -d.)"\n')
        f.write('''rundate="$(date '+ %m/%d/%y %H:%M')"\n''')
        f.write('echo "Batch job started on $runhost on $rundate" > $outfile\n\n')
        f.write('python {} >> $outfile\n'.format(py_fn))
        f.write('echo "Batch job completed on $rundate" >> $outfile')
