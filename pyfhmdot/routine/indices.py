from logging import warning as _warning
import numpy as _np
from typing import Dict as _Dict
from typing import KeysView as _KeysView
from typing import List as _List
from typing import Tuple as _Tuple


def split_degenerate_indices(
    indices: _List[_Tuple[tuple, tuple, tuple]]
) -> _Tuple[_List[_Tuple[tuple, tuple, tuple]], _List[_Tuple[tuple, tuple, tuple]]]:
    list_deg = []
    list_nondeg = []
    all_theta = [_[0] for _ in indices]
    for l in range(len(indices)):
        if all_theta.index(indices[l][0]) == l:
            list_nondeg.append(indices[l])
        else:
            list_deg.append(indices[l])
    return list_nondeg, list_deg


def indices_dst_theta_no_gate(
    left_indices: _KeysView[tuple],
    right_indices: _KeysView[tuple],
    *,
    conserve_left_right: bool = False
) -> _List[_Tuple[tuple, tuple, tuple]]:
    about_indices_to_contract = []

    for left_index in left_indices:
        for right_index in right_indices:
            if left_index[2] == right_index[0]:
                if (not conserve_left_right) or (
                    conserve_left_right
                    and (
                        left_index[0] + left_index[1] + right_index[1] == right_index[2]
                    )
                ):
                    about_indices_to_contract.append(
                        (
                            (
                                left_index[0],
                                left_index[1],
                                right_index[1],
                                right_index[2],
                            ),
                            left_index,
                            right_index,
                        )
                    )

    return sorted(set(about_indices_to_contract))


def indices_dst_theta_with_gate(
    theta_indices: _KeysView[tuple],
    gate_indices: _KeysView[tuple],
    *,
    conserve_left_right: bool = False
) -> _List[_Tuple[tuple, tuple, tuple]]:
    destination_indices = []
    for theta_index in theta_indices:
        for gate_index in gate_indices:
            if theta_index[1] == gate_index[0] and theta_index[2] == gate_index[3]:
                if (not conserve_left_right) or (
                    conserve_left_right
                    and (
                        theta_index[0] + gate_index[1] + gate_index[2] == theta_index[3]
                    )
                ):
                    destination_indices.append(
                        (
                            (
                                theta_index[0],
                                gate_index[1],
                                gate_index[2],
                                theta_index[3],
                            ),
                            theta_index,
                            gate_index,
                        )
                    )

    return sorted(set(destination_indices))


def internal_qn_sum(lhs: int, rhs: int) -> int:
    return lhs + rhs


def internal_qn_sub(lhs: int, rhs: int) -> int:
    return lhs - rhs


def potential_middle_indices(
    theta_indices: _List[_Tuple], *, direction_right: int = -1
):
    middle_indices = []
    if direction_right == 0:  # take from left sum
        for theta_index in theta_indices:
            middle_indices.append(internal_qn_sum(theta_index[0], theta_index[1]))
            middle_indices.append(internal_qn_sub(theta_index[3], theta_index[2]))
    elif direction_right in [1, 2]:  # take from left sum
        for theta_index in theta_indices:
            middle_indices.append(internal_qn_sum(theta_index[0], theta_index[1]))
    elif direction_right == -1:  # take from right sub
        for theta_index in theta_indices:
            val = internal_qn_sub(theta_index[3], theta_index[2])
            if val >= 0:  # shouldn't occur but let's be carefull
                middle_indices.append(val)
            else:
                _warning(
                    "warning,qnum problem could arises with substraction of qnums..."
                )
    elif direction_right in [-2, -3]:  # take from right sum
        for theta_index in theta_indices:
            middle_indices.append(internal_qn_sum(theta_index[2], theta_index[3]))

    return sorted(set(middle_indices))


