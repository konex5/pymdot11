import pytest


def test_general():
    from pyfhmdot.general import create_hamiltonian_gates
    from pyfhmdot.models.splitgroup import split_four_dgate

    dmps = create_hamiltonian_gates("sh_xxz-hz_u1",{"Jz":1,"Jxy":2,"hz":5},10,dbeta=0.01,is_dgate=True,in_group=True)

    dst_dgate = {}
    split_four_dgate("sh_xxz-hz_u1",dst_dgate,dmps[0][0])