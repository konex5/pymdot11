from copy import deepcopy as _copy


from pyfhmdot.intense.contract import (
    contract_dmps_dmps_left_border as _contract_dmps_dmps_left_border,
)
from pyfhmdot.intense.contract import (
    contract_dmps_dmps_right_border as _contract_dmps_dmps_right_border,
)
from pyfhmdot.intense.contract import (
    contract_dmps_left_border as _contract_dmps_left_border,
)
from pyfhmdot.intense.contract import (
    contract_left_right_small_bloc as _contract_left_right_small_bloc,
)
from pyfhmdot.intense.contract import (
    contract_left_small_bloc_dmps as _contract_left_small_bloc_dmps,
)
from pyfhmdot.intense.contract import (
    contract_right_small_bloc_dmps as _contract_right_small_bloc_dmps,
)

from pyfhmdot.intense.contract import (
    contract_dmps_right_border as _contract_dmps_right_border,
)
from pyfhmdot.intense.contract import (
    contract_left_very_small_bloc_dmps as _contract_left_very_small_bloc_dmps,
)
from pyfhmdot.intense.contract import (
    contract_right_very_small_bloc_dmps as _contract_right_very_small_bloc_dmps,
)
from pyfhmdot.intense.contract import (
    contract_left_right_very_small_bloc as _contract_left_right_very_small_bloc,
)


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

from pyfhmdot.intense.contract import (
    contract_dmps_mpo_dmps_left_border as _contract_left_border_big,
)
from pyfhmdot.intense.contract import (
    contract_dmps_mpo_dmps_right_border as _contract_right_border_big,
)
from pyfhmdot.intense.contract import contract_left_bloc_dmps as _contract_left_big
from pyfhmdot.intense.contract import contract_right_bloc_dmps as _contract_right_big
from pyfhmdot.intense.contract import (
    contract_left_right_bloc as _contract_left_right_big,
)

from pyfhmdot.intense.contract import (
    contract_dmps_mpo_mpo_dmps_left_border as _contract_left_border_very_big,
)
from pyfhmdot.intense.contract import (
    contract_dmps_mpo_mpo_dmps_right_border as _contract_right_border_very_big,
)
from pyfhmdot.intense.contract import (
    contract_left_very_big_bloc_dmps as _contract_left_very_big,
)
from pyfhmdot.intense.contract import (
    contract_right_very_big_bloc_dmps as _contract_right_very_big,
)
from pyfhmdot.intense.contract import (
    contract_left_right_very_big_bloc as _contract_left_right_very_big,
)


def measure_dmps(mps_one, position=-1):
    if position == -1:
        position = len(mps_one) // 2

    tmp_left = {}
    _contract_dmps_left_border(tmp_left, mps_one[0])
    tmp = {}
    for l in range(1, position + 1, 1):
        tmp, tmp_left = tmp_left, tmp  # swap
        tmp_left.clear()
        _contract_left_very_small_bloc_dmps(tmp_left, tmp, mps_one[l])

    tmp_right = {}
    _contract_dmps_right_border(tmp_right, mps_one[-1])
    tmp.clear()
    for l in range(len(mps_one) - 2, position, -1):
        tmp, tmp_right = tmp_right, tmp  # swap
        tmp_right.clear()
        _contract_right_very_small_bloc_dmps(tmp_right, tmp, mps_one[l])

    dst = {}
    _contract_left_right_very_small_bloc(dst, tmp_left, tmp_right)

    return dst[()][()]


def measure_dmps_dmps(dmps_one, dmps_two, position=-1):
    if position == -1:
        position = len(dmps_one) // 2

    tmp_left = {}
    _contract_dmps_dmps_left_border(tmp_left, dmps_one[0], dmps_two[0])
    tmp = {}
    for l in range(1, position + 1, 1):
        tmp, tmp_left = tmp_left, tmp  # swap
        tmp_left.clear()
        _contract_left_small_bloc_dmps(tmp_left, tmp, dmps_one[l], dmps_two[l])

    tmp_right = {}
    _contract_dmps_dmps_right_border(tmp_right, dmps_one[-1], dmps_two[-1])
    tmp.clear()
    for l in range(len(dmps_one) - 2, position, -1):
        tmp, tmp_right = tmp_right, tmp  # swap
        tmp_right.clear()
        _contract_right_small_bloc_dmps(tmp_right, tmp, dmps_one[l], dmps_two[l])

    dst = {}
    _contract_left_right_small_bloc(dst, tmp_left, tmp_right)

    return dst[()][()]


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
    _contract_right_border(tmp_right, mps_one[-1], mpo[-1], mps_two[-1])
    for l in range(len(mps_one)-2, position, -1):
        tmp = _copy(tmp_right)  # swap
        tmp_right.clear()
        _contract_right(tmp_right, tmp, mps_one[l], mpo[l], mps_two[l])

    dst = {}
    _contract_left_right(dst, tmp_left, tmp_right)

    return dst[()][()]


def measure_dmps_mpo_dmps(dmps_one, mpo, dmps_two, position=-1):
    if position == -1:
        position = len(dmps_one) // 2

    tmp_left = {}
    _contract_left_border_big(tmp_left, dmps_one[0], mpo[0], dmps_two[0])
    tmp = {}
    for l in range(1, position, 1):
        tmp, tmp_left = tmp_left, tmp  # swap
        _contract_left_big(tmp_left, tmp, dmps_one[l], mpo[l], dmps_two[l])

    tmp_right = {}
    _contract_right_border_big(tmp_right, dmps_one[-1], mpo[-1], dmps_two[-1])
    tmp = {}
    for l in range(len(dmps_one) - 2, position, -1):
        tmp, tmp_right = tmp_right, tmp  # swap
        _contract_right_big(tmp_right, tmp, dmps_one[l], mpo[l], dmps_two[l])

    dst = {}
    _contract_left_right_big(dst, tmp_left, tmp_right)

    return dst[()][()]


def measure_dmps_mpo_mpo_dmps(dmps_one, mpo_one, mpo_two, dmps_two, position=-1):
    if position == -1:
        position = len(dmps_one) // 2

    tmp_left = {}
    _contract_left_border_very_big(
        tmp_left, dmps_one[0], mpo_one[0], mpo_two[0], dmps_two[0]
    )
    tmp = {}
    for l in range(1, position, 1):
        tmp, tmp_left = tmp_left, tmp  # swap
        _contract_left_very_big(
            tmp_left, tmp, dmps_one[l], mpo_one[l], mpo_two[l], dmps_two[l]
        )

    tmp_right = {}
    _contract_right_border_very_big(
        tmp_right, dmps_one[-1], mpo_one[-1], mpo_two[-1], dmps_two[-1]
    )
    tmp = {}
    for l in range(len(dmps_one) - 2, position, -1):
        tmp, tmp_right = tmp_right, tmp  # swap
        _contract_right_very_big(
            tmp_right, tmp, dmps_one[l], mpo_one[l], mpo_two[l], dmps_two[l]
        )

    dst = {}
    _contract_left_right_very_big(dst, tmp_left, tmp_right)

    return dst[()][()]
