import numpy as _np
from typing import Dict as _Dict


from pyfhmdot.mul_routine import multiply_arrays, multiply_arrays_and_transpose


def multiply_blocs_no_gate_applied(
    dst_blocs: _Dict[tuple, _np.ndarray],
    lhs_blocs: _Dict[tuple, _np.ndarray],
    rhs_blocs: _Dict[tuple, _np.ndarray],
    *,
    conserve_left_right: bool = False
) -> None:
    dest_indices = indices_prepare_destination_without_gate(
        lhs_blocs.keys(), rhs_blocs.keys(), conserve_left_right=conserve_left_right
    )
    multiply_arrays(dst_blocs, lhs_blocs, rhs_blocs, dest_indices)


def multiply_blocs_with_gate_applied(
    dst_blocs: _Dict[tuple, _np.ndarray],
    lhs_blocs: _Dict[tuple, _np.ndarray],
    rhs_blocs: _Dict[tuple, _np.ndarray],
    gate_blocs: _Dict[tuple, _np.ndarray],
    *,
    conserve_left_right_before: bool = False,
    conserve_left_right_after: bool = False
) -> None:
    tmp_blocs: _Dict[tuple, _np.ndarray] = {}
    tmp_indices = indices_prepare_destination_without_gate(
        lhs_blocs.keys(),
        rhs_blocs.keys(),
        conserve_left_right=conserve_left_right_before,
    )
    multiply_arrays(tmp_blocs, lhs_blocs, rhs_blocs, tmp_indices)
    dst_indices = indices_theta_prepare_conservation_for_gate(
        tmp_blocs.keys(),
        gate_blocs.keys(),
        conserve_left_right=conserve_left_right_after,
    )
    multiply_arrays_and_transpose(dst_blocs, tmp_blocs, gate_blocs, dst_indices)
