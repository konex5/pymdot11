import numpy as _np
from typing import Dict as _Dict
from typing import KeysView as _KeysView
from typing import List as _List
from typing import Tuple as _Tuple


def indices_prepare_destination_without_gate(
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


def indices_theta_prepare_conservation_for_gate(
    theta_indices: _KeysView[tuple],
    gate_indices: _KeysView[tuple],
    *,
    conserve_left_right: bool = False
) -> _List[_Tuple[tuple, tuple, tuple]]:
    destination_indices = []
    for theta_index in theta_indices:
        for gate_index in gate_indices:
            if gate_index[2] == theta_index[1] and gate_index[3] == theta_index[2]:
                if (not conserve_left_right) or (
                    conserve_left_right
                    and (
                        theta_index[0] + gate_index[0] + gate_index[1] == theta_index[3]
                    )
                ):
                    destination_indices.append(
                        (
                            (
                                theta_index[0],
                                gate_index[0],
                                gate_index[1],
                                theta_index[3],
                            ),
                            theta_index,
                            gate_index,
                        )
                    )

    return sorted(set(destination_indices))


def list_degenerate_indices(destination_indices: _List[tuple]) -> _List[bool]:
    list_degenerate = []
    for l in range(len(destination_indices)):
        if destination_indices.index(destination_indices[l]) == l:
            is_degenerate = True
        else:
            is_degenerate = False
        list_degenerate.append(is_degenerate)
    return list_degenerate


def multiply_arrays(
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


def multiply_blocs_no_gate_applied(
    dst_blocs: _Dict[tuple, _np.ndarray],
    lhs_blocs: _Dict[tuple, _np.ndarray],
    rhs_blocs: _Dict[tuple, _np.ndarray],
    *,
    conserve_left_right: bool = False
) -> None:
    dest_indices = indices_prepare_destination_without_gate(
        lhs_blocs.keys(), rhs_blocs.keys(), conserve_left_right=conserve_left_right
    )
    multiply_arrays(dst_blocs, lhs_blocs, rhs_blocs, dest_indices)


def multiply_arrays_and_transpose(
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


def multiply_blocs_with_gate_applied(
    dst_blocs: _Dict[tuple, _np.ndarray],
    lhs_blocs: _Dict[tuple, _np.ndarray],
    rhs_blocs: _Dict[tuple, _np.ndarray],
    gate_blocs: _Dict[tuple, _np.ndarray],
    *,
    conserve_left_right_before: bool = False,
    conserve_left_right_after: bool = False
) -> None:
    tmp_indices = indices_prepare_destination_without_gate(
        lhs_blocs.keys(),
        rhs_blocs.keys(),
        conserve_left_right=conserve_left_right_before,
    )
    tmp_blocs: _Dict[tuple, _np.ndarray] = {}
    multiply_arrays(tmp_blocs, lhs_blocs, rhs_blocs, tmp_indices)
    dest_indices = indices_theta_prepare_conservation_for_gate(
        tmp_blocs.keys(),
        gate_blocs.keys(),
        conserve_left_right=conserve_left_right_after,
    )
    multiply_arrays_and_transpose(dst_blocs, tmp_blocs, gate_blocs, dest_indices)
