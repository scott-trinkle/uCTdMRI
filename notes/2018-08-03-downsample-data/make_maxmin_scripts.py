import os
import numpy as np

outdir = 'maxmin/'
if not os.path.isdir(outdir):
    os.mkdir(outdir)
results_dir = 'maxmin/results/'
if not os.path.isdir(results_dir):
    os.mkdir(results_dir)


num_slices = 11098
n_nodes = 6
d_sl = np.ceil(num_slices / n_nodes).astype(int)
bounds = [[i * d_sl + 1, (i + 1) * d_sl] for i in range(n_nodes)]
bounds[0][0] = 0
bounds[-1][-1] = -1
nodes = ['bigmem1', 'bigmem2', 'bigmem3', 'bigmem4', 'bignode3', 'bignode4']

for i in range(n_nodes):
    with open('maxmin/get_maxmin_{}.py'.format(i+1), 'w') as f:
        f.write('import os\n')
        f.write('from tifffile import imread\n\n')

        f.write('start = {}\n'.format(bounds[i][0]))
        f.write('stop = {}\n\n'.format(bounds[i][1]))

        f.write(
            "fns=['../../../../Data/2018_06_08_WholeBrainBK_Redtube/recon_flatcorr_1x/recon/recon_{:0>5d}.tiff'.format(i) for i in range(start, stop + 1)]\n\n")

        f.write("with open('maxmin/results/batch_{}.csv', 'w') as f:\n".format(i+1))
        f.write("    f.write('fn, max, min')\n")
        f.write("    for fn in fns:\n")
        f.write("        sl = fn.split('/')[-1].split('.')[0]\n")
        f.write("        im = imread(fn)\n")
        f.write("        f.write(sl + ',{},{}'.format(im.max(), im.min()))\n")

    sh_fn = 'maxmin_{:0>2d}.sh'.format(i + 1)
    with open('maxmin/' + sh_fn, 'w') as f:
        f.write('#!/bin/sh\n')
        f.write('#$ -j y\n')
        f.write('#$ -cwd\n')
        f.write('#$ -V\n')
        f.write('#$ -l h={}\n\n'.format(nodes[i]))

        f.write('outfile={}\n\n'.format(sh_fn.split(".")[0] + ".out"))

        f.write('runhost="$(hostname | cut -f1 -d.)"\n')
        f.write('''rundate="$(date '+ %m/%d/%y %H:%M')"\n''')
        f.write('echo "Batch job started on $runhost on $rundate" > $outfile\n\n')

        f.write('python get_maxmin_{}.py >> $outfile\n\n'.format(i+1))

        f.write('''enddate="$(date '+ %m/%d/%y %H:%M')"\n''')
        f.write('echo "Batch job completed on $enddate" >> $outfile')
