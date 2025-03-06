import pytest


def test_svd_nondeg():
    import numpy as np
    from scipy.linalg import svd as _svd

    a = np.ndarray((1, 2, 2))
    a.fill(0)
    a[0, 0, 0] = 1
    b = np.ndarray((2, 2, 4))
    b.fill(0)
    b[0, 0, 0] = 1
    th = np.ndarray((2, 2, 2, 2))
    th.fill(0)
    th[0, 0, 0, 0] = 1
    t = np.tensordot(np.tensordot(a, th, (1, 0)), b, ((2, 1), (1, 0)))
    u, s, vd = _svd(
        t.reshape(1 * 2, 2 * 4),
        full_matrices=False,
        compute_uv=True,
        overwrite_a=False,
        lapack_driver="gesvd",
    )
    # sweep right
    U = u.reshape(1, 2, 2)  # should be orthogonal/hermitian
    M = np.tensordot(np.diag(s), vd.reshape(2, 2, 4), (1, 0))
    # or sweep left
    M = np.tensordot(u.reshape(1, 2, 2), np.diag(s), (2, 0))
    VD = vd.reshape(2, 2, 4)  # should be orthogonal/hermitian
    pass
