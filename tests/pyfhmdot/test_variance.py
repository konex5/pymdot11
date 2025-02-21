import pytest


def test_average_variance(make_maximal_entangled_state_u1):
    
    from pyfhmdot.models.pymodels import hamiltonian_obc
    from pyfhmdot.intense.splitgroup import split_all
    dmps = split_all("sh_soks_u1", make_maximal_entangled_state_u1(12))

    

    mpo = hamiltonian_obc("sh_xxz-hz_u1", {"Jxy": 1, "Jz": 2, "hz": 0.5}, size=12)

    from pyfhmdot.intense.interface import measure_dmps_mpo_dmps
    average=measure_dmps_mpo_dmps(dmps,mpo,dmps)
    assert average == 0