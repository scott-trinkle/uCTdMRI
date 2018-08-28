def write_apply_script(fn, res, fixedfn, movingfn,
                       lineartransfile, deformtransfile, node=None):

    with open(fn, 'w') as f:
        f.write('#!/bin/sh\n')
        f.write('#$ -j y\n')
        f.write('#$ -cwd\n')
        f.write('#$ -V\n')
        if node is not None:
            f.write('#$ -l h={}\n\n'.format(node))
        else:
            f.write('\n')

        f.write('regname={}_{}_sampled\n'.format(interp, res))
        f.write('outfile=${regname}.out\n\n')

        f.write('runhost="$(hostname | cut -f1 -d.)"\n')
        f.write('''rundate="$(date '+ %m/%d/%y %H:%M')"\n''')
        f.write('echo "Batch job started on $runhost on $rundate" > $outfile\n\n')

        f.write('fixed=../../{}\n'.format(fixedfn))
        f.write('moving=../../{}\n\n'.format(movingfn))

        f.write('lineartransformfile={}\n'.format(lineartransfile))
        f.write('deformfile={}\n\n'.format(deformtransfile))

        f.write('antsApplyTransforms --dimensionality 3')
        f.write('    --input-image-type 0')
        f.write('    --input $moving')
        f.write('    --reference-image $fixed')
        f.write('    --output ${regname}_Warped.nii.gz')
        f.write('    --interpolation Linear')
        f.write('    --transform $deformfile')
        f.write('    --transform $lineartransformfile')
        f.write('    --float 0')
        f.write('    --verbose 1 >> $outfile\n\n')

        f.write('''enddate="$(date '+ %m/%d/%y %H:%M')"\n''')
        f.write('echo "Batch job ended on $runhost on $enddate" >> $outfile\n')


resolutions = [15, 20, 25, 40, 60, 75, 100, 150]
data_path = 'data/'
for res in resolutions:
    for interp in ['no_interp', 'bilinear', 'bicubic']:
        fn = 'registrations/{0}_{1}/{0}_{1}_sampled.sh'.format(interp, res)
        fixedfn = 'data/mri_{0}um_{1}.nii'.format(res, interp)
        movingfn = 'data/recon_{}um.nii'.format(res)
        lineartransfile = '{0}_{1}0GenericAffine.mat'.format(interp, res)
        deformtransfile = 'sampled_{0}_{1}1Warp.nii'.format(interp, res)
        write_apply_script(fn, res, fixedfn, movingfn,
                           lineartransfile, deformtransfile)
