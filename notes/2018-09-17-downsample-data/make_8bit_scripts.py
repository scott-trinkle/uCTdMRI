import numpy as np

num_slices = 11098
n_nodes = 6
d_sl = np.ceil(num_slices / n_nodes).astype(int)
bounds = [[i * d_sl + 1, (i + 1) * d_sl] for i in range(n_nodes)]
bounds[0][0] = 0
bounds[-1][-1] = -1
nodes = ['bigmem1', 'bigmem2', 'bigmem3', 'bigmem4', 'bignode3', 'bignode4']

for i in range(n_nodes):
    with open('to_8bit/to_8bit_{}.py'.format(i+1), 'w') as f:
        f.write('import os\n')
        f.write('import numpy as np\n')
        f.write('import tifffile as tf\n\n')

        f.write(
            "outdir = '../../../Data/2018_06_08_WholeBrainBK_Redtube/recon_flatcorr_1x/recon_8bit/'\n")
        f.write('if not os.path.isdir(outdir):\n')
        f.write('    os.mkdir(outdir)\n\n')

        f.write('min_t, max_t = np.load("results/maxmin.npy")\n\n')

        f.write('start = {}\n'.format(bounds[i][0]))
        f.write('stop = {}\n\n'.format(bounds[i][1]))

        f.write(
            "fns=['../../../Data/2018_06_08_WholeBrainBK_Redtube/recon_flatcorr_1x/recon/recon_{:0>5d}.tiff'.format(i) for i in range(start, stop + 1)]\n\n")

        f.write('for fn in fns:\n')
        f.write('    im = tf.imread(fn)\n')
        f.write('    im = (255 * (im - min_t) / (max_t - min_t)).astype(np.uint8)\n')
        f.write(
            '    outfn = outdir + "recon_8bit_" + fn.split("/")[1].split("_")[1]\n')
        f.write('    tf.imsave(outfn, im)')

    sh_fn = 'to_8bit_{:0>2d}.sh'.format(i + 1)
    with open('to_8bit/' + sh_fn, 'w') as f:
        f.write('#!/bin/sh\n')
        f.write('#$ -j y\n')
        f.write('#$ -cwd\n')
        f.write('#$ -V\n')
        f.write('#$ -l h={}\n\n'.format(nodes[i]))

        f.write('outfile={}\n\n'.format(sh_fn.split(".")[0] + ".out"))

        f.write('runhost="$(hostname | cut -f1 -d.)"\n')
        f.write('''rundate="$(date '+ %m/%d/%y %H:%M')"\n''')
        f.write('echo "Batch job started on $runhost on $rundate" > $outfile\n\n')

        f.write('python to_8bit_{}.py >> $outfile\n\n'.format(i+1))

        f.write('''enddate="$(date '+ %m/%d/%y %H:%M')"\n''')
        f.write('echo "Batch job completed on $enddate" >> $outfile')
