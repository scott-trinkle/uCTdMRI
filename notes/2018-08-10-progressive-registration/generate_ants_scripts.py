def write_siraf_ants_call(fn, fixedfn, movingfn, node=None, threads=16,
                          transform='s', precision='d'):

    with open(fn, 'w') as f:
        f.write('#!/bin/sh\n')
        f.write('#$ -j y\n')
        f.write('#$ -cwd\n')
        f.write('#$ -V\n')
        if node is not None:
            f.write('#$ -l h={}\n'.format(node))
        f.write('\n')

        f.write('regname={}\n'.format(fn.split('.sh')[0]))
        f.write('outfile=$regname.out\n')
        f.write('runhost="$(hostname | cut -f1 -d.)"\n')
        f.write('''rundate="$(date '+ %m/%d/%y %H:%M')"\n''')
        f.write('echo "Batch job started on $runhost on $rundate" > $outfile\n\n')

        f.write('fixed={}\n'.format(fixedfn))
        f.write('moving={}\n'.format(movingfn))
        f.write('threads={}\n'.format(threads))
        f.write('transform={}\n'.format(transform))
        f.write('precision={}\n\n'.format(precision))

        f.write('antsRegistrationSyN.sh -d 3 -f $fixed -m $moving -o $regname -n $threads -t $transform -p $precision >> $outfile\n\n')
        f.write('''enddate="$(date '+ %m/%d/%y %H:%M')"\n''')
        f.write('echo "Batch job ended on $runhost on $enddate" >> $outfile')


resolutions = [15, 20, 25, 40, 50, 60, 75, 100, 150]
data_path = 'data/'
script_path = 'scripts/'
for res in resolutions:
    for interp in ['no_interp', 'bilinear', 'bicubic']:
        write_siraf_ants_call(script_path + '{}_{}.sh'.format(interp, res),
                              fixedfn=data_path +
                              'mri_{}um_{}.nii'.format(res, interp),
                              movingfn=data_path + 'recon_{}um.nii'.format(res))
