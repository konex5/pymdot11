import pytest


def test_truncation_strategy():
    import numpy as np

    a = [np.array([3, 2, 1]), np.array([2, 1]), np.array([2, 1, 1])]

    from pymdot.routine.svd_routine import truncation_strategy

    indices, dw = truncation_strategy(a, 0.1, 10)
    assert indices == [3, 2, 3]
    assert dw == 2

    indices, dw = truncation_strategy(a, 0.2, 10)
    assert indices == [2, 1, 1]
    assert dw == 4

    indices, dw = truncation_strategy(a, 0.8, 10)
    assert indices == [1, 0, 0]
    assert dw == 16
