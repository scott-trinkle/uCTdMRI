regname=outputname
outfile=$regname.out 
mri=/path/to/fixed (MRI)
xray=/path/to/moving (xray)
threads=numberofthreads
transform= # 's' for rigid + affine + deformable, 'a' for rigid + affine 
precision= # 'f' for float, 'd' for double

antsRegistrationSyN.sh -d 3 -f $mri -m $xray -o $regname -n $threads -t $transform -p $precision >> $outfile
