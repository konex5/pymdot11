import numpy as _np
from typing import Dict as _Dict
from typing import List as _List
from typing import Tuple as _Tuple

from pyfhmdot.indices import list_degenerate_indices


def mul_mm_blocs(
    new_blocks: _Dict[tuple, _np.ndarray],
    old_blocks1: _Dict[tuple, _np.ndarray],
    old_blocks2: _Dict[tuple, _np.ndarray],
    buildtarget: _List[_Tuple[tuple, tuple, tuple]],
) -> None:
    list_isnew = list_degenerate_indices([_[0] for _ in buildtarget])
    for new, it in zip(list_isnew, buildtarget):
        target, it1, it2 = it[0], it[1], it[2]
        if new:
            new_blocks[target] = _np.tensordot(
                old_blocks1[it1],
                old_blocks2[it2],
                axes=(2, 0),
            )
        else:
            new_blocks[target] += _np.tensordot(
                old_blocks1[it1],
                old_blocks2[it2],
                axes=(2, 0),
            )


def mul_theta_with_gate(
    new_blocks: _Dict[tuple, _np.ndarray],
    old_blocks1: _Dict[tuple, _np.ndarray],
    old_blocks2: _Dict[tuple, _np.ndarray],
    buildtarget: _List[_Tuple[tuple, tuple, tuple]],
) -> None:
    list_isnew = list_degenerate_indices([_[0] for _ in buildtarget])
    for new, it in zip(list_isnew, buildtarget):
        target, it1, it2 = it[0], it[1], it[2]
        if new:
            new_blocks[target] = _np.tensordot(
                old_blocks1[it1],
                old_blocks2[it2],
                axes=([1, 2], [2, 3]),
            ).transpose(0, 2, 3, 1)
        else:
            new_blocks[target] += _np.tensordot(
                old_blocks1[it1],
                old_blocks2[it2],
                axes=([1, 2], [2, 3]),
            ).transpose(0, 2, 3, 1)


def mul_mv_nondeg(
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


def mul_mv_deg(array_U, array_S, cut, array_V, deg, subnewsize, dict_left, dict_right):
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


def mul_um_nondeg(
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
            array_U.pop()
            array_V.pop()
            array_S.pop()
            nondeg_dims.pop()
            nondeg.pop()


def mul_um_deg(array_U, array_S, cut, array_V, deg, subnewsize, dict_left, dict_right):
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
