import pytest


def test_operator_mpo():
    from pyfhmdot.models.pyoperators import operator_mpo

    mpo = operator_mpo("sh_sz_no", 7.0, 4, size=10)
    assert len(mpo) == 10
    assert mpo[3][(0, 0, 0, 0)][0, 1, 1, 0] == -7

    mpo = operator_mpo("sh_sz_no", 7.0, 10, size=10)
    assert len(mpo) == 10
    assert mpo[9][(0, 0, 0, 0)][0, 1, 1, 0] == -7
    
    mpo = operator_mpo("sh_sz_no", 7.0, 1, size=10)
    assert len(mpo) == 10
    assert mpo[0][(0, 0, 0, 0)][0, 1, 1, 0] == -7

    mpo = operator_mpo("sh_sz_no-sh_sz_no", 49.0, 4, size=10)
    assert len(mpo) == 10
    assert mpo[3][(0, 0, 0, 0)][0, 1, 1, 0] == -7
    assert mpo[4][(0, 0, 0, 0)][0, 1, 1, 0] == -7

    mpo = operator_mpo("sh_sz_no-sh_sz_no", 49.0, 1, size=10)
    assert len(mpo) == 10
    assert mpo[0][(0, 0, 0, 0)][0, 1, 1, 0] == -7
    assert mpo[1][(0, 0, 0, 0)][0, 1, 1, 0] == -7

    mpo = operator_mpo("sh_sz_no-sh_sz_no", 49.0, 9, size=10)
    assert len(mpo) == 10
    assert mpo[8][(0, 0, 0, 0)][0, 1, 1, 0] == -7
    assert mpo[9][(0, 0, 0, 0)][0, 1, 1, 0] == -7
