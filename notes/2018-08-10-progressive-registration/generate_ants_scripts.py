import os


def write_siraf_ants_call(fn, fixedfn, movingfn, node=None, threads=8,
                          transform='s', precision='d'):

    with open(fn, 'w') as f:
        f.write('#!/bin/sh\n')
        f.write('#$ -j y\n')
        f.write('#$ -cwd\n')
        f.write('#$ -V\n')
        if node is not None:
            f.write('#$ -l h={}\n'.format(node))
        f.write('\n')

        f.write('regname={}\n'.format(fn.split('/')[-1].split('.sh')[0]))
        f.write('outfile=$regname.out\n')
        f.write('runhost="$(hostname | cut -f1 -d.)"\n')
        f.write('''rundate="$(date '+ %m/%d/%y %H:%M')"\n''')
        f.write('echo "Batch job started on $runhost on $rundate" > $outfile\n\n')

        f.write('fixed=../../{}\n'.format(fixedfn))
        f.write('moving=../../{}\n'.format(movingfn))
        f.write('threads={}\n'.format(threads))
        f.write('transform={}\n'.format(transform))
        f.write('precision={}\n\n'.format(precision))

        f.write('antsRegistrationSyN.sh -d 3 -f $fixed -m $moving -o $regname -n $threads -t $transform -p $precision >> $outfile\n\n')
        f.write('''enddate="$(date '+ %m/%d/%y %H:%M')"\n''')
        f.write('echo "Batch job ended on $runhost on $enddate" >> $outfile')


resolutions = [15, 20, 25, 40, 50, 60, 75, 100, 150]
data_path = 'data/'
reg_path = 'registrations/'
if not os.path.isdir(reg_path):
    os.mkdir(reg_path)


for res in resolutions:
    if res == 50:
        if not os.path.isdir(reg_path + 'reg_50um/'):
            os.mkdir(reg_path + 'reg_50um/')
        write_siraf_ants_call(reg_path + 'reg_50um/reg_50um.sh',
                              fixedfn=data_path + 'mri_50um.nii',
                              movingfn=data_path + 'recon_50um.nii')
    else:
        for interp in ['no_interp', 'bilinear', 'bicubic']:
            name = '{}_{}'.format(interp, res)
            path = reg_path + name + '/'
            if not os.path.isdir(path):
                os.mkdir(path)
            fn = path + name + '.sh'
            fixedfn = data_path + 'mri_{}um_{}.nii'.format(res, interp)
            movingfn = data_path + 'recon_{}um.nii'.format(res)

            write_siraf_ants_call(fn,
                                  fixedfn=fixedfn,
                                  movingfn=movingfn)
