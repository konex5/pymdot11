from copy import deepcopy as _copy


from pyfhmdot.intense.contract import (
    contract_mps_mps_left_border as _contract_mps_mps_left_border,
)
from pyfhmdot.intense.contract import (
    contract_mps_mps_right_border as _contract_mps_mps_right_border,
)
from pyfhmdot.intense.contract import (
    contract_left_small_bloc_mps as _contract_left_small_bloc_mps,
)
from pyfhmdot.intense.contract import (
    contract_right_small_bloc_mps as _contract_right_small_bloc_mps,
)
from pyfhmdot.intense.contract import (
    contract_left_right_small_bloc as _contract_left_right_small_bloc,
)


from pyfhmdot.intense.contract import (
    contract_mps_mpo_mps_left_border as _contract_left_border,
)
from pyfhmdot.intense.contract import contract_left_bloc_mps as _contract_left

from pyfhmdot.intense.contract import (
    contract_mps_mpo_mps_right_border as _contract_right_border,
)
from pyfhmdot.intense.contract import contract_right_bloc_mps as _contract_right

from pyfhmdot.intense.contract import contract_left_right_bloc as _contract_left_right


def measure_mps_mps(mps_one, mps_two, position=-1):
    if position == -1:
        position = len(mps_one) // 2

    tmp_left = {}
    _contract_mps_mps_left_border(tmp_left, mps_one[0], mps_two[0])
    for l in range(1, position + 1, 1):
        tmp = _copy(tmp_left)  # swap
        tmp_left.clear()
        _contract_left_small_bloc_mps(tmp_left, tmp, mps_one[l], mps_two[l])

    tmp.clear()
    tmp_right = {}
    _contract_mps_mps_right_border(tmp_right, mps_one[-1], mps_two[-1])
    for l in range(len(mps_one) - 2, position, -1):
        tmp = _copy(tmp_right)  # swap
        tmp_right.clear()
        _contract_right_small_bloc_mps(tmp_right, tmp, mps_one[l], mps_two[l])

    dst = {}
    _contract_left_right_small_bloc(dst, tmp_left, tmp_right)

    return dst[()][()]


def measure_mps_mpo_mps(mps_one, mpo, mps_two, position=-1):
    if position == -1:
        position = len(mps_one) // 2

    tmp_left = {}
    _contract_left_border(tmp_left, mps_one[0], mpo[0], mps_two[0])
    for l in range(1, position, 1):
        tmp = _copy(tmp_left)  # swap
        tmp_left.clear()
        _contract_left(tmp_left, tmp, mps_one[l], mpo[l], mps_two[l])

    tmp_right = {}
    _contract_right_border(tmp_right, mps_one[0], mpo[0], mps_two[0])
    for l in range(len(mps_one), position, -1):
        tmp = _copy(tmp_right)  # swap
        tmp_right.clear()
        _contract_right(tmp_right, tmp, mps_one[l], mpo[l], mps_two[l])

    dst = {}
    _contract_left_right(dst, tmp_left, tmp_right)

    return dst[()][()]
