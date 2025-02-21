import pytest

@pytest.mark.skip
def test_conservation():
    from pyfhmdot.conservation import conserve_qnum
    size = 2
    assert conserve_qnum(0,size,qnum_conserved=0) == [0]
    assert conserve_qnum(0,size,qnum_conserved=1) == [0]
    assert conserve_qnum(0,size,qnum_conserved=2) == [0]
    assert conserve_qnum(1,size,qnum_conserved=0) == [0]
    assert conserve_qnum(1,size,qnum_conserved=1) == [0,1]
    assert conserve_qnum(1,size,qnum_conserved=2) == [1]
    assert conserve_qnum(2,size,qnum_conserved=0) == [0]
    assert conserve_qnum(2,size,qnum_conserved=1) == [1]
    assert conserve_qnum(2,size,qnum_conserved=2) == [2]
    size = 3
    assert conserve_qnum(0,size,qnum_conserved=0) == [0]
    assert conserve_qnum(0,size,qnum_conserved=3) == [0]
    assert conserve_qnum(1,size,qnum_conserved=0) == [0]
    assert conserve_qnum(1,size,qnum_conserved=1) == [0,1]
    assert conserve_qnum(1,size,qnum_conserved=2) == [0,1]
    assert conserve_qnum(1,size,qnum_conserved=3) == [1]
    assert conserve_qnum(2,size,qnum_conserved=0) == [0]
    assert conserve_qnum(2,size,qnum_conserved=1) == [0,1]
    assert conserve_qnum(2,size,qnum_conserved=2) == [1,2]
    assert conserve_qnum(2,size,qnum_conserved=3) == [2]
    assert conserve_qnum(3,size,qnum_conserved=0) == [0]
    assert conserve_qnum(3,size,qnum_conserved=1) == [1]
    assert conserve_qnum(3,size,qnum_conserved=2) == [2]
    assert conserve_qnum(3,size,qnum_conserved=3) == [3]
    size = 4
    assert conserve_qnum(0,size,qnum_conserved=0) == [0]
    assert conserve_qnum(0,size,qnum_conserved=4) == [0]
    assert conserve_qnum(1,size,qnum_conserved=0) == [0]
    assert conserve_qnum(1,size,qnum_conserved=1) == [0,1]
    assert conserve_qnum(1,size,qnum_conserved=2) == [0,1]
    assert conserve_qnum(1,size,qnum_conserved=3) == [0,1]
    assert conserve_qnum(1,size,qnum_conserved=4) == [1]
    assert conserve_qnum(2,size,qnum_conserved=0) == [0]
    assert conserve_qnum(2,size,qnum_conserved=1) == [0,1]
    assert conserve_qnum(2,size,qnum_conserved=2) == [0,1,2]
    assert conserve_qnum(2,size,qnum_conserved=3) == [1,2]
    assert conserve_qnum(2,size,qnum_conserved=4) == [2]
    assert conserve_qnum(3,size,qnum_conserved=0) == [0]
    assert conserve_qnum(3,size,qnum_conserved=1) == [0,1]
    assert conserve_qnum(3,size,qnum_conserved=2) == [1,2,3]
    assert conserve_qnum(3,size,qnum_conserved=3) == [2,3]
    assert conserve_qnum(3,size,qnum_conserved=4) == [3]
    assert conserve_qnum(4,size,qnum_conserved=0) == [0]
    assert conserve_qnum(4,size,qnum_conserved=1) == [1]
    assert conserve_qnum(4,size,qnum_conserved=2) == [2]
    assert conserve_qnum(4,size,qnum_conserved=3) == [3]
    assert conserve_qnum(4,size,qnum_conserved=4) == [4]
    size = 5
    
    
    