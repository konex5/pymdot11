import pytest
import time


def test_simple_dw():
    import numpy as np

    s = np.array([0.9, 0.8, 0.6, 0.3, 0.01, 0, 0, 0])
    tol = 0.25  # eps
    s_out = s[s**2 > tol]
    assert s_out.size == 3


def test_advanced_dw():
    import numpy as np

    array_of_s = [np.array([0.9, 0]), np.array([0.8, 0.6, 0.01, 0]), np.array([0.3, 0])]
    tol = 0.25  # eps
    chi_max = 100
    a = np.sort(np.concatenate(array_of_s, axis=0))
    index2cutA = np.searchsorted(np.cumsum(a**2), tol, side="left")  # norm rm
    cut_at_index = [
        min(arr.size - np.searchsorted(arr[::-1], a[index2cutA], "left"), chi_max)
        for arr in array_of_s
    ]
    s_out = [array_of_s[i][: cut_at_index[i]] for i in range(3)]

    assert s_out[0].size == 1
    assert s_out[1].size == 2
    assert s_out[2].size == 0
