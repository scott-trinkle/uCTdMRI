mri=/path/to/fixed (MRI)
xray=/path/to/moving (xray)

regname=my_deform
outfile=${regname}.out

lineartransformfile=/path/to/linear/transform
deformfile=/path/to/nonlinear/transform


# Remember, transforms are applied in reverse order

antsApplyTransforms --dimensionality 3 \
    --input-image-type 0 \  # scalar, vector, time-series, etc. 
    --input $xray \
    --reference-image $mri \
    --output ${regname}_Warped.nii.gz \
    --interpolation Linear \
    --transform $deformfile \
    --transform $lineartransformfile \
    --float 0 \
    --verbose 1 # >> $outfile
