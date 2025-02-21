import pytest

def test_contract_left(make_single_blocs_mps):
    from pyfhmdot.models.pymodels import hamiltonian_obc
    from pyfhmdot.intense.contract import contract_mps_mpo_mps_left
    mpo = hamiltonian_obc("sh_xxz-hz_u1", {"Jxy": 0, "Jz": 0, "hz": 10}, 2)
    mps_down_left = mpo[0]
    mps_up_left = mpo[0]
    mpo = mpo[0]
    dst = {}
    contract_mps_mpo_mps_left(dst,mps_down_left,mpo,mps_up_left)

