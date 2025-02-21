from typing import Dict as _Dict
from typing import KeysView as _KeysView
from typing import List as _List
from typing import Tuple as _Tuple
import numpy as _np


def permute_blocs(new_blocks, old_blocks, map_old2new):
    for it in old_blocks.keys():
        tmp = list(it)
        for i in range(len(it)):
            tmp[map_old2new[1][i]] = it[map_old2new[0][i]]
        new_blocks[tuple(tmp)] = old_blocks[it].transpose(
            [
                i
                for j, y in enumerate(map_old2new[0])
                for i, x in enumerate(map_old2new[1])
                if (x == y)
            ]
        )


def rm_border_mpo(dst_blocs, mpo_blocs, is_left):
    for it in mpo_blocs.keys():
        if is_left:
            dst_indices = (it[1], it[2], it[3])
            tmp = mpo_blocs[it].shape
            dst_shape = (tmp[1], tmp[2], tmp[3])
        else:
            dst_indices = (it[0], it[1], it[2])
            tmp = mpo_blocs[it].shape
            dst_shape = (tmp[0], tmp[1], tmp[2])
        dst_blocs[dst_indices] = mpo_blocs[it].reshape(dst_shape)


def fuse_mp(dst_blocs, mpo_blocs, index):
    """
    This method is used for ED only
    fuse index and index+1
    """
    # deg1 = len(set([_[index] for _ in mpo_blocs.keys()]))
    deg2 = len(set([_[index + 1] for _ in mpo_blocs.keys()]))

    def get_fused_index(key, index, deg2):
        return key[index] * deg2 + key[index + 1]

    for it in mpo_blocs.keys():
        dst_indices = tuple(
            [_ for i, _ in enumerate(it) if i < index]
            + [get_fused_index(it, index, deg2)]
            + [_ for i, _ in enumerate(it) if i > index + 1]
        )
        tmp = mpo_blocs[it].shape
        dst_shape = tuple(
            [_ for i, _ in enumerate(tmp) if i < index]
            + [tmp[index] * tmp[index + 1]]
            + [_ for i, _ in enumerate(tmp) if i > index + 1]
        )
        dst_blocs[dst_indices] = mpo_blocs[it].reshape(dst_shape)


def trace_mp(dst_blocs, mpo_blocs, index1, index2):
    for it in mpo_blocs.keys():
        dst_indices = tuple([_ for i, _ in enumerate(it) if i not in [index1, index2]])
        if dst_indices in dst_blocs.keys():
            dst_blocs[dst_indices] += _np.trace(
                mpo_blocs[it], axis1=index1, axis2=index2
            )
        else:
            dst_blocs[dst_indices] = _np.trace(
                mpo_blocs[it], axis1=index1, axis2=index2
            )


def indices_dst_mul_mpo(
    left_indices: _KeysView[tuple],
    right_indices: _KeysView[tuple],
    lind: int,
    rind: int,
) -> _List[_Tuple[tuple, tuple, tuple]]:
    about_indices_to_contract = []

    for left_index in left_indices:
        for right_index in right_indices:
            if _np.all(
                [left_index[lind[i]] == right_index[rind[i]] for i in range(len(lind))]
            ):
                about_indices_to_contract.append(
                    (
                        tuple(
                            [
                                left_index[i]
                                for i in range(len(left_index))
                                if i not in lind
                            ]
                            + [
                                right_index[i]
                                for i in range(len(right_index))
                                if i not in rind
                            ]
                        ),
                        left_index,
                        right_index,
                    )
                )

    return sorted(set(about_indices_to_contract))


def multiply_mp(
    new_blocks: _Dict[tuple, _np.ndarray],
    old_blocks1: _Dict[tuple, _np.ndarray],
    old_blocks2: _Dict[tuple, _np.ndarray],
    index1: int,
    index2: int,
) -> None:
    """
    This method is used for ED
    """
    from pyfhmdot.routine.indices import list_degenerate_indices

    buildtarget = indices_dst_mul_mpo(
        old_blocks1.keys(), old_blocks2.keys(), index1, index2
    )

    list_isnew = list_degenerate_indices([_[0] for _ in buildtarget])
    for new, it in zip(list_isnew, buildtarget):
        target, it1, it2 = it[0], it[1], it[2]
        if new:
            new_blocks[target] = _np.tensordot(
                old_blocks1[it1],
                old_blocks2[it2],
                axes=(index1, index2),
            )
        else:
            new_blocks[target] += _np.tensordot(
                old_blocks1[it1],
                old_blocks2[it2],
                axes=(index1, index2),
            )
