import pytest

from pyfhmdot.contract import (
    multiply_blocs_no_gate_applied,
    multiply_blocs_with_gate_applied,
)


def test_multiply_blocs_dense(make_single_dense_mps):
    lhs_blocs = make_single_dense_mps(chiL=3, d=4, chiR=5)
    rhs_blocs = make_single_dense_mps(chiL=5, d=4, chiR=2)
    dest_blocs = {}
    multiply_blocs_no_gate_applied(dest_blocs, lhs_blocs, rhs_blocs)
    assert list(dest_blocs.keys())[0] == (0, 0, 0, 0)
    assert len(dest_blocs.keys()) == 1
    assert dest_blocs[(0, 0, 0, 0)].shape == (3, 4, 4, 2)


def test_multiply_blocs_dense_with_gate(make_single_dense_mps, make_single_dense_gate):
    lhs_blocs = make_single_dense_mps(chiL=3, d=4, chiR=5)
    rhs_blocs = make_single_dense_mps(chiL=5, d=4, chiR=2)
    gate_blocs = make_single_dense_gate(d=4)
    dest_blocs = {}
    multiply_blocs_with_gate_applied(dest_blocs, lhs_blocs, rhs_blocs, gate_blocs)
    assert list(dest_blocs.keys())[0] == (0, 0, 0, 0)
    assert len(dest_blocs.keys()) == 1
