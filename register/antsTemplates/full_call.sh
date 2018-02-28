mri=/path/to/fixed (MRI)
xray=/path/to/moving (xray)


antsRegistration --dimensionality 3 \
    --float 0 \
    --output [linear_transform_] \  # replace with [transform, warped, inverse_warped (i think)]
    --interpolation Linear \
    --use-histogram-matching 0 \
    --save-state 0 \
    --write-composite-transform 1 \
    --collapse-output-transforms 1 \
    --winsorize-image-intensities [0.005,0.995] \
    --initial-moving-transform [${mri},${xray},1] \  # replace with /path/to/linear/transform if needbe
    --transform Rigid[0.1] \
    --metric MI[${mri},${xray},1,32,Regular,0.25] \
    --convergence [1000x1000x1000x1000,1e-6,10] \
    --shrink-factors 8x4x2x1 \
    --smoothing-sigmas 3x2x1x0vox \
    --transform Affine[0.1] \
    --metric MI[${mri},${xray},1,32,Regular,0.25] \
    --convergence [1000x1000x1000x1000,1e-6,10] \
    --shrink-factors 8x4x2x1 \
    --smoothing-sigmas 3x2x1x0vox \
    --transform SyN[0.1,3,0] \
    --metric CC[${mri}, ${xray}, 1, 4] \
    --convergence [100x100x70x50x20,1e-6,10] \
    --shrink-factors 10x6x4x2x1 \
    --smoothing-sigmas 5x3x2x1x0vox
