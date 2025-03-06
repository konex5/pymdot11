import pytest


def test_mapping():
    from pymdot.intense.splitgroup import splitgroup_mapping

    assert splitgroup_mapping("sh_xxz-hz_u1", section="deg")[0] == 1
    assert splitgroup_mapping("sh_xxz-hz_no", section="deg")[0] == 2


def test_reshape_group(make_maximal_entangled_state_u1):
    import numpy as np
    from pymdot.intense.splitgroup import reshape_and_split, reshape_and_group

    dmps = make_maximal_entangled_state_u1(3)[0]
    dst_blocs = {}

    reshape_and_split("sh_blabla_u1", dst_blocs, dmps, 1)
    assert dst_blocs[(0, 0, 0, 0)][0, 0, 0, 0] == 1 / np.sqrt(2)

    dst_dst_blocs = {}
    reshape_and_group("sh_blabla_u1", dst_dst_blocs, dst_blocs, [1, 2])
    assert np.all(dst_dst_blocs[(0, 1, 0)][0, :, 0] == dmps[(0, 1, 0)][0, :, 0])
