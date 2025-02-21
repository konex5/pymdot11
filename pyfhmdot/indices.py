import numpy as _np
from typing import Dict as _Dict
from typing import List as _List
from typing import Optional as _Optional
from typing import Tuple as _Tuple


def merge_map_indices_slices_according_to_qnum(qname):
    basis = {  #
        "sh-None": {
            "zero": [(0,)],
            "qn": [(0,)],
            "deg": [2],
            "2qn": [(0,)],
            "2deg": [4],
            "map": [[(0, 0)], [0], [slice(0, 4)]],
        },  # Nothing
        "sh-U1": {
            "zero": [(0,)],
            "qn": [(-1,), (1,)],
            "deg": [1, 1],
            "2qn": [(-2,), (0,), (2,)],
            "2deg": [1, 2, 1],
            "map": [
                [(0, 0), (0, 1), (1, 0), (1, 1)],
                [1, 0, 2, 1],
                [slice(0, 1), slice(0, 1), slice(0, 1), slice(1, 2)],
            ],
        },  # S^z_tot
        "so-None": {
            "zero": [(0,)],
            "qn": [(0,)],
            "deg": [3],
            "2qn": [(0,)],
            "2deg": [9],
            "map": [[(0, 0)], [0], [slice(0, 9)]],
        },
        "so-U1": {
            "zero": [(0,)],
            "qn": [(-2,), (0,), (2,)],
            "deg": [1, 1, 1],
            "2qn": [(-4,), (-2,), (0,), (+2,), (+4,)],
            "2deg": [1, 2, 3, 2, 1],
            "map": [
                [
                    (0, 0),
                    (0, 1),
                    (0, 2),
                    (1, 0),
                    (1, 1),
                    (1, 2),
                    (2, 0),
                    (2, 1),
                    (2, 2),
                ],
                [2, 1, 0, 3, 2, 1, 4, 3, 2],
                [
                    slice(0, 1),
                    slice(0, 1),
                    slice(0, 1),
                    slice(0, 1),
                    slice(1, 2),
                    slice(1, 2),
                    slice(0, 1),
                    slice(1, 2),
                    slice(2, 3),
                ],
            ],
        },  # S^z_tot
        "ldsh-None": {
            "zero": [(0,)],
            "qn": [(0,)],
            "deg": [4],
            "2qn": [(0,)],
            "2deg": [16],
            "map": [[(0, 0)], [0], [slice(0, 16)]],
        },
        # the one favorising antiferro order is ============================
        "ldsh-U1comb": {
            "zero": [(0,)],
            "qn": [(-2,), (0,), (+2,)],
            "deg": [1, 2, 1],
            "2qn": [(-4,), (-2,), (0,), (+2,), (+4,)],
            "2deg": [1, 4, 6, 4, 1],
            "map": [
                [
                    (0, 0),
                    (0, 1),
                    (0, 2),
                    (1, 0),
                    (1, 1),
                    (1, 2),
                    (2, 0),
                    (2, 1),
                    (2, 2),
                ],
                [2, 1, 0, 3, 2, 1, 4, 3, 2],
                [
                    slice(0, 1),
                    slice(0, 2),
                    slice(0, 1),
                    slice(0, 2),
                    slice(1, 5),
                    slice(2, 4),
                    slice(0, 1),
                    slice(2, 4),
                    slice(5, 6),
                ],
            ],
        },
        "skeleton": {
            "zero": ["neutral QN"],
            "qn": ["pure state QN"],
            "deg": ["int"],
            "2qn": ["mixed state QN"],
            "2deg": ["int**2"],
            "map": [["pair of pure QN"], ["mixed QN"], ["slice"]],
        },
    }


def internal_qn_sum(lhs: int, rhs: int) -> int:
    return lhs + rhs


def internal_qn_sub(lhs: int, rhs: int) -> int:
    return lhs - rhs


