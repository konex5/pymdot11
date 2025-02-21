import pytest


def two_two_random_matrices():
    import numpy as np

    a = np.random.random(4).reshape(2, 2)
    b = np.random.random(4).reshape(2, 2)
    return a, b


def test_dgemm():
    from numpy import dot as _dot

    a, b = two_two_random_matrices()
    c = _dot(a, b)
    assert c[0, 0] == a[0, 0] * b[0, 0] + a[0, 1] * b[1, 0]

    from scipy.linalg import tensordot as _tensordot

    d = _tensordot(a, b)
    assert d[0, 0] == a[0, 0] * b[0, 0] + a[0, 1] * b[1, 0]


def test_dgesvd():
    from scipy.linalg import svd as _svd

    a, two_two_random_matrices()
