import numpy as _np
from typing import Dict as _Dict

from pyfhmdot.svd_routine import (
    normalize_the_array,
    truncation_strategy,
    svd_nondeg,
    svd_deg,
)
from pyfhmdot.indices import (
    indices_dst_theta_no_gate,
    indices_dst_theta_with_gate,
    degeneracy_in_theta,
    potential_middle_indices,
    slices_degenerate_blocs,
)
from pyfhmdot.mul_routine import (
    mul_mm_blocs,
    mul_theta_with_gate,
    mul_mv_nondeg,
    mul_mv_deg,
    mul_um_nondeg,
    mul_um_deg,
)


def mm_to_theta_no_gate(
    dst_blocs: _Dict[tuple, _np.ndarray],
    lhs_blocs: _Dict[tuple, _np.ndarray],
    rhs_blocs: _Dict[tuple, _np.ndarray],
    *,
    conserve_left_right: bool = False
) -> None:
    dest_indices = indices_dst_theta_no_gate(
        lhs_blocs.keys(), rhs_blocs.keys(), conserve_left_right=conserve_left_right
    )
    mul_mm_blocs(dst_blocs, lhs_blocs, rhs_blocs, dest_indices)


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
    tmp_indices = indices_dst_theta_no_gate(
        lhs_blocs.keys(),
        rhs_blocs.keys(),
        conserve_left_right=conserve_left_right_before,
    )
    mul_mm_blocs(tmp_blocs, lhs_blocs, rhs_blocs, tmp_indices)
    dst_indices = indices_dst_theta_with_gate(
        tmp_blocs.keys(),
        gate_blocs.keys(),
        conserve_left_right=conserve_left_right_after,
    )
    mul_theta_with_gate(dst_blocs, tmp_blocs, gate_blocs, dst_indices)


def theta_to_um(
    theta_blocs: _Dict[tuple, _np.ndarray],
    lhs_blocs: _Dict[tuple, _np.ndarray],
    rhs_blocs: _Dict[tuple, _np.ndarray],
    simdict: dict,
    **kwargs
) -> None:

    keys = list(theta_blocs.keys())
    middle = potential_middle_indices(keys, direction_right=True)

    # # froebenius norm !
    # norm_before = 0.
    # for _ in theta_blocs._blocks.itervalues():
    #     norm_before += _np.linalg.norm(_)**2
    # norm_before = _np.sqrt(norm_before)
    # print('norm_before=',norm_before)

    nondeg, deg = degeneracy_in_theta(keys, middle, direction_right=True)

    subnewsize_deg = []
    slices_degenerate_blocs(theta_blocs, deg, subnewsize_deg)
    nondeg_dims = [theta_blocs[_[1]].shape for _ in nondeg]

    array_of_U = []
    array_of_S = []
    array_of_V = []

    svd_nondeg(theta_blocs, nondeg, nondeg_dims, array_of_U, array_of_S, array_of_V)
    svd_deg(theta_blocs, deg, subnewsize_deg, array_of_U, array_of_S, array_of_V)

    eps_truncation_error = simdict["eps_truncation_error"]
    chi_max = simdict["dw_Dmax"]

    cut, dw = truncation_strategy(array_of_S, eps_truncation_error, chi_max)

    if simdict["normalize"] == True:
        normalize_the_array(array_of_S, cut)

    simdict["dw_one_serie"] += dw
    # simdict['dw_max'] = max(dw,simdict['dw_max'])
    cut_nondeg = [cut[i] for i in range(len(nondeg))]
    cut_deg = [cut[i] for i in range(len(nondeg), len(nondeg) + len(deg))]
    mul_um_deg(
        array_of_U,
        array_of_S,
        cut_deg,
        array_of_V,
        deg,
        subnewsize_deg,
        lhs_blocs,
        rhs_blocs,
    )
    mul_um_nondeg(
        array_of_U,
        array_of_S,
        cut_nondeg,
        array_of_V,
        nondeg,
        nondeg_dims,
        lhs_blocs,
        rhs_blocs,
    )


def theta_to_mv(
    theta_blocs: _Dict[tuple, _np.ndarray],
    lhs_blocs: _Dict[tuple, _np.ndarray],
    rhs_blocs: _Dict[tuple, _np.ndarray],
    simdict: dict,
    **kwargs
) -> None:

    keys = list(theta_blocs.keys())
    middle = potential_middle_indices(keys, direction_right=False)

    # # froebenius norm
    # norm_before = 0.
    # for _ in theta_blocs._blocks.itervalues():
    #     norm_before += _np.linalg.norm(_)**2
    # norm_before = _np.sqrt(norm_before)
    # print('norm_before=',norm_before)

    nondeg, deg = degeneracy_in_theta(keys, middle, direction_right=False)

    subnewsize_deg = []
    slices_degenerate_blocs(theta_blocs, deg, subnewsize_deg)
    nondeg_dims = [theta_blocs[_[1]].shape for _ in nondeg]

    array_of_U = []
    array_of_S = []
    array_of_V = []

    svd_nondeg(theta_blocs, nondeg, nondeg_dims, array_of_U, array_of_S, array_of_V)
    svd_deg(theta_blocs, deg, subnewsize_deg, array_of_U, array_of_S, array_of_V)

    eps_truncation_error = simdict["eps_truncation_error"]
    chi_max = simdict["dw_Dmax"]
    cut, dw = truncation_strategy(
        array_of_S,
        eps_truncation_error,
        chi_max,
    )

    if simdict["normalize"] == True:
        normalize_the_array(array_of_S, cut)

    simdict["dw_one_serie"] += dw

    cut_nondeg = [cut[i] for i in range(len(nondeg))]
    cut_deg = [cut[i] for i in range(len(nondeg), len(nondeg) + len(deg))]

    mul_mv_deg(
        array_of_U,
        array_of_S,
        cut_deg,
        array_of_V,
        deg,
        subnewsize_deg,
        lhs_blocs,
        rhs_blocs,
    )
    mul_mv_nondeg(
        array_of_U,
        array_of_S,
        cut_nondeg,
        array_of_V,
        nondeg,
        nondeg_dims,
        lhs_blocs,
        rhs_blocs,
    )