def potential_middle_indices(
    theta_indices: _List[_Tuple], *, direction_right: _Optional[bool] = None
):
    middle_indices = []
    if direction_right or direction_right is None:
        for theta_index in theta_indices:
            middle_indices.append(internal_qn_sum(
                theta_index[0], theta_index[1]))
    if not direction_right or direction_right is None:
        for theta_index in theta_indices:
            val = internal_qn_sub(
                theta_index[3], theta_index[2]
            )  # note for TDMRG here is a sum according to direction
            if val >= 0:  # shouldn't occur but let's be carefull
                middle_indices.append(val)
    return sorted(set(middle_indices))


def degeneracy_in_theta(
    keys: _List[_Tuple[int, int, int, int]],
    middle: _List[int],
    *,
    direction_right: _Optional[bool] = None
) -> _Tuple[_List[_Tuple[int, _Tuple[int, int, int, int]]], _List[_Tuple[int, _List[_Tuple[int, int, int, int]]]]]:
    nondeg = []
    degenerate = []

    if direction_right is None:
        for j in range(len(middle)):
            tmp = []
            for it in keys:
                if (middle[j] == internal_qn_sum(it[0], it[1])) and (
                    middle[j] == internal_qn_sub(it[3], it[2])
                ):  # note for TDMRG here is a sum according to direction
                    tmp.append(it)
            if len(tmp) > 1:
                degenerate.append((j, tmp))
            elif len(tmp) == 1:
                nondeg.append((j, tmp[0]))
    elif direction_right:
        for j in range(len(middle)):
            tmp = []
            for it in keys:
                if middle[j] == internal_qn_sum(it[0], it[1]):
                    tmp.append(it)
            if len(tmp) > 1:
                degenerate.append((j, tmp))
            elif len(tmp) == 1:
                nondeg.append((j, tmp[0]))
    elif not direction_right:
        for j in range(len(middle)):
            tmp = []
            for it in keys:
                if middle[j] == internal_qn_sub(
                    it[3], it[2]
                ):  # note for TDMRG here is a sum according to direction
                    tmp.append(it)
            if len(tmp) > 1:
                degenerate.append((j, tmp))
            elif len(tmp) == 1:
                nondeg.append((j, tmp[0]))

    return nondeg, degenerate


def slices_degenerate_blocs(
    thetaQ: _Dict[_Tuple, _np.ndarray],
    degenerate_list: _List[_Tuple[int, _List[_Tuple[int, int, int, int]]]],
    subnewsize: _List[_List],
) -> None:
    for i in range(len(degenerate_list)):  # for each deg global block
        # define a local basis
        left__loc_basis = sorted(
            set([(it[0], it[1]) for it in degenerate_list[i][1]]))
        right_loc_basis = sorted(
            set([(it[2], it[3]) for it in degenerate_list[i][1]]))
        # find the local dim corresponding to left_loc_basis and right_loc_basis
        left__loc_dim = len(left__loc_basis) * [(0, 0)]
        right_loc_dim = len(right_loc_basis) * [(0, 0)]
        # for each local_index
        for it in degenerate_list[i][1]:
            dims = thetaQ[it].shape
            left__loc_dim[left__loc_basis.index(
                (it[0], it[1]))] = (dims[0], dims[1])
            right_loc_dim[right_loc_basis.index(
                (it[2], it[3]))] = (dims[2], dims[3])
        # find the totdim
        total_left__dim = sum([d[0] * d[1] for d in left__loc_dim])
        total_right_dim = sum([d[0] * d[1] for d in right_loc_dim])
        # offsets
        left__loc_off = [0] + [
            sum([d[0] * d[1] for d in left__loc_dim[:i]])
            for i in range(1, len(left__loc_dim))
        ]
        right_loc_off = [0] + [
            sum([d[0] * d[1] for d in right_loc_dim[:i]])
            for i in range(1, len(right_loc_dim))
        ]
        subnewsize.append(
            [
                total_left__dim,
                total_right_dim,
                left__loc_basis,
                left__loc_off,
                left__loc_dim,
                right_loc_basis,
                right_loc_off,
                right_loc_dim,
            ]
        )
