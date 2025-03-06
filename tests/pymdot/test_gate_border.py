import pytest


def test_gate_border():
    from numpy import all, any
    from pymdot.initialize import create_hamiltonian_gates

    ggate = create_hamiltonian_gates(
        "sh_xxz-hz_u1",
        {"Jxy": 0.25, "Jz": 0.5, "hz": 1.5},  # 1/4.*1, 1/4.*2, 1/2.*3
        10,
        dbeta=0.025,
        is_dgate=True,
        in_group=True,
    )

    for key in ggate[0][1].keys():
        assert all(ggate[0][1][key] == ggate[0][-2][key])

    should_be_at_least_one_true = []
    for key in ggate[0][0].keys():
        should_be_at_least_one_true.append(all(ggate[0][0][key] != ggate[0][1][key]))
    assert any(should_be_at_least_one_true)

    should_be_at_least_one_true = []
    for key in ggate[0][-1].keys():
        should_be_at_least_one_true.append(all(ggate[0][-2][key] != ggate[0][-1][key]))
    assert any(should_be_at_least_one_true)
