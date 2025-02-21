import pytest


from pyfhmdot.pyoperators import single_operator_dense


def test_single_operator_dense():
    a = single_operator_dense("sh_id_no", coef=3)[0][(0, 0)]
    assert a[0, 0] == 3 and a[1, 1] == 3
    a = single_operator_dense("sh_sp_u1", coef=3)[0][(1, 0)]
    assert a[0, 0] == 3
