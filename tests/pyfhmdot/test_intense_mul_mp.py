import pytest

def test_map_order():
    from pyfhmdot.intense.mul_mp import map_order
    tmp = map_order([0,2,1,3],[0,1,2,3])
    tmp = map_order([0,1,2,3],[0,2,1,3])
    pass

def test_permute_arrays(make_single_dummy_dgate):
    from pyfhmdot.intense.mul_mp import permute_blocs
    theta = make_single_dummy_dgate()
    dst_blocs = {}
    permute_blocs(dst_blocs,theta,[(0,1,2,3),(3,2,0,1)])
    assert dst_blocs[(1,0,1,0)][1,0,1,0] == theta[(1,0,0,1)][1,0,0,1]
    assert dst_blocs[(1,0,1,0)][0,0,1,0] == theta[(1,0,0,1)][1,0,0,0]

def test_trace_mpo(make_single_dummy_dgate):
    from pyfhmdot.intense.mul_mp import trace_mpo
    theta = make_single_dummy_dgate()
    dst_blocs = {}
    trace_mpo(dst_blocs,theta,0,3)
    assert dst_blocs[(0,0)].shape == (1,1)
    

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