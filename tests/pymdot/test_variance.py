import pytest


def test_average_variance(make_maximal_entangled_state_u1):

    from pymdot.models.pymodels import hamiltonian_obc
    from pymdot.intense.splitgroup import split_all

    dmps = split_all("sh_soks_u1", make_maximal_entangled_state_u1(12))
    mpo = hamiltonian_obc("sh_xxz-hz_u1", {"Jxy": 1, "Jz": 2, "hz": 1}, size=12)

    from pymdot.intense.interface import measure_dmps_mpo_dmps

    average = measure_dmps_mpo_dmps(dmps, mpo, dmps)
    assert average == 0

    from pymdot.intense.interface import measure_dmps_mpo_mpo_dmps

    variance = measure_dmps_mpo_mpo_dmps(dmps, mpo, mpo, dmps)
    assert variance != 0
