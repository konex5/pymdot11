from asyncio.proactor_events import _ProactorBaseWritePipeTransport
import pytest


def test_pyhamiltonian():

    from pyfhmdot.models.pymodels import pyhamiltonian

    a = pyhamiltonian("sh_xxz_no")
    assert a["nn_bond"][0][0] == "Jxy"
    assert a["nn_bond"][0][-1] == "sh_sp_no-sh_sm_no"
    assert a["nn_bond"][2][0] == "Jz"
    assert a["nn_bond"][2][-1] == "sh_sz_no-sh_sz_no"
    b = pyhamiltonian("sh_xxz_hz_u1")
    assert b["nn_bond"][0][0] == "Jxy"
    assert b["nn_bond"][0][-1] == "sh_sp_u1-sh_sm_u1"
    assert b["nn_bond"][2][0] == "Jz"
    assert b["nn_bond"][2][-1] == "sh_sz_u1-sh_sz_u1"
    assert b["on_site"][0][0] == "hz"
    assert b["on_site"][0][-1] == "sh_sz_u1"


def test_operators_from_hamiltonian():
    from pyfhmdot.models.pymodels import (
        on_site_operators_from_hamiltonian,
        nn_bond_operators_from_hamiltonian,
    )
    import numpy as np

    on_site = on_site_operators_from_hamiltonian(
        "sh_xxz_hz_no", {"Jxy": 5.0, "Jz": 3.0, "hz": -0.5}
    )
    assert on_site[0][(0, 0)][0, 0] == 0.5
    nn_bond = nn_bond_operators_from_hamiltonian(
        "sh_xxz_hz_no", {"Jxy": 5.0, "Jz": 3.0, "hz": -0.5}
    )
    assert nn_bond[0][0][(0, 0)][0, 1] == np.sqrt(2.5)


def test_hamiltonian_obc():
    from pyfhmdot.models.pymodels import hamiltonian_obc

    mpo = hamiltonian_obc("sh_xxz-hz_u1", {"Jxy": 7, "Jz": -5, "hz": 3}, size=10)
    assert mpo[0][(0, 1, 1, 4)][0, 0, 0, 0] == 1
    assert mpo[1][(0, 0, 0, 0)][0, 0, 0, 0] == 1
    assert mpo[-1][(0, 1, 1, 0)][0, 0, 0, 0] == 1
    assert mpo[-1][(4, 1, 1, 0)][0, 0, 0, 0] == 3
