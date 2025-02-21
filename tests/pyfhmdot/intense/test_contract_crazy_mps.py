import pytest


def test_contract_left(make_single_blocs_mps, lhs_indices, lhs_chi_shapes):
    mps_down = make_single_blocs_mps(lhs_indices, lhs_chi_shapes, d=1)
    mps_up = make_single_blocs_mps(lhs_indices, lhs_chi_shapes, d=1)
    from pyfhmdot.models.pymodels import hamiltonian_obc

    mpo_left = hamiltonian_obc("sh_xxz-hz_u1", {"Jxy": 0, "Jz": 0, "hz": 10}, 3)[0]

    from pyfhmdot.intense.contract import contract_mps_mpo_mps_left_border

    left = {}
    contract_mps_mpo_mps_left_border(left, mps_down, mpo_left, mps_up)
    assert [len(_) for _ in left.keys()][0] == 3
    return left


def test_contract_right(make_single_blocs_mps, rhs_indices, rhs_chi_shapes):
    mps_down = make_single_blocs_mps(rhs_indices, rhs_chi_shapes, d=1)
    mps_up = make_single_blocs_mps(rhs_indices, rhs_chi_shapes, d=1)
    from pyfhmdot.models.pymodels import hamiltonian_obc

    mpo_right = hamiltonian_obc("sh_xxz-hz_u1", {"Jxy": 0, "Jz": 0, "hz": 10}, 3)[-1]

    from pyfhmdot.intense.contract import contract_mps_mpo_mps_right_border

    right = {}
    contract_mps_mpo_mps_right_border(right, mps_down, mpo_right, mps_up)
    assert [len(_) for _ in right.keys()][0] == 3
    return right


def test_contract(
    make_single_blocs_mps, lhs_indices, lhs_chi_shapes, rhs_indices, rhs_chi_shapes
):
    left = test_contract_left(make_single_blocs_mps, lhs_indices, lhs_chi_shapes)
    right = test_contract_right(make_single_blocs_mps, rhs_indices, rhs_chi_shapes)
    from pyfhmdot.models.pymodels import hamiltonian_obc

    mpo = hamiltonian_obc("sh_xxz-hz_u1", {"Jxy": 0, "Jz": 0, "hz": 10}, 3)[1]
    from pyfhmdot.intense.contract import (
        contract_right_bloc_mps,
        contract_left_bloc_mps,
    )

    next_mps_down = make_single_blocs_mps(lhs_indices, lhs_chi_shapes, d=1)
    next_mps_up = make_single_blocs_mps(lhs_indices, lhs_chi_shapes, d=1)

    dst_one = {}
    contract_right_bloc_mps(dst_one, right, next_mps_down, mpo, next_mps_up)
    assert [len(_) for _ in dst_one.keys()][0] == 3

    #
    next_mps_down = make_single_blocs_mps(rhs_indices, rhs_chi_shapes, d=1)
    next_mps_up = make_single_blocs_mps(rhs_indices, rhs_chi_shapes, d=1)
    dst_two = {}
    contract_left_bloc_mps(dst_two, left, next_mps_down, mpo, next_mps_up)
    assert [len(_) for _ in dst_two.keys()][0] == 3


def test_contract_mps_left(make_single_blocs_mps, lhs_indices, lhs_chi_shapes):
    mps_down = make_single_blocs_mps(lhs_indices, lhs_chi_shapes, d=1)
    mps_up = make_single_blocs_mps(lhs_indices, lhs_chi_shapes, d=1)

    from pyfhmdot.intense.contract import contract_mps_mps_left_border

    left = {}
    contract_mps_mps_left_border(left, mps_down, mps_up)
    assert [len(_) for _ in left.keys()][0] == 2
    return left


def test_contract_mps_right(make_single_blocs_mps, rhs_indices, rhs_chi_shapes):
    mps_down = make_single_blocs_mps(rhs_indices, rhs_chi_shapes, d=1)
    mps_up = make_single_blocs_mps(rhs_indices, rhs_chi_shapes, d=1)

    from pyfhmdot.intense.contract import contract_mps_mps_right_border

    right = {}
    contract_mps_mps_right_border(right, mps_down, mps_up)
    assert [len(_) for _ in right.keys()][0] == 2
    return right


def test_contract(
    make_single_blocs_mps, lhs_indices, lhs_chi_shapes, rhs_indices, rhs_chi_shapes
):
    left = test_contract_mps_left(make_single_blocs_mps, lhs_indices, lhs_chi_shapes)
    right = test_contract_mps_right(make_single_blocs_mps, rhs_indices, rhs_chi_shapes)
    from pyfhmdot.intense.contract import contract_left_right_small_bloc

    dst_one = {}
    contract_left_right_small_bloc(dst_one, left, right)
    assert isinstance(dst_one[()][()], float)
