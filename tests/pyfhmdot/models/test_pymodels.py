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
