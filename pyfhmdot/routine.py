import numpy as _np
from scipy.linalg import svd as _svd

from pyfhmdot.svd_routine import (
    normalize_the_array,
    truncation_strategy,
    svd_nondeg,
    svd_deg,
    mult_nondeg_MV,
    mult_deg_MV,
    mult_nondeg_UM,
    mult_deg_UM,
)

from pyfhmdot.indices import (
    degeneracy_in_theta,
    potential_middle_indices,
    slices_degenerate_blocs,
)


def mpsQ_svd_th2Um(thetaQ, mpsL, mpsR, simdict, **kwargs):

    keys = list(thetaQ.keys())
    middle = potential_middle_indices(keys, direction_right=True)

    # # froebenius norm !
    # norm_before = 0.
    # for _ in thetaQ._blocks.itervalues():
    #     norm_before += _np.linalg.norm(_)**2
    # norm_before = _np.sqrt(norm_before)
    # print('norm_before=',norm_before)

    nondeg, deg = degeneracy_in_theta(keys, middle, direction_right=True)

    subnewsize_deg = []
    slices_degenerate_blocs(thetaQ, deg, subnewsize_deg)
    nondeg_dims = [thetaQ[_[1]].shape for _ in nondeg]

    array_of_U = []
    array_of_S = []
    array_of_V = []

    svd_nondeg(thetaQ, nondeg, nondeg_dims, array_of_U, array_of_S, array_of_V)
    svd_deg(thetaQ, deg, subnewsize_deg, array_of_U, array_of_S, array_of_V)

    eps_truncation_error = simdict["eps_truncation_error"]
    chi_max = simdict["dw_Dmax"]
    chi_max_total = simdict["dw_Dmax_tot"]

    cut, dw = truncation_strategy(array_of_S, eps_truncation_error, chi_max)

    if simdict["normalize"] == True:
        normalize_the_array(array_of_S, cut)

    simdict["dw_one_serie"] += dw
    # simdict['dw_max'] = max(dw,simdict['dw_max'])
    cut_nondeg = [cut[i] for i in range(len(nondeg))]
    cut_deg = [cut[i] for i in range(len(nondeg), len(nondeg) + len(deg))]
    mult_deg_UM(
        array_of_U,
        array_of_S,
        cut_deg,
        array_of_V,
        deg,
        subnewsize_deg,
        mpsL,
        mpsR,
    )
    mult_nondeg_UM(
        array_of_U,
        array_of_S,
        cut_nondeg,
        array_of_V,
        nondeg,
        nondeg_dims,
        mpsL,
        mpsR,
    )


def mpsQ_svd_th2mV(thetaQ, mpsL, mpsR, simdict, **kwargs):

    keys = list(thetaQ.keys())
    middle = potential_middle_indices(keys, direction_right=False)

    # # froebenius norm
    # norm_before = 0.
    # for _ in thetaQ._blocks.itervalues():
    #     norm_before += _np.linalg.norm(_)**2
    # norm_before = _np.sqrt(norm_before)
    # print('norm_before=',norm_before)

    nondeg, deg = degeneracy_in_theta(keys, middle, direction_right=False)

    subnewsize_deg = []
    slices_degenerate_blocs(thetaQ, deg, subnewsize_deg)
    nondeg_dims = [thetaQ[_[1]].shape for _ in nondeg]

    array_of_U = []
    array_of_S = []
    array_of_V = []

    svd_nondeg(thetaQ, nondeg, nondeg_dims, array_of_U, array_of_S, array_of_V)
    svd_deg(thetaQ, deg, subnewsize_deg, array_of_U, array_of_S, array_of_V)

    eps_truncation_error = simdict["eps_truncation_error"]
    chi_max = simdict["dw_Dmax"]
    chi_max_total = simdict["dw_Dmax_tot"]
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

    mult_deg_MV(
        array_of_U,
        array_of_S,
        cut_deg,
        array_of_V,
        deg,
        subnewsize_deg,
        mpsL,
        mpsR,
    )
    mult_nondeg_MV(
        array_of_U,
        array_of_S,
        cut_nondeg,
        array_of_V,
        nondeg,
        nondeg_dims,
        mpsL,
        mpsR,
    )
    pass


# def merge_indices_according_to_qnum(qname, theta_blocs_no_merge):
#     # previously called subnewsize
#     pass
#
#
# def fast_UM_no_mult():
#     pass
#
#
# def fast_MV_no_mult():
#     pass
#
#
# def theta_to_um(theta_blocs, deg_indices_and_slices, eps_trunk):
#     pass
#
#
# def theta_to_mv(theta_blocs, deg_indices_and_slices, eps_trunk):
#     pass
