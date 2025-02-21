import pytest

def test_contract_left():
    from pyfhmdot.models.pymodels import hamiltonian_obc
    from pyfhmdot.intense.contract import contract_mps_mpo_mps_left_border, contract_left_bloc
    mpo = hamiltonian_obc("sh_xxz-hz_u1", {"Jxy": 0, "Jz": 0, "hz": 10}, 3)
    mps_down_left = mpo[0]
    mps_up_left = mpo[0]
    mpo_left = mpo[0]
    dst = {}
    contract_mps_mpo_mps_left_border(dst,mps_down_left,mpo_left,mps_up_left)
    assert [len(_) for _ in dst.keys()][0] == 3
    #
    mps_down = mpo[1]
    mps_up = mpo[1]
    mpo_middle = mpo[1]
    new_dst = {}
    contract_left_bloc(new_dst,dst,mps_down,mpo_middle,mps_up)
    assert [len(_) for _ in new_dst.keys()][0] == 3
    return new_dst

def test_contract_right():
    from pyfhmdot.models.pymodels import hamiltonian_obc
    from pyfhmdot.intense.contract import contract_mps_mpo_mps_right_border, contract_right_bloc
    mpo = hamiltonian_obc("sh_xxz-hz_u1", {"Jxy": 0, "Jz": 0, "hz": 10}, 3)
    mps_down_left = mpo[-1]
    mps_up_left = mpo[-1]
    mpo_left = mpo[-1]
    dst = {}
    contract_mps_mpo_mps_right_border(dst,mps_down_left,mpo_left,mps_up_left)
    assert [len(_) for _ in dst.keys()][0] == 3
    #
    mps_down = mpo[1]
    mps_up = mpo[1]
    mpo_middle = mpo[1]
    new_dst = {}
    contract_right_bloc(new_dst,dst,mps_down,mpo_middle,mps_up)
    assert [len(_) for _ in new_dst.keys()][0] == 3
    return new_dst

def test_contract_middle():
    left = test_contract_left()
    right = test_contract_right()