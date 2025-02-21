import pytest


def test_general():
    import numpy as np

    from pyfhmdot.models.pymodels import suzu_trotter_obc_exp
    from pyfhmdot.models.splitgroup import group_four_dgate, split_four_dgate

    gate = suzu_trotter_obc_exp(
        0.025,
        "sh_xxz-hz_u1",
        {"Jxy": 1, "Jz": 2, "hz": 3},
        3,
        is_dgate=True,
        in_group=False,
    )[1]
    dst_gate_grouped = {}
    group_four_dgate("sh_xxz-hz_u1", dst_gate_grouped, gate)

    dst_dgate_splited = {}
    split_four_dgate("sh_xxz-hz_u1", dst_dgate_splited, dst_gate_grouped)
    for key in gate.keys():
        assert np.all(gate[key] == dst_dgate_splited[key])

    gate = suzu_trotter_obc_exp(
        0.025,
        "sh_xxz-hz_u1",
        {"Jxy": 1, "Jz": 2, "hz": 3},
        3,
        is_dgate=True,
        in_group=True,
    )[1]
    for key in gate.keys():
        assert np.all(gate[key] == dst_gate_grouped[key])
