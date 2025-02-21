import pytest


def test_simple_eigh():
    import numpy as np
    from scipy.linalg import eigh

    A = np.array([[6, 3, 1, 5], [3, 0, 5, 1], [1, 5, 6, 2], [5, 1, 2, 2]])
    w, v = eigh(A)
    np.allclose(A @ v - v @ np.diag(w), np.zeros((4, 4)))
