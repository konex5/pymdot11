import pytest
import numpy as np
from pyfhmdot.contract import (
    prepare_index_target_no_gate,
    multiply_blocs_no_gate,
    multiply_blocs_with_gate,
)


lhs_indices = [
    (0, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 1, 1),
    (1, 0, 2),
    (1, 1, 3),
    (1, 0, 3),
]
rhs_indices = [
    (0, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 1, 1),
    (1, 0, 2),
    (2, 1, 0),
    (2, 0, 3),
    (1, 0, 4),
    (1, 0, 1),
    (1, 1, 1),
]


def test_prepare_index_target_no_gate():
    t = prepare_index_target_no_gate(lhs_indices, rhs_indices)
    assert len(t) == 18
    assert t[0][0]
    assert t[0][1] == (0, 0, 0, 0)
    assert t[1][0]
    assert not t[2][0]

    tl = prepare_index_target_no_gate(lhs_indices, rhs_indices, left_conservation=True)
    assert len(tl) == 8
    assert tl[0][0]
    assert tl[0][1] == (0, 0, 0, 0)
    assert tl[1][0]
    assert tl[2][0]

    tr = prepare_index_target_no_gate(lhs_indices, rhs_indices, right_conservation=True)
    assert len(tr) == 4
    assert tr[0][0]
    assert tr[0][1] == (0, 0, 0, 0)
    assert tr[1][0]
    assert tr[2][0]

    tlr = prepare_index_target_no_gate(
        lhs_indices, rhs_indices, left_conservation=True, right_conservation=True
    )
    assert len(tlr) == 2
    assert tlr[0][0]
    assert tlr[0][1] == (0, 0, 0, 0)
    assert tlr[1][0]
    assert tlr[1][1] == (0, 1, 0, 1)


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


lhs_blocs = {(0, 0, 0): ma(), (0, 0, 1): ma(), (0, 1, 0): ma()}
rhs_blocs = {(0, 1, 0): mb(), (1, 1, 0): mb()}
theta_blocs = {
    (0, 1, 0, 0): mtheta(),
    (1, 1, 0, 0): mtheta(),
    (1, 0, 1, 0): mtheta(),
    (0, 1, 0, 1): mtheta(),
}


@pytest.mark.parametrize("lhs_blocs", [lhs_blocs])
@pytest.mark.parametrize("rhs_blocs", [rhs_blocs])
def test_prepare_index_target_no_gate(lhs_blocs, rhs_blocs):
    dest_blocs = multiply_blocs_no_gate(lhs_blocs, rhs_blocs)
    assert dest_blocs[(0, 0, 1, 0)].shape == (3, 2, 2, 5)


@pytest.mark.parametrize("lhs_blocs", [lhs_blocs])
@pytest.mark.parametrize("rhs_blocs", [rhs_blocs])
@pytest.mark.parametrize("theta_blocs", [theta_blocs])
def test_prepare_index_target_with_gate(lhs_blocs, rhs_blocs, theta_blocs):
    dest_blocs = multiply_blocs_with_gate(lhs_blocs, rhs_blocs, theta_blocs)
    assert dest_blocs[(0, 0, 1, 0)].shape == (3, 2, 2, 5)
