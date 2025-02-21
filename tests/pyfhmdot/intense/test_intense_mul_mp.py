import pytest


def test_map_order():
    from pyfhmdot.intense.mul_mp import map_order

    tmp = map_order([0, 2, 1, 3], [0, 1, 2, 3])
    tmp = map_order([0, 1, 2, 3], [0, 2, 1, 3])
    pass


def test_permute_arrays(make_single_dummy_dgate):
    from pyfhmdot.intense.mul_mp import permute_blocs

    theta = make_single_dummy_dgate()
    dst_blocs = {}
    permute_blocs(dst_blocs, theta, [(0, 1, 2, 3), (3, 2, 0, 1)])
    assert dst_blocs[(1, 0, 1, 0)][1, 0, 1, 0] == theta[(1, 0, 0, 1)][1, 0, 0, 1]
    assert dst_blocs[(1, 0, 1, 0)][0, 0, 1, 0] == theta[(1, 0, 0, 1)][1, 0, 0, 0]


def test_trace_mpo(make_single_dummy_dgate):
    from pyfhmdot.intense.mul_mp import trace_mp

    theta = make_single_dummy_dgate()
    dst_blocs = {}
    trace_mp(dst_blocs, theta, 0, 3)
    assert dst_blocs[(0, 0)].shape == (1, 1)


def test_fuse_mpo(make_single_dummy_dgate):
    from pyfhmdot.intense.mul_mp import fuse_mp

    theta = make_single_dummy_dgate()
    dst_blocs = {}
    fuse_mp(dst_blocs, theta, 0)
    pass
