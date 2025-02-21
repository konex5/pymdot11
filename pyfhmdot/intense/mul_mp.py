from typing import Dict as _Dict
from typing import KeysView as _KeysView
from typing import List as _List
from typing import Tuple as _Tuple
import numpy as _np

from pyfhmdot.routine.indices import list_degenerate_indices


def indices_dst_mul_mpo(
        left_indices: _KeysView[tuple],
        right_indices: _KeysView[tuple], lind: int, rind: int) -> _List[_Tuple[tuple, tuple, tuple]]:
    about_indices_to_contract = []

    for left_index in left_indices:
        for right_index in right_indices:
            if left_index[lind] == right_index[rind]:
                about_indices_to_contract.append((
                    tuple(
                        [
                            left_index[i]
                            for i in range(len(left_index))
                            if i is not lind
                        ]
                        + [
                            right_index[i]
                            for i in range(len(right_index))
                            if i is not rind
                        ]
                    ),
                    left_index,
                    right_index)
                )

    return sorted(set(about_indices_to_contract))


def multiply_mp(new_blocks: _Dict[tuple, _np.ndarray],
                old_blocks1: _Dict[tuple, _np.ndarray],
                old_blocks2: _Dict[tuple, _np.ndarray],
                index1: int,
                index2: int
                ) -> None:
    """
    This method is used for ED
    """
    from pyfhmdot.routine.indices import list_degenerate_indices
    buildtarget = indices_dst_mul_mpo(old_blocks1.keys(), old_blocks2.keys(),index1,index2)
    
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


