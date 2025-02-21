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
    assert t[0][0]
    assert t[0][1] == (0, 0, 0, 0)
    assert t[1][0]
    assert not t[2][0]
