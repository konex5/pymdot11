import numpy as _np
from typing import Dict as _Dict
from typing import List as _List
from typing import Optional as _Optional


from pyfhmdot.routine.svd_routine import (
    normalize_the_array,
    truncation_strategy,
    svd_nondeg,
    svd_deg,
)
from pyfhmdot.routine.indices import (
    indices_dst_theta_no_gate,
    indices_dst_theta_with_gate,
    degeneracy_in_theta,
    potential_middle_indices,
    slices_degenerate_blocs,
    split_degenerate_indices,
)
from pyfhmdot.routine.mul_routine import (
    mul_mm_blocs_new,
    mul_mm_blocs_snd,
    mul_theta_with_gate_new,
    mul_theta_with_gate_snd,
    mul_usv_nondeg,
    mul_usv_deg,
)


def mm_to_theta_no_gate(
    dst_blocs: _Dict[tuple, _np.ndarray],
    lhs_blocs: _Dict[tuple, _np.ndarray],
    rhs_blocs: _Dict[tuple, _np.ndarray],
    *,
    conserve_left_right: bool = False
) -> None:
    dest_indices_new, dest_indices_snd = split_degenerate_indices(
        indices_dst_theta_no_gate(
            lhs_blocs.keys(), rhs_blocs.keys(), conserve_left_right=conserve_left_right
        )
    )
    mul_mm_blocs_new(dst_blocs, lhs_blocs, rhs_blocs, dest_indices_new)
    mul_mm_blocs_snd(dst_blocs, lhs_blocs, rhs_blocs, dest_indices_snd)


def mm_to_theta_with_gate_to_delete_at_some_point(
    dst_blocs: _Dict[tuple, _np.ndarray],
    lhs_blocs: _Dict[tuple, _np.ndarray],
    rhs_blocs: _Dict[tuple, _np.ndarray],
    gate_blocs: _Dict[tuple, _np.ndarray],
    *,
    conserve_left_right_before: bool = False,
    conserve_left_right_after: bool = False
) -> None:
    from pyfhmdot.intense.mul_mp import multiply_mp

    tmp_blocs: _Dict[tuple, _np.ndarray] = {}

    multiply_mp(tmp_blocs, lhs_blocs, gate_blocs, [1], [0])
    multiply_mp(dst_blocs, tmp_blocs, rhs_blocs, [1, 4], [0, 1])


def mm_to_theta_with_gate(
    dst_blocs: _Dict[tuple, _np.ndarray],
    lhs_blocs: _Dict[tuple, _np.ndarray],
    rhs_blocs: _Dict[tuple, _np.ndarray],
    gate_blocs: _Dict[tuple, _np.ndarray],
    *,
    conserve_left_right_before: bool = False,
    conserve_left_right_after: bool = False
) -> None:
    tmp_blocs: _Dict[tuple, _np.ndarray] = {}
    mm_to_theta_no_gate(
        tmp_blocs, lhs_blocs, rhs_blocs, conserve_left_right=conserve_left_right_before
    )

    dst_indices_new, dst_indices_snd = split_degenerate_indices(
        indices_dst_theta_with_gate(
            theta_indices=tmp_blocs.keys(),
            gate_indices=gate_blocs.keys(),
            conserve_left_right=conserve_left_right_after,
        )
    )
    mul_theta_with_gate_new(dst_blocs, tmp_blocs, gate_blocs, dst_indices_new)
    mul_theta_with_gate_snd(dst_blocs, tmp_blocs, gate_blocs, dst_indices_snd)


def theta_to_mm(
    theta_blocs: _Dict[tuple, _np.ndarray],
    lhs_blocs: _Dict[tuple, _np.ndarray],
    rhs_blocs: _Dict[tuple, _np.ndarray],
    dw_dict: dict,
    chi_max: int,
    normalize: bool,
    is_um: _Optional[bool],
    direction_right: int,
    eps: float = 10**-8,
) -> None:

    keys = list(theta_blocs.keys())
    middle = potential_middle_indices(keys, direction_right=direction_right)

    # # froebenius norm !
    # norm_before = 0.
    # for _ in theta_blocs._blocks.itervalues():
    #     norm_before += _np.linalg.norm(_)**2
    # norm_before = _np.sqrt(norm_before)
    # print('norm_before=',norm_before)

    nondeg, deg = degeneracy_in_theta(keys, middle, direction_right=direction_right)

    subnewsize_deg: _List[_List] = []
    slices_degenerate_blocs(theta_blocs, deg, subnewsize_deg)
    nondeg_dims = [theta_blocs[_[1]].shape for _ in nondeg]

    array_of_U: _List[_np.ndarray] = []
    array_of_S: _List[_np.array] = []
    array_of_V: _List[_np.ndarray] = []

    svd_nondeg(theta_blocs, nondeg, nondeg_dims, array_of_U, array_of_S, array_of_V)
    svd_deg(theta_blocs, deg, subnewsize_deg, array_of_U, array_of_S, array_of_V)

    cut, dw = truncation_strategy(array_of_S, eps, chi_max)

    if normalize:
        normalize_the_array(array_of_S, cut)

    dw_dict["dw_one_serie"] += dw
    # simdict['dw_max'] = max(dw,simdict['dw_max'])

    cut_nondeg = [cut[i] for i in range(len(nondeg))]
    cut_deg = [cut[i] for i in range(len(nondeg), len(nondeg) + len(deg))]
    mul_usv_deg(
        array_of_U,
        array_of_S,
        cut_deg,
        array_of_V,
        deg,
        subnewsize_deg,
        lhs_blocs,
        rhs_blocs,
        is_um=is_um,
    )
    mul_usv_nondeg(
        array_of_U,
        array_of_S,
        cut_nondeg,
        array_of_V,
        nondeg,
        nondeg_dims,
        lhs_blocs,
        rhs_blocs,
        is_um=is_um,
    )
