import numpy as _np
from scipy.linalg import svd as _svd

from typing import Dict as _Dict
from typing import List as _List
from typing import Optional as _Optional
from typing import Tuple as _Tuple


from pyfhmdot.indices import (
    degeneracy_in_theta,
    potential_middle_indices,
    slices_degenerate_blocs,
)


def normalize_the_array(list_of_array: _List[_np.array], cut: _Optional[_List[int]]) -> None:
    if isinstance(cut, list):
        norm = _np.sqrt(
            _np.sum(
                [
                    _np.linalg.norm(arr[: cut[i]]) ** 2
                    for i, arr in enumerate(list_of_array)
                ]
            )
        )
        for i in range(len(list_of_array)):
            list_of_array[i] /= norm
    else:
        norm = _np.sqrt(_np.sum([_np.linalg.norm(arr) ** 2 for arr in list_of_array]))
        for i in range(len(list_of_array)):
            list_of_array[i] /= norm


def truncation_strategy(
    list_of_array: _List[_np.array],
    eps_truncation_error: float = 10 ** -32,
    chi_max: int = 600,
) -> _Tuple[list,float]:
    #
    # epsilon = || forall bloc s_bloc ||_2^2
    # chi_max = max chi of bloc
    # eps_truncation_error < sum_{i>chi_max} s_all,i^2
    #
    norm = _np.sqrt(_np.sum([_np.linalg.norm(arr) ** 2 for arr in list_of_array]))

    A = _np.sort(_np.concatenate(list_of_array, axis=0))
    index2cutA = _np.searchsorted(
        _np.cumsum(A ** 2), eps_truncation_error * norm ** 2, side="left"
    )

    dw = _np.sum(A[:index2cutA] ** 2)
    maxcutvalue = A[index2cutA]

    del A
    cut_at_index = [
        min(arr.size - _np.searchsorted(arr[::-1], maxcutvalue, "left"), chi_max)
        for arr in list_of_array
    ]

    return cut_at_index, dw


def _svd_nondeg(
    block_dict: _Dict[tuple, _np.ndarray],
    nondeg: _List[_Tuple[int, _Tuple[int, int, int, int]]],
    nondeg_dims: _List[_Tuple[int, int, int, int]],
    array_of_U: _List[_np.ndarray],
    array_of_S: _List[_np.array],
    array_of_V: _List[_np.ndarray],
) -> None:
    for i in range(len(nondeg)):
        dims = nondeg_dims[i]
        try:
            U, S, V = _svd(
                block_dict[nondeg[i][1]].reshape(dims[0] * dims[1], dims[2] * dims[3]),
                full_matrices=False,
                compute_uv=True,
                overwrite_a=True,
            )
        except:
            print("!!!!!!!!matrix badly conditioned!!!!!!!!!")
            U, S, V = _svd(
                block_dict[nondeg[i][1]].reshape(dims[0] * dims[1], dims[2] * dims[3]),
                full_matrices=False,
                compute_uv=True,
                overwrite_a=False,
                lapack_driver="gesvd",
            )
        array_of_U.append(U)
        array_of_S.append(S)
        array_of_V.append(V)


def _svd_deg(
    thetaQ: _Dict[tuple, _np.ndarray],
    deg: _List[_Tuple[int, _List[_Tuple[int, int, int, int]]]],
    subnewsize: _List[_List],
    array_of_U: _List[_np.ndarray],
    array_of_S: _List[_np.array],
    array_of_V: _List[_np.ndarray],
) -> None:
    if len(thetaQ.keys()) == 0:
        datatype = None
    else:
        datatype = list(thetaQ.values())[0].dtype
    for i in range(len(deg)):
        # construct the degenerated matrix
        thetaDeg = _np.zeros((subnewsize[i][0], subnewsize[i][1]), dtype=datatype)
        # fill it
        for it in deg[i][1]:
            posL = subnewsize[i][2].index((it[0], it[1]))
            offL = subnewsize[i][3][posL]
            dimL = subnewsize[i][4][posL]
            posR = subnewsize[i][5].index((it[2], it[3]))
            offR = subnewsize[i][6][posR]
            dimR = subnewsize[i][7][posR]
            sliceL = slice(offL, offL + dimL[0] * dimL[1])
            sliceR = slice(offR, offR + dimR[0] * dimR[1])
            thetaDeg[sliceL, sliceR] = thetaQ[it].reshape(
                dimL[0] * dimL[1], dimR[0] * dimR[1]
            )
        try:
            U, S, V = _svd(
                thetaDeg, full_matrices=False, compute_uv=True, overwrite_a=False
            )
        except:
            print("!!!!!!!!matrix badly conditioned!!!!!!!!!")
            U, S, V = _svd(
                thetaDeg,
                full_matrices=False,
                compute_uv=True,
                overwrite_a=True,
                lapack_driver="gesvd",
            )

        array_of_U.append(U)
        array_of_S.append(S)
        array_of_V.append(V)


