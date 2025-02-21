import numpy as _np
from scipy.linalg import svd as _svd
from typing import List


def indices_and_discarded_weights(
    list_of_array: List[float],
    eps_truncation_error: float = 10 ** -32,
    chi_max: int = 600,
):
    """
    epsilon = || forall bloc s_bloc ||_2^2
    :param: list_of_array, array of singular values
    :param: eps_truncation_error > sum_{i>chi_max_tot} s_all,i^2
    :param: chi_max = max chi of bloc

    :return: list_of_indices, sum of discarded_weights
    """
    norm = _np.sqrt(_np.sum([_np.linalg.norm(arr) ** 2 for arr in list_of_array]))
    #
    A = _np.sort(_np.concatenate(list_of_array, axis=0))
    index2cutA = _np.searchsorted(
        _np.cumsum(A ** 2), eps_truncation_error * norm ** 2, side="left"
    )
    #
    dw = _np.sum(A[:index2cutA] ** 2)
    maxcutvalue = A[index2cutA]
    del A
    cut_at_index = [
        min(arr.size - _np.searchsorted(arr[::-1], maxcutvalue, "left"), chi_max)
        for arr in list_of_array
    ]

    return cut_at_index, dw


def _svd_nondeg(block_dict, nondeg, nondeg_dims, array_of_U, array_of_S, array_of_V):
    """
    :param: block_dict {index_tuple:np.ndarray}
    :param: nondeg, list of index_tuple
    :param: nondeg_dims, list of dimensions corresponds to block_dict[index_tuple].shape, at the time, it was to avoid access dict too much
    :param: array_of_u
    :param: array_of_s
    :param: array_of_vd

    :return: None
    """
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
        # U,S,V = _svd(block_dict[nondeg[i][1]].reshape(dims[0]*dims[1],dims[2]*dims[3]), full_matrices=False, compute_uv=True, overwrite_a=True, lapack_driver='gesvd')
        array_of_U.append(U)
        array_of_S.append(S)
        array_of_V.append(V)
        # del U,S,V
    pass


def _svd_deg(thetaQ, deg, subnewsize, array_of_U, array_of_S, array_of_V):
    if len(thetaQ._blocks.keys()) == 0:
        pass
    else:
        datatype = thetaQ._blocks.itervalues().next().dtype

    # print(subnewsize)
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
            thetaDeg[sliceL, sliceR] = thetaQ._blocks[it].reshape(
                dimL[0] * dimL[1], dimR[0] * dimR[1]
            )
        # print("thetaDeg",thetaDeg)
        # now SVD
        # U,S,V = _np.linalg.svd(thetaDeg, full_matrices=False, compute_uv=True)
        # U,S,V = _np.linalg.svd(thetaDeg)
        # scipy
        # U,S,V = _svd(thetaDeg)
        try:
            U, S, V = _svd(
                thetaDeg, full_matrices=False, compute_uv=True, overwrite_a=False
            )
        except:
            # _np.save('/users/kestin0/MYBUGGY/matrix_{0}'.format(_np.random.randint(100000)),thetaDeg)
            print("!!!!!!!!matrix badly conditioned!!!!!!!!!")
            U, S, V = _svd(
                thetaDeg,
                full_matrices=False,
                compute_uv=True,
                overwrite_a=True,
                lapack_driver="gesvd",
            )

        # U,S,V = _svd(thetaDeg, full_matrices=False, compute_uv=True, overwrite_a=True, lapack_driver='gesvd')
        array_of_U.append(U)
        array_of_S.append(S)
        array_of_V.append(V)
        # del U, S, V
    pass


def sweep(size, *, from_site=None, to_site=None):
    if from_site is None:
        from_site = 1
    if to_site is None:
        to_site = size
    if from_site < to_site:  # go right
        for _ in range(from_site, to_site, 1):
            yield _
    else:
        for _ in range(from_site - 1, to_site - 2, -1):
            yield _


def print_single(size, site_i):
    return "\r" + "".join(
        ["A" for _ in range(1, site_i,1)] + ["*"] + ["B" for _ in range(site_i, size, 1)]
    )


def print_double(size, site_i):
    return "\r" + "".join(
        ["A" for _ in range(1, site_i,1)]
        + ["*="]
        + ["B" for _ in range(site_i + 1, size, 1)]
    )


def apply_UM(A, B):
    pass


def apply_MV(A, B):
    pass


def apply_UM_slow(A, B):
    pass


def apply_MV_slow(A, B):
    pass


def apply_gate_UM(A, B, theta):
    pass


def apply_gate_MV(A, B, theta):
    pass


def sweep_move(size, *, start_position, end_position, apply_UM, apply_MV, **kwargs):
    if start_position < end_position:
        for site_i in sweep(size, from_site=start_position, to_site=end_position):
            apply_UM(kwargs["mps"][site_i - 1], kwargs["mps"][site_i])
    else:
        for site_i in sweep(size, from_site=start_position, to_site=end_position):
            apply_MV(kwargs["mps"][site_i - 1], kwargs["mps"][site_i])


def sweep_and_apply(
    size,
    *,
    start_position,
    end_position,
    apply_UM,
    apply_MV,
    apply_gate_UM,
    apply_gate_MV,
    start_odd_bonds,
    **kwargs
):

    should_apply_gate = (start_position % 2) == 0
    if start_odd_bonds:
        should_apply_gate = not should_apply_gate

    if start_position < end_position:
        for site_i in sweep(size, from_site=start_position, to_site=end_position):
            if should_apply_gate:
                apply_gate_UM(
                    kwargs["mps"][site_i - 1],
                    kwargs["mps"][site_i],
                    kwargs["theta"][site_i],
                )
            else:
                apply_UM(kwargs["mps"][site_i - 1], kwargs["mps"][site_i])
            should_apply_gate = not should_apply_gate
    else:
        for site_i in sweep(size, from_site=start_position, to_site=end_position):
            if should_apply_gate:
                apply_gate_MV(
                    kwargs["mps"][site_i - 1],
                    kwargs["mps"][site_i],
                    kwargs["theta"][site_i],
                )
            else:
                apply_MV(kwargs["mps"][site_i - 1], kwargs["mps"][site_i])
            should_apply_gate = not should_apply_gate


def apply_border(
    size,
    *,
    position,
    apply_UM,
    apply_MV,
    apply_gate_UM,
    apply_gate_MV,
    start_odd_bonds=True,
    **kwargs
):
    pass


def sweep_eleven_times(
    size,
    *,
    start_position,
    end_position,
    apply_UM,
    apply_MV,
    apply_gate_UM,
    apply_gate_MV,
    start_odd_bonds=True,
    **kwargs
):

    if start_position is None:
        start_position = 1
    if end_position is None:
        end_position = size

    if start_position < size / 2:
        start_position = 1
        right_direction = True
    else:
        start_position = size
        right_direction = False

    for _ in range(11):
        if (_ % 2) == 0:
            # apply_border(size, position=1,apply_UM,apply_MV,apply_gate_UM,apply_gate_MV,start_odd_bonds,**kwargs)
            # sweep_and_apply(size, start_position=2,end_position=end_position-2,apply_UM,apply_MV,apply_gate_UM,apply_gate_MV,start_odd_bonds,**kwargs)
            pass
        else:
            # apply_border(size, position=size-1,apply_UM,apply_MV,apply_gate_UM,apply_gate_MV,start_odd_bonds,**kwargs)
            # sweep_and_apply(size, start_position=size-2,end_position=2,apply_UM,apply_MV,apply_gate_UM,apply_gate_MV,start_odd_bonds,**kwargs)
            pass
