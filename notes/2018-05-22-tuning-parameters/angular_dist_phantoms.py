import numpy as np


def rand_vectors(n):
    costheta = np.random.uniform(-1, 1, n)
    theta = np.arccos(costheta)
    phi = np.random.uniform(0, 2 * np.pi, n)
    return theta, phi


def sph_to_cart(theta, phi):
    # Assumes normalized
    # Takes in N-length array of theta, phi coordinates,
    # Returns Nx3 array of x, y, z coordinates

    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    dirs = np.vstack((x, y, z)).T.round(15)
    return dirs


def make_2peak_deg_phantom(deg, n=1800, k=[0.34, 0.33, 0.33]):
    '''
    deg = angle in degrees between angle0 and angle1
    n = total number of points
    k [list] = weights between [noise, angle0, angle1]
    '''

    # First k[0] * n vectors are random
    nr = int(k[0] * n)
    theta = np.zeros(n)
    phi = np.zeros(n)
    randtheta, randphi = rand_vectors(nr)
    theta[:nr] = randtheta
    phi[:nr] = randphi

    # Vector 0 is at (1, 0, 0)
    theta_1 = np.pi / 2
    phi_0 = 0

    # Vector 1 is at vector 0 + deg along xz plane
    dtheta = deg * np.pi / 180
    theta_2 = theta_1 + dtheta
    if theta_2 > np.pi:
        theta_2 -= np.pi

    peaktheta = [theta_1] * int(k[1] * n) + [theta_2] * int(k[2] * n)
    peakphi = [phi_0] * int(k[1] * n) + [phi_0] * int(k[2] * n)

    # Pads with random vectors if dimensions don't work out exactly
    if len(peaktheta) > n - nr:
        peaktheta = peaktheta[: n - nr]
        peakphi = peakphi[: n - nr]
    if len(peaktheta) < n - nr:
        randtheta2, randphi2 = rand_vectors((n - nr) - peaktheta.size)
        peaktheta = np.append(peaktheta, randtheta2)
        peakphi = np.append(peakphi, randphi2)

    theta[nr:] = peaktheta
    phi[nr:] = peakphi

    dirs = sph_to_cart([theta_1, theta_2], [phi_0, phi_0])
    return theta, phi, dirs


def get_phant_peaks(npeaks):
    theta = [np.pi / 2]  # 1st peak
    phi = [0]
    if npeaks > 1:  # 2nd peak
        theta += [np.pi / 2]
        phi += [np.pi / 2]
    if npeaks > 2:  # 3rd peak
        theta += [0.005]
        phi += [0.2]
    if npeaks > 3:  # 4th peak
        theta += [np.pi / 4]
        phi += [np.pi / 4]
    if npeaks > 4:  # 5th peak
        theta += [np.pi / 4]
        phi += [3 * np.pi / 4]
    if npeaks > 5:  # 6th peak
        theta += [3 * np.pi / 4]
        phi += [np.pi / 4 + 0.2]
    if npeaks > 6:  # 7th peak
        theta += [3 * np.pi / 4]
        phi += [3 * np.pi / 4 + 0.2]
    if npeaks > 7:
        raise ValueError('Please enter npeaks <= 7')

    return np.array(theta), np.array(phi)


def make_npeak_phantom(npeaks):
    n = 3000
    np.random.seed(1)
    theta = np.zeros(n)
    phi = np.zeros(n)

    nr = int(n / (npeaks + 1))
    randtheta, randphi = rand_vectors(nr)
    theta[: nr] = randtheta
    phi[: nr] = randphi

    theta_i, phi_i = get_phant_peaks(npeaks)

    peaktheta = np.repeat(theta_i, nr)
    peakphi = np.repeat(phi_i, nr)

    # Pads with random vectors if dimensions don't work out exactly
    if peaktheta.size > n - nr:
        peaktheta = peaktheta[: n - nr]
        peakphi = peakphi[: n - nr]
    if peaktheta.size < n - nr:
        randtheta2, randphi2 = rand_vectors((n - nr) - peaktheta.size)
        peaktheta = np.append(peaktheta, randtheta2)
        peakphi = np.append(peakphi, randphi2)

    theta[nr:] = peaktheta
    phi[nr:] = peakphi

    dirs = sph_to_cart(theta_i, phi_i)

    return theta, phi, dirs
