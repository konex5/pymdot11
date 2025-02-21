import pytest

from pyfhmdot.contract import prepare_index_target_no_gate

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

    tl = prepare_index_target_no_gate(lhs_indices, rhs_indices,left_conservation=True)
    assert len(tl) == 8
    assert tl[0][0]
    assert tl[0][1] == (0, 0, 0, 0)
    assert tl[1][0]
    assert tl[2][0]


    tr = prepare_index_target_no_gate(lhs_indices, rhs_indices,right_conservation=True)
    assert len(tr) == 4
    assert tr[0][0]
    assert tr[0][1] == (0, 0, 0, 0)
    assert tr[1][0]
    assert tr[2][0]

    tlr = prepare_index_target_no_gate(lhs_indices, rhs_indices,left_conservation=True,right_conservation=True)
    assert len(tlr) == 2
    assert tlr[0][0]
    assert tlr[0][1] == (0, 0, 0, 0)
    assert tlr[1][0]
    assert tlr[1][1] == (0, 1, 0, 1)
