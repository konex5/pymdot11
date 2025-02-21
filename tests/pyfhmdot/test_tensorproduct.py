import pytest
import numpy as np


def ma():
    a = np.ndarray((3, 2, 4))
    a.fill(0)
    a[0, 0, 0] = 1
    a[0, 1, 0] = 2
    a[2, 0, 1] = 3
    return a


def mb():
    b = np.ndarray((4, 2, 5))
    b.fill(0)
    b[0, 0, 0] = 7
    b[0, 1, 0] = 5
    b[1, 0, 4] = 9
    b[1, 0, 2] = -8
    return b


def mtheta():
    t = np.ndarray((2, 2, 2, 2))
    t.fill(0)
    t[0, 0, 0, 0] = -2
    t[1, 1, 0, 0] = -5
    t[1, 0, 1, 0] = 3
    t[1, 0, 0, 1] = -1
    return t


@pytest.mark.parametrize("a", [ma()])
def test_simple_transpose(a):
    assert a[2, 0, 1] == 3
    b = a.transpose([1, 0, 2])
    assert b[0, 2, 1] == 3


@pytest.mark.parametrize("a", [ma()])
@pytest.mark.parametrize("b", [mb()])
def test_simple_tensordot(a, b):
    r = np.tensordot(a, b, (2, 0))
    assert r.shape == (3, 2, 2, 5)
    assert r[0, 0, 0, 0] == 7
    assert r[0, 0, 1, 0] == 5


@pytest.mark.parametrize("a", [ma()])
@pytest.mark.parametrize("b", [mb()])
@pytest.mark.parametrize("theta", [mtheta()])
def test_simple_tensordot_transpose(a, b, theta):
    mtmp = np.tensordot(a, b, (2, 0))
    mdest_tmp = np.tensordot(theta, mtmp, ([0, 1], [1, 2]))
    assert mdest_tmp.shape == (2, 2, 3, 5)
    assert mdest_tmp[0, 0, 0, 0] == -64
    assert mdest_tmp[0, 0, 2, 4] == -54
    mdest = mdest_tmp.transpose([2, 0, 1, 3])
    assert mdest.shape == (3, 2, 2, 5)
    assert mdest[0, 0, 0, 0] == -64
    assert mdest[2, 0, 0, 4] == -54
    mth = mdest.reshape(3 * 2, 2 * 5)
    assert mth.shape == (6, 10)
