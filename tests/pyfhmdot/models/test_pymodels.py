import pytest


def test_pyhamiltonian():

    from pyfhmdot.models.pymodels import pyhamiltonian

    a = pyhamiltonian("sh_xxz_no")
    assert a["bond"][0][0] == "Jxy"
    assert a["bond"][0][-1] == "sh_sp_no-sh_sm_no"
    assert a["bond"][2][0] == "Jz"
    assert a["bond"][2][-1] == "sh_sz_no-sh_sz_no"
