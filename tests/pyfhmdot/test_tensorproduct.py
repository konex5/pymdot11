import pytest
import numpy as np


def ma():
    a = np.ndarray((3, 2, 4))
    a.fill(0)
    a[0, 0, 0] = 1
    a[0, 1, 0] = 2
    a[2, 0, 1] = 3
    return a


@pytest.mark.parametrize("a", [ma()])
def test_transpose(a):
    assert a[2, 0, 1] == 3
    # a.transpose([1,0,2])
    # assert a[0,2,1] == 3
