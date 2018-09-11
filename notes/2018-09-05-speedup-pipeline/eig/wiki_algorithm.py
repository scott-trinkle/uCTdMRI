import numpy as np


def wiki_eig(A):

    p1 = A[0, 1]**2 + A[0, 2]**2 + A[1, 2]**2
    if p1 == 0:
        eigs = np.diag(A)
        return eigs

    I = np.eye(3)
    q = np.trace(A) / 3
    p2 = ((np.diag(A) - q)**2).sum() + 2 * p1
    p = np.sqrt(p2 / 6)
    B = (1 / p) * (A - q * I)
    r = np.linalg.det(B) / 2

    if r <= -1:
        phi = np.pi / 3
    elif r >= 1:
        phi = 0
    else:
        phi = np.arccos(r) / 3

    eig1 = q + 2 * p * np.cos(phi)
    eig3 = q + 2 * p * np.cos(phi + (2 * np.pi / 3))
    eig2 = 3 * q - eig1 - eig3

    eigs = [eig3, eig2, eig1]
    a1 = A - eig1*I
    a2 = A - eig2*I

    a12 = np.matmul(a1, a2)
    vec3 = a12[..., 0] / np.linalg.norm(a12[..., 0])

    return np.array([eig3, eig2, eig1]), vec3


fxx, fxy, fxz, fyy, fyz, fzz = np.random.random(6)
A = np.array([[fxx, fxy, fxz],
              [fxy, fyy, fyz],
              [fxz, fyz, fzz]])

weigs, wvecs = wiki_eig(A)
npeig, vecs = np.linalg.eigh(A)
