import pytest


def random_matrices(n, m):
    import numpy as np

    a = np.random.random(n * m).reshape(n, m)
    b = np.random.random(n * m).reshape(n, m)
    return a, b


def test_dgemm_dense_pool():
    from numpy import dot as _dot

    matpool = []
    matpool.append(((0, 0), random_matrices(2, 2)))
    matpool.append(((1, 1), random_matrices(3, 3)))
    matpool.append(((0, 2), random_matrices(4, 4)))

    from numpy import tensordot as _tensordot


#     d = _tensordot(a, b,(1,0))
#     assert d[0, 0] == a[0, 0] * b[0, 0] + a[0, 1] * b[1, 0]
#
#
# def test_dgesvd():
#     import numpy as np
#     from scipy.linalg import svd as _svd
#     from copy import deepcopy
#
#     a, b = two_two_random_matrices()
#
#     adeep = deepcopy(a)
#     u, s, vd = _svd(
#         a,
#         full_matrices=False,
#         compute_uv=True,
#         overwrite_a=True,
#     )
#     #assert np.any(adeep != a)
#
#     usvd = np.dot(np.dot(u, np.diag(s)), vd)
#     assert np.all(np.round(usvd,4) == np.round(adeep,4))
#
#     u, s, vd = _svd(
#         b,
#         full_matrices=False,
#         compute_uv=True,
#         overwrite_a=False,
#         lapack_driver="gesvd",
#     )
#
#     usvd = np.dot(u, np.dot(np.diag(s), vd))
#     assert np.all(np.round(usvd,4) == np.round(b,4))
#
#