def degeneracy_in_theta(
    keys: _List[_Tuple[int, int, int, int]],
    middle: _List[int],
    *,
    direction_right: int = -1
) -> _Tuple[
    _List[_Tuple[int, _Tuple[int, int, int, int]]],
    _List[_Tuple[int, _List[_Tuple[int, int, int, int]]]],
]:
    nondeg = []
    degenerate = []

    if direction_right == 0:  # conserve right and left qnum
        for j in range(len(middle)):
            tmp = []
            for it in keys:
                if (middle[j] == internal_qn_sum(it[0], it[1])) and (
                    internal_qn_sum(middle[j],it[2]) == it[3]
                ):
                    tmp.append(it)
            if len(tmp) > 1:
                degenerate.append((middle[j], tmp))
            elif len(tmp) == 1:
                nondeg.append((middle[j], tmp[0]))
    elif direction_right == 1:  # conserve left sum qnum
        for j in range(len(middle)):
            tmp = []
            for it in keys:
                if middle[j] == internal_qn_sum(it[0], it[1]):
                    tmp.append(it)
            if len(tmp) > 1:
                degenerate.append((middle[j], tmp))
            elif len(tmp) == 1:
                nondeg.append((middle[j], tmp[0]))
    elif direction_right == 2:  # conserve left sum qnum, no index
        for j in range(len(middle)):
            tmp = []
            for it in keys:
                if middle[j] == internal_qn_sum(it[0], it[1]):
                    tmp.append(it)
            if len(tmp) > 1:
                degenerate.append((j, tmp))
            elif len(tmp) == 1:
                nondeg.append((j, tmp[0]))
    elif direction_right == -1:  # conserve right sub qnum
        for j in range(len(middle)):
            tmp = []
            for it in keys:
                if (
                    internal_qn_sum(middle[j],it[2]) == it[3]
                ):
                    tmp.append(it)
            if len(tmp) > 1:
                degenerate.append((middle[j], tmp))
            elif len(tmp) == 1:
                nondeg.append((middle[j], tmp[0]))
    elif direction_right == -2:  # conserve right only sum qnum, no index
        for j in range(len(middle)):
            tmp = []
            for it in keys:
                if middle[j] == internal_qn_sum(
                    it[3], it[2]
                ):  # note for TDMRG here is a sum according to direction
                    tmp.append(it)
            if len(tmp) > 1:
                degenerate.append((j, tmp))
            elif len(tmp) == 1:
                nondeg.append((j, tmp[0]))
    elif direction_right == -3:  # conserve left sum qnum
        for j in range(len(middle)):
            tmp = []
            for it in keys:
                if middle[j] == internal_qn_sum(it[0], it[1]):
                    tmp.append(it)
            if len(tmp) > 1:
                degenerate.append((middle[j], tmp))
            elif len(tmp) == 1:
                nondeg.append((middle[j], tmp[0]))

    return nondeg, degenerate


def slices_degenerate_blocs(
    theta_blocs: _Dict[_Tuple, _np.ndarray],
    degenerate_list: _List[_Tuple[int, _List[_Tuple[int, int, int, int]]]],
    subnewsize: _List[_List],
) -> None:
    for i in range(len(degenerate_list)):  # for each deg global block
        # define a local basis
        left__loc_basis = sorted(set([(it[0], it[1]) for it in degenerate_list[i][1]]))
        right_loc_basis = sorted(set([(it[2], it[3]) for it in degenerate_list[i][1]]))
        # find the local dim corresponding to left_loc_basis and right_loc_basis
        left__loc_dim = len(left__loc_basis) * [(0, 0)]
        right_loc_dim = len(right_loc_basis) * [(0, 0)]
        # for each local_index
        for it in degenerate_list[i][1]:
            dims = theta_blocs[it].shape
            left__loc_dim[left__loc_basis.index((it[0], it[1]))] = (dims[0], dims[1])
            right_loc_dim[right_loc_basis.index((it[2], it[3]))] = (dims[2], dims[3])
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