def _mult_nondeg_MV(
    array_U, array_S, cut, array_V, nondeg, nondeg_dims, dict_left, dict_right
):
    i_Nb = len(nondeg)
    for i in range(i_Nb):  # reversed, and passed by pop.
        Dsi = cut.pop()
        if Dsi > 0:
            dims = nondeg_dims.pop()
            tmp_nondeg = nondeg.pop()
            dict_left[(tmp_nondeg[1][0], tmp_nondeg[1][1], tmp_nondeg[0])] = _np.dot(
                array_U.pop()[:, :Dsi], _np.diag(array_S.pop()[:Dsi])
            ).reshape(dims[0], dims[1], Dsi)
            dict_right[
                (tmp_nondeg[0], tmp_nondeg[1][2], tmp_nondeg[1][3])
            ] = array_V.pop()[:Dsi, :].reshape(Dsi, dims[2], dims[3])
        else:
            array_U.pop()
            array_V.pop()
            array_S.pop()
            nondeg_dims.pop()
            nondeg.pop()


def _mult_deg_MV(
    array_U, array_S, cut, array_V, deg, subnewsize, dict_left, dict_right
):
    i_Nb = len(deg)  # index for deg and subnewsize.. we
    for i in range(i_Nb):  # reversed, and pop each value.
        Dsi = cut.pop()
        if Dsi > 0:
            M = _np.dot(array_U.pop()[:, :Dsi], _np.diag(array_S.pop()[:Dsi]))
            V = array_V.pop()  # [Dsi:,:]

            tmp = subnewsize.pop()
            tmp_deg = deg.pop()
            for it in tmp_deg[1]:
                posL = tmp[2].index((it[0], it[1]))
                offL = tmp[3][posL]
                dimL = tmp[4][posL]
                posR = tmp[5].index((it[2], it[3]))
                offR = tmp[6][posR]
                dimR = tmp[7][posR]

                dict_left[(it[0], it[1], tmp_deg[0])] = M[
                    slice(offL, offL + dimL[0] * dimL[1]), :Dsi
                ].reshape(dimL[0], dimL[1], Dsi)
                dict_right[(tmp_deg[0], it[2], it[3])] = V[
                    :Dsi, slice(offR, offR + dimR[0] * dimR[1])
                ].reshape(Dsi, dimR[0], dimR[1])
        else:
            array_U.pop()
            array_V.pop()
            array_S.pop()
            subnewsize.pop()
            deg.pop()


def _mult_nondeg_UM(
    array_U, array_S, cut, array_V, nondeg, nondeg_dims, dict_left, dict_right
):
    for i in range(len(nondeg)):  # reversed, and passed by pop.
        Dsi = cut[i]
        if Dsi != 0:
            dims = nondeg_dims[i]
            dict_left[(nondeg[i][1][0], nondeg[i][1][1], nondeg[i][0])] = array_U[i][
                :, :Dsi
            ].reshape(dims[0], dims[1], Dsi)
            dict_right[(nondeg[i][0], nondeg[i][1][2], nondeg[i][1][3])] = _np.dot(
                _np.diag(array_S[i][:Dsi]), array_V[i][:Dsi, :]
            ).reshape(Dsi, dims[2], dims[3])
        else:
            pass


def _mult_deg_UM(
    array_U, array_S, cut, array_V, deg, subnewsize, dict_left, dict_right
):
    i_Nb = len(deg)
    for i in range(i_Nb):
        Dsi = cut.pop()
        if Dsi > 0:
            M = _np.dot(_np.diag(array_S.pop()[:Dsi]), array_V.pop()[:Dsi, :])
            U = array_U.pop()  # [:,:Dsi]

            tmp = subnewsize.pop()
            tmp_deg = deg.pop()
            for it in tmp_deg[1]:
                posL = tmp[2].index((it[0], it[1]))
                offL = tmp[3][posL]
                dimL = tmp[4][posL]
                posR = tmp[5].index((it[2], it[3]))
                offR = tmp[6][posR]
                dimR = tmp[7][posR]

                dict_left[(it[0], it[1], tmp_deg[0])] = U[
                    slice(offL, offL + dimL[0] * dimL[1]), :Dsi
                ].reshape(dimL[0], dimL[1], Dsi)
                dict_right[(tmp_deg[0], it[2], it[3])] = M[
                    :Dsi, slice(offR, offR + dimR[0] * dimR[1])
                ].reshape(Dsi, dimR[0], dimR[1])
        else:
            array_U.pop()
            array_V.pop()
            array_S.pop()
            subnewsize.pop()
            deg.pop()
    pass


############################################################


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

    _svd_nondeg(thetaQ, nondeg, nondeg_dims, array_of_U, array_of_S, array_of_V)
    _svd_deg(thetaQ, deg, subnewsize_deg, array_of_U, array_of_S, array_of_V)

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
    _mult_deg_UM(
        array_of_U,
        array_of_S,
        cut_deg,
        array_of_V,
        deg,
        subnewsize_deg,
        mpsL,
        mpsR,
    )
    _mult_nondeg_UM(
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

    _svd_nondeg(thetaQ, nondeg, nondeg_dims, array_of_U, array_of_S, array_of_V)
    _svd_deg(thetaQ, deg, subnewsize_deg, array_of_U, array_of_S, array_of_V)

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

    _mult_deg_MV(
        array_of_U,
        array_of_S,
        cut_deg,
        array_of_V,
        deg,
        subnewsize_deg,
        mpsL,
        mpsR,
    )
    _mult_nondeg_MV(
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
