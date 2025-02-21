import pytest

from pyfhmdot.contract import indices_prepare_destination_without_gate


def test_prepare_targets_two_mps_without_gate(lhs_indices, rhs_indices):
    destination_indices = indices_prepare_destination_without_gate(
        lhs_indices, rhs_indices, conserve_left_right=False
    )
    assert type(destination_indices) == list
    assert type(destination_indices[0]) == tuple
    assert destination_indices[0][0] == (0, 0, 0, 0)
    assert destination_indices[3][0] == (
        destination_indices[3][1][0],
        destination_indices[3][1][1],
        destination_indices[3][2][1],
        destination_indices[3][2][2],
    )
    assert len(destination_indices) == 18
    #
    destination_indices = indices_prepare_destination_without_gate(
        lhs_indices, rhs_indices, conserve_left_right=True
    )
    assert destination_indices[0][0] == (0, 0, 0, 0)
    assert destination_indices[3][0] == (
        destination_indices[3][1][0],
        destination_indices[3][1][1],
        destination_indices[3][2][1],
        destination_indices[3][2][2],
    )
    assert len(destination_indices) == 5
