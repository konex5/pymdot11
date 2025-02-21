import pytest


def test_conservation():
    from pyfhmdot.conservation import conserve_qnum

    size = 2
    assert list(conserve_qnum(0, size=size, qnum_conserved=0, d=2)) == [0]
    assert list(conserve_qnum(0, size=size, qnum_conserved=1, d=2)) == [0]
    assert list(conserve_qnum(0, size=size, qnum_conserved=2, d=2)) == [0]
    assert list(conserve_qnum(1, size=size, qnum_conserved=0, d=2)) == [0]
    assert list(conserve_qnum(1, size=size, qnum_conserved=1, d=2)) == [0, 1]
    assert list(conserve_qnum(1, size=size, qnum_conserved=2, d=2)) == [1]
    assert list(conserve_qnum(2, size=size, qnum_conserved=0, d=2)) == [0]
    assert list(conserve_qnum(2, size=size, qnum_conserved=1, d=2)) == [1]
    assert list(conserve_qnum(2, size=size, qnum_conserved=2, d=2)) == [2]
    size = 3
    assert list(conserve_qnum(0, size=size, qnum_conserved=0, d=2)) == [0]
    assert list(conserve_qnum(0, size=size, qnum_conserved=3, d=2)) == [0]
    assert list(conserve_qnum(1, size=size, qnum_conserved=0, d=2)) == [0]
    assert list(conserve_qnum(1, size=size, qnum_conserved=1, d=2)) == [0, 1]
    assert list(conserve_qnum(1, size=size, qnum_conserved=2, d=2)) == [0, 1]
    assert list(conserve_qnum(1, size=size, qnum_conserved=3, d=2)) == [1]
    assert list(conserve_qnum(2, size=size, qnum_conserved=0, d=2)) == [0]
    assert list(conserve_qnum(2, size=size, qnum_conserved=1, d=2)) == [0, 1]
    assert list(conserve_qnum(2, size=size, qnum_conserved=2, d=2)) == [1, 2]
    assert list(conserve_qnum(2, size=size, qnum_conserved=3, d=2)) == [2]
    assert list(conserve_qnum(3, size=size, qnum_conserved=0, d=2)) == [0]
    assert list(conserve_qnum(3, size=size, qnum_conserved=1, d=2)) == [1]
    assert list(conserve_qnum(3, size=size, qnum_conserved=2, d=2)) == [2]
    assert list(conserve_qnum(3, size=size, qnum_conserved=3, d=2)) == [3]
    size = 4
    assert list(conserve_qnum(0, size=size, qnum_conserved=0, d=2)) == [0]
    assert list(conserve_qnum(0, size=size, qnum_conserved=4, d=2)) == [0]
    assert list(conserve_qnum(1, size=size, qnum_conserved=0, d=2)) == [0]
    assert list(conserve_qnum(1, size=size, qnum_conserved=1, d=2)) == [0, 1]
    assert list(conserve_qnum(1, size=size, qnum_conserved=2, d=2)) == [0, 1]
    assert list(conserve_qnum(1, size=size, qnum_conserved=3, d=2)) == [0, 1]
    assert list(conserve_qnum(1, size=size, qnum_conserved=4, d=2)) == [1]
    assert list(conserve_qnum(2, size=size, qnum_conserved=0, d=2)) == [0]
    assert list(conserve_qnum(2, size=size, qnum_conserved=1, d=2)) == [0, 1]
    assert list(conserve_qnum(2, size=size, qnum_conserved=2, d=2)) == [0, 1, 2]
    assert list(conserve_qnum(2, size=size, qnum_conserved=3, d=2)) == [1, 2]
    assert list(conserve_qnum(2, size=size, qnum_conserved=4, d=2)) == [2]
    assert list(conserve_qnum(3, size=size, qnum_conserved=0, d=2)) == [0]
    assert list(conserve_qnum(3, size=size, qnum_conserved=1, d=2)) == [0, 1]
    assert list(conserve_qnum(3, size=size, qnum_conserved=2, d=2)) == [1, 2]
    assert list(conserve_qnum(3, size=size, qnum_conserved=3, d=2)) == [2, 3]
    assert list(conserve_qnum(3, size=size, qnum_conserved=4, d=2)) == [3]
    assert list(conserve_qnum(4, size=size, qnum_conserved=0, d=2)) == [0]
    assert list(conserve_qnum(4, size=size, qnum_conserved=1, d=2)) == [1]
    assert list(conserve_qnum(4, size=size, qnum_conserved=2, d=2)) == [2]
    assert list(conserve_qnum(4, size=size, qnum_conserved=3, d=2)) == [3]
    assert list(conserve_qnum(4, size=size, qnum_conserved=4, d=2)) == [4]
    size = 5
