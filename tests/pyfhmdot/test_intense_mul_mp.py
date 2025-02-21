import pytest

def test_outerprod_mpo():
    from pyfhmdot.models.pymodels import hamiltonian_obc
    from pyfhmdot.intense.mul_mp import multiply_mp
    mpo = hamiltonian_obc('sh_xxz-hz_u1',{"Jxy":1,"Jz":2,"hz":3},10)
    dst = {}
    tmp = {}
    multiply_mp(dst,mpo[8],mpo[9],3,0)
    multiply_mp(tmp,mpo[7],dst,3,0)
    dst.clear()
    multiply_mp(dst,mpo[6],tmp,3,0)
    tmp.clear()
    # multiply_mp(tmp,mpo[5],dst,3,0)
    # dst.clear()
    # multiply_mp(dst,mpo[4],tmp,3,0)
    # tmp.clear()
    # multiply_mp(tmp,mpo[3],dst,3,0)
    # dst.clear()
    # multiply_mp(dst,mpo[2],tmp,3,0)
    # tmp.clear()
    # multiply_mp(tmp,mpo[1],dst,3,0)
    # dst.clear()
    # multiply_mp(dst,mpo[0],tmp,3,0)
    # pass