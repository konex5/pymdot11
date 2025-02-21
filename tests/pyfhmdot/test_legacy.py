import pytest

from pyfhmdot.legacy import _sliceds
import numpy as np


class thetaQ:
    def __init__(self) -> None:
        self._blocks = [np.ndarray((2, 4, 4, 3)), np.ndarray((5, 2, 2, 4))]


def test_sliceds():
    theta = thetaQ()
    deg = [
        [
            ([(0, 0, 1, 1), (1, 1, 0, 0)], [(2, 1, 1, 3), (2, 1, 2, 3)]),
            ([(0, 1, 1, 0), (1, 0, 0, 1)], [(2, 1, 1, 3), (2, 1, 2, 3)]),
        ]
    ]
    subnewsize = []
    assert theta._blocks[1].shape == (5, 2, 2, 4)
    _sliceds(theta, deg, subnewsize)
    pass
