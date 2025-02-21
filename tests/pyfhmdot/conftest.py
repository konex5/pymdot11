from numpy import dtype
import pytest
import numpy as np


def user_type(complex: bool):
    is_float = True
    if is_float and complex:

        if complex:
            return dtype


@pytest.fixture
def make_mps():
    def _make_mps(i=None, d=None, j=None):
        if i is None:
            i = np.random.randint(100)
        if d is None:
            d = np.random.randint(5)
        if j is None:
            j = np.random.randint(100)
        mps = np.random.random.rand(i * d * j, dtype="u8").reshape(i, d, j)
        return mps

    return _make_mps


def mps(make_mps):
    return make_mps()
