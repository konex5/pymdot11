import pytest

from pyfhmdot.models.pymodels import suzu_trotter_obc_exp


def test_pyhamiltonian():

    from pyfhmdot.models.pymodels import pyhamiltonian

    a = pyhamiltonian("sh_xxz_no")
    assert a["nn_bond"][0][0] == "Jxy"
    assert a["nn_bond"][0][-1] == "sh_sp_no-sh_sm_no"
    assert a["nn_bond"][2][0] == "Jz"
    assert a["nn_bond"][2][-1] == "sh_sz_no-sh_sz_no"
    b = pyhamiltonian("sh_xxz-hz_u1")
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
        "sh_xxz-hz_no", {"Jxy": 5.0, "Jz": 3.0, "hz": -0.5}
    )
    assert on_site[0][(0, 0)][0, 0] == 0.5
    nn_bond = nn_bond_operators_from_hamiltonian(
        "sh_xxz-hz_no", {"Jxy": 5.0, "Jz": 3.0, "hz": -0.5}
    )
    assert nn_bond[0][0][(0, 0)][0, 1] == np.sqrt(2.5)


def test_hamiltonian_obc():
    from pyfhmdot.models.pymodels import hamiltonian_obc

    mpo = hamiltonian_obc("sh_xxz-hz_u1", {"Jxy": 7, "Jz": -5, "hz": 3}, size=10)
    assert mpo[0][(0, 1, 1, 4)][0, 0, 0, 0] == 1
    assert mpo[1][(0, 0, 0, 0)][0, 0, 0, 0] == 1
    assert mpo[-1][(0, 1, 1, 0)][0, 0, 0, 0] == 1
    assert mpo[-1][(4, 1, 1, 0)][0, 0, 0, 0] == 3


def test_hamiltonian_gate():
    from pyfhmdot.models.pyoperators import single_operator
    from pyfhmdot.models.pymodels import (
        on_site_operators_from_hamiltonian,
        nn_bond_operators_from_hamiltonian,
        _hamiltonian_gate_from_dense,
        _exp_gate,
    )

    model_name = "sh_xxz-hz_no"
    parameters = {"Jxy": 7, "Jz": -5, "hz": 3}
    head, _, tail = model_name.split("_")
    d = 2

    id_bloc = single_operator(name=head + "_id_" + tail, coef=1.0)
    on_site = on_site_operators_from_hamiltonian(model_name, parameters)
    # fuse on_site

    # fuse
    nn_bond = nn_bond_operators_from_hamiltonian(model_name, parameters)
    before_exp = _hamiltonian_gate_from_dense(id_bloc, on_site, on_site, nn_bond, d=2)

    a = _exp_gate(-0.01j, before_exp, d=2)


def test_gate_exp():
    from pyfhmdot.models.pymodels import suzu_trotter_obc_exp

    model_name = "sh_xxz-hz_u1"
    parameters = {"Jxy": 7, "Jz": -5, "hz": 3}

    a = suzu_trotter_obc_exp(-0.01, model_name, parameters, 10, is_dgate=False,in_group=False)
    model_name = "sh_xxz-hz_no"
    parameters = {"Jxy": 7, "Jz": -5, "hz": 3}
    b = suzu_trotter_obc_exp(-0.01, model_name, parameters, 10, is_dgate=False,in_group=False)

    for i in range(len(b)):
        assert b[i][(0, 0, 0, 0)][0, 0, 0, 0] == a[i][(0, 0, 0, 0)][0, 0, 0, 0]


def test_on_site_fuse():
    from pyfhmdot.models.pymodels import (
        on_site_operators_from_hamiltonian,
        on_site_fuse_for_mpo,
    )
    from pyfhmdot.models.pyoperators import single_operator

    on_site = [
        single_operator("sh_sx_no", coef=2.0),
        single_operator("sh_sy_no", coef=5.0),
    ]
    out_site = on_site_fuse_for_mpo(on_site)
    assert out_site[0][(0, 0)][0, 1] == 2.0 - 5j

    on_site = [
        single_operator("sh_sz_u1", coef=2.0),
        single_operator("sh_sz_u1", coef=5.0),
    ]
    out_site = on_site_fuse_for_mpo(on_site)
    assert out_site[0][(0, 0)][0, 0] == 7.0
    assert out_site[0][(1, 1)][0, 0] == -7.0
