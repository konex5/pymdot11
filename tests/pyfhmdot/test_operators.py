import pytest


def test_single_operator_dense():
    from pyfhmdot.models.pyoperators import single_operator

    a = single_operator("sh_id_no", coef=3)[(0, 0)]
    assert a[0, 0] == 3 and a[1, 1] == 3
    a = single_operator("sh_sp_u1", coef=3)[(1, 0)]
    assert a[0, 0] == 3
