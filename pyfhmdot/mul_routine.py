import numpy as _np
from typing import Dict as _Dict
from typing import List as _List
from typing import Tuple as _Tuple

from pyfhmdot.indices import list_degenerate_indices


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
