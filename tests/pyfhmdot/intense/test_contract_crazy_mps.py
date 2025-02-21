import pytest


def test_contract_left(make_single_blocs_mps, lhs_indices, lhs_chi_shapes):
    mps_down = make_single_blocs_mps(lhs_indices, lhs_chi_shapes, d=1)
    mps_up = make_single_blocs_mps(lhs_indices, lhs_chi_shapes, d=1)
    from pyfhmdot.models.pymodels import hamiltonian_obc

    mpo_left = hamiltonian_obc("sh_xxz-hz_u1", {"Jxy": 0, "Jz": 0, "hz": 10}, 3)[0]
    mpo_right = hamiltonian_obc("sh_xxz-hz_u1", {"Jxy": 0, "Jz": 0, "hz": 10}, 3)[-1]
    mpo = hamiltonian_obc("sh_xxz-hz_u1", {"Jxy": 0, "Jz": 0, "hz": 10}, 3)[1]

    from pyfhmdot.intense.contract import (
        contract_mps_mpo_mps_left_border,
        contract_mps_mpo_mps_right_border,
    )

    left = {}
    contract_mps_mpo_mps_left_border(left, mps_down, mpo_left, mps_up)
    assert [len(_) for _ in left.keys()][0] == 3
    right = {}
    contract_mps_mpo_mps_right_border(right, mps_down, mpo_left, mps_up)
    assert [len(_) for _ in right.keys()][0] == 3
