import pytest


def test_single_operator_dense():
    from pyfhmdot.models.pyoperators import single_operator

    a = single_operator("sh_id_no", coef=3)[(0, 0)]
    assert a[0, 0] == 3 and a[1, 1] == 3
    a = single_operator("sh_sp_u1", coef=3)[(1, 0)]
    assert a[0, 0] == 3


def test_two_sites_bond_operator():
    from pyfhmdot.models.pyoperators import two_sites_bond_operator

    blocs_left, blocs_right = two_sites_bond_operator(
        "sh_id_u1-sh_id_u1", 4.0, weight_on_left=True
    )
    assert blocs_left[(0, 0)][0, 0] == 4
    assert blocs_right[(0, 0)][0, 0] == 1
