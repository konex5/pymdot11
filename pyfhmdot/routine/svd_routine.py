import numpy as _np
from scipy.linalg import svd as _svd

from typing import Dict as _Dict
from typing import List as _List
from typing import Optional as _Optional
from typing import Tuple as _Tuple


def normalize_the_array(
    list_of_array: _List[_np.array], cut: _Optional[_List[int]]
) -> None:
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
) -> _Tuple[list, float]:
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


def svd_nondeg(
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


def svd_deg(
    theta_blocs: _Dict[tuple, _np.ndarray],
    deg: _List[_Tuple[int, _List[_Tuple[int, int, int, int]]]],
    subnewsize: _List[_List],
    array_of_U: _List[_np.ndarray],
    array_of_S: _List[_np.array],
    array_of_V: _List[_np.ndarray],
) -> None:
    if len(theta_blocs.keys()) == 0:
        datatype = None
    else:
        datatype = list(theta_blocs.values())[0].dtype
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
            thetaDeg[sliceL, sliceR] = theta_blocs[it].reshape(
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
