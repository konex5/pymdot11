import pytest


def contract_left():
    from pyfhmdot.models.pymodels import hamiltonian_obc
    from pyfhmdot.intense.contract import (
        contract_dmps_mpo_dmps_left_border,
        contract_left_bloc_dmps,
    )

    mpo = hamiltonian_obc("sh_xxz-hz_u1", {"Jxy": 0, "Jz": 0, "hz": 10}, 3)
    mps_down_left = mpo[0]
    mps_up_left = mpo[0]
    mpo_left = mpo[0]
    dst = {}
    contract_dmps_mpo_dmps_left_border(dst, mps_down_left, mpo_left, mps_up_left)
    assert [len(_) for _ in dst.keys()][0] == 3
    #
    mps_down = mpo[1]
    mps_up = mpo[1]
    mpo_middle = mpo[1]
    new_dst = {}
    contract_left_bloc_dmps(new_dst, dst, mps_down, mpo_middle, mps_up)
    assert [len(_) for _ in new_dst.keys()][0] == 3
    return new_dst


def contract_right():
    from pyfhmdot.models.pymodels import hamiltonian_obc
    from pyfhmdot.intense.contract import (
        contract_dmps_mpo_dmps_right_border,
        contract_right_bloc_dmps,
    )

    mpo = hamiltonian_obc("sh_xxz-hz_u1", {"Jxy": 0, "Jz": 0, "hz": 10}, 3)
    mps_down_left = mpo[-1]
    mps_up_left = mpo[-1]
    mpo_left = mpo[-1]
    dst = {}
    contract_dmps_mpo_dmps_right_border(dst, mps_down_left, mpo_left, mps_up_left)
    assert [len(_) for _ in dst.keys()][0] == 3
    #
    mps_down = mpo[1]
    mps_up = mpo[1]
    mpo_middle = mpo[1]
    new_dst = {}
    contract_right_bloc_dmps(new_dst, dst, mps_down, mpo_middle, mps_up)
    assert [len(_) for _ in new_dst.keys()][0] == 3
    return new_dst


def test_contract_middle():
    from pyfhmdot.intense.contract import contract_left_right_bloc

    left = contract_left()
    right = contract_right()
    dst = {}
    contract_left_right_bloc(dst, left, right)
    assert dst[()][()] == 0.0
