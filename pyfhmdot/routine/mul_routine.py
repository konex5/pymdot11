import numpy as _np
from typing import Dict as _Dict
from typing import List as _List
from typing import Tuple as _Tuple

from pyfhmdot.routine.indices import list_degenerate_indices


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
                axes=([1, 2], [0, 3]),
            ).transpose(0, 2, 3, 1)
        else:
            new_blocks[target] += _np.tensordot(
                old_blocks1[it1],
                old_blocks2[it2],
                axes=([1, 2], [0, 3]),
            ).transpose(0, 2, 3, 1)


def mul_usv_nondeg(
    array_U: _List[_np.ndarray],
    array_S: _List[_np.array],
    cut: list,
    array_V: _List[_np.ndarray],
    nondeg: _List,
    nondeg_dims: _List,
    dst_lhs_blocs: _Dict[_Tuple[int, int, int], _np.ndarray],
    dst_rhs_blocs: _Dict[_Tuple[int, int, int], _np.ndarray],
    *,
    is_um: bool = False,
) -> None:
    for i in range(len(nondeg)):  # reversed, and passed by pop.
        Dsi = cut.pop()
        if Dsi > 0:
            dims = nondeg_dims.pop()
            tmp_nondeg = nondeg.pop()
            if is_um:
                # U
                mat_left = array_U[i][:, :Dsi].reshape(dims[0], dims[1], Dsi)
                # M
                mat_right = _np.dot(
                    _np.diag(array_S[i][:Dsi]), array_V[i][:Dsi, :]
                ).reshape(Dsi, dims[2], dims[3])
            else:
                # M
                mat_left = _np.dot(
                    array_U.pop()[:, :Dsi], _np.diag(array_S.pop()[:Dsi])
                ).reshape(dims[0], dims[1], Dsi)
                # V
                mat_right = array_V.pop()[:Dsi, :].reshape(Dsi, dims[2], dims[3])

            dst_lhs_blocs[
                (tmp_nondeg[1][0], tmp_nondeg[1][1], tmp_nondeg[0])
            ] = mat_left
            dst_rhs_blocs[
                (tmp_nondeg[0], tmp_nondeg[1][2], tmp_nondeg[1][3])
            ] = mat_right
        else:
            array_U.pop()
            array_V.pop()
            array_S.pop()
            nondeg_dims.pop()
            nondeg.pop()


def mul_usv_deg(
    array_U: _List[_np.ndarray],
    array_S: _List[_np.array],
    cut: list,
    array_V: _List[_np.ndarray],
    deg: _List,
    subnewsize: _List,
    dst_lhs_blocs: _Dict[_Tuple[int, int, int], _np.ndarray],
    dst_rhs_blocs: _Dict[_Tuple[int, int, int], _np.ndarray],
    *,
    is_um: bool = False,
) -> None:
    for i in range(len(deg)):  # reversed, and pop each value.
        Dsi = cut.pop()
        if Dsi > 0:
            if is_um:
                # U
                mat_left = array_U.pop()  # [:,:Dsi]
                # M
                mat_right = _np.dot(
                    _np.diag(array_S.pop()[:Dsi]), array_V.pop()[:Dsi, :]
                )
            else:
                # M
                mat_left = _np.dot(
                    array_U.pop()[:, :Dsi], _np.diag(array_S.pop()[:Dsi])
                )
                # V
                mat_right = array_V.pop()  # [Dsi:,:]

            tmp = subnewsize.pop()
            tmp_deg = deg.pop()
            for it in tmp_deg[1]:
                posL = tmp[2].index((it[0], it[1]))
                offL = tmp[3][posL]
                dimL = tmp[4][posL]
                posR = tmp[5].index((it[2], it[3]))
                offR = tmp[6][posR]
                dimR = tmp[7][posR]

                dst_lhs_blocs[(it[0], it[1], tmp_deg[0])] = mat_left[
                    slice(offL, offL + dimL[0] * dimL[1]), :Dsi
                ].reshape(dimL[0], dimL[1], Dsi)
                dst_rhs_blocs[(tmp_deg[0], it[2], it[3])] = mat_right[
                    :Dsi, slice(offR, offR + dimR[0] * dimR[1])
                ].reshape(Dsi, dimR[0], dimR[1])
        else:
            array_U.pop()
            array_V.pop()
            array_S.pop()
            subnewsize.pop()
            deg.pop()
