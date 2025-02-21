import pytest

def test_outerprod_mpo():
    from pyfhmdot.models.pymodels import hamiltonian_obc
    from pyfhmdot.intense.mul_mp import multiply_mp, fuse_mp, permute_blocs
    import numpy as np
    from scipy.linalg import eig
    mpo = hamiltonian_obc("sh_xxz-hz_u1", {"Jxy": 0, "Jz": 0, "hz": 10}, 4)
    dst = {}
    tmpL = {}
    tmpR = {}
    tmp = {}
    fuse_mp(tmpL,mpo[0],0)
    fuse_mp(tmpR,mpo[3],2)
    multiply_mp(tmp, tmpL, mpo[1], 2, 0)
    dst.clear()
    permute_blocs(dst,tmp,[(0,1,2,3,4),(0,2,1,3,4)])
    tmp.clear()
    fuse_mp(tmp,dst,0)
    dst.clear()
    fuse_mp(dst,tmp,1)
    tmp.clear()
    multiply_mp(tmp, dst, mpo[2], 2, 0)
    dst.clear()
    permute_blocs(dst,tmp,[(0,1,2,3,4),(0,2,1,3,4)])
    tmp.clear()
    fuse_mp(tmp,dst,0)
    dst.clear()
    fuse_mp(dst,tmp,1)
    tmp.clear()
    multiply_mp(tmp, dst, tmpR, 2, 0)
    dst.clear()
    permute_blocs(dst,tmp,[(0,1,2,3),(0,2,1,3)])
    tmp.clear()
    fuse_mp(tmp,dst,0)
    dst.clear()
    fuse_mp(dst,tmp,1)
    
    res = np.ndarray((2**4,2**4))
    res.fill(0)
    for i,j in dst.keys():
        res[i,j] = dst[(i,j)][0,0]
    
    eig(res)

