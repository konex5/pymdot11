import pytest


def test_prepare_targets_two_mps_without_gate(lhs_indices, rhs_indices):
    from pyfhmdot.routine.indices import (
        indices_dst_theta_no_gate,
    )

    destination_indices = indices_dst_theta_no_gate(
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
    destination_indices = indices_dst_theta_no_gate(
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


def test_prepare_targets_two_mps_without_gate_splited(lhs_indices, rhs_indices):
    from pyfhmdot.routine.indices import (
        indices_dst_theta_no_gate,split_degenerate_indices
    )

    destination_indices = indices_dst_theta_no_gate(
        lhs_indices, rhs_indices, conserve_left_right=False
    )
    list_nondeg, list_deg = split_degenerate_indices(destination_indices)
    assert type(list_nondeg) == list
    assert type(list_deg) == list
    assert type(list_nondeg[0]) == tuple
    assert type(list_deg[0]) == tuple
    assert list_nondeg[0][0] == (0, 0, 0, 0)
    """
    assert destination_indices[3][0] == (
        destination_indices[3][1][0],
        destination_indices[3][1][1],
        destination_indices[3][2][1],
        destination_indices[3][2][2],
    )
    assert len(destination_indices) == 18
    #
    destination_indices = indices_dst_theta_no_gate(
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
    """






def test_prepare_targets_two_mps_without_gate(lhs_indices, rhs_indices, gate_indices):
    from pyfhmdot.routine.indices import (
        indices_dst_theta_no_gate,
        indices_dst_theta_with_gate,
    )

    dst_indices = indices_dst_theta_no_gate(
        lhs_indices, rhs_indices, conserve_left_right=False
    )
    destination_indices = indices_dst_theta_with_gate(
        [_[0] for _ in dst_indices], gate_indices, conserve_left_right=False
    )
    assert destination_indices[0][0] == (0, 0, 0, 0)
    assert len(destination_indices) == 22
    #
    destination_indices = indices_dst_theta_with_gate(
        [_[0] for _ in dst_indices], gate_indices, conserve_left_right=True
    )
    assert destination_indices[0][0] == (0, 0, 0, 0)
    assert len(destination_indices) == 6
