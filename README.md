# uCTdMRI

Tools for using synchrotron microCT images to validate diffusion MRI in whole mouse brains. 

# Axis convention

Assume the shape of the input data is `(n0, n1, n2)`. Each orientation output from
the structure tensor analysis pipeline will be a 3D vector `vec` with `vec[0]`
along the n0 direction, `vec[1]` along the n1 direction, and `vec[2]` along the
n2 direction. 

For expansion onto spherical harmonics and visualization with the fury package,
it is convenient to define these dimensions as a right-handed coordinate system
with `(n0,n1,n2)` corresponding to `(x,y,z)`, where the polar angle $(0,\pi)$ is
formed by cos$^{-1}$(z) and the azimuth $(0,2\pi)$ is formed by tan$^{-1}$(y/x).
