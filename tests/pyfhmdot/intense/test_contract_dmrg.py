import pytest


def test_contract_dmrg(make_single_blocs_mps):
    from pyfhmdot.initialize import create_infinite_hamiltonian

    mpo_left, mpo, mpo_right = create_infinite_hamiltonian(
        "sh_xxz-hz_u1", {"Jxy": 1, "Jz": 2, "hz": 3}
    )
    mps_left = make_single_blocs_mps(
        [(0, 0, 0), (0, 1, 1), (0, 0, 1), (0, 1, 0)],
        [(1, 1), (1, 3), (1, 3), (1, 1)],
        d=1,
    )
    mps_left_two = make_single_blocs_mps(
        [(0, 0, 0), (0, 1, 2), (0, 1, 3), (0, 1, 0)],
        [(1, 2), (1, 3), (1, 4), (1, 2)],
        d=1,
    )
    mps_right = make_single_blocs_mps(
        [(0, 0, 0), (1, 1, 0), (1, 0, 0), (0, 1, 0)],
        [(1, 1), (3, 1), (3, 1), (1, 1)],
        d=1,
    )
    mps_right_two = make_single_blocs_mps(
        [(0, 0, 0), (2, 1, 0), (3, 1, 0), (0, 1, 0)],
        [(2, 1), (3, 1), (4, 1), (2, 1)],
        d=1,
    )

    from pyfhmdot.intense.contract import (
        contract_left_right_bloc_with_mpo,
        contract_mps_mpo_mps_left_border,
        contract_mps_mpo_mps_right_border,
        contract_left_bloc_mps,
        contract_right_bloc_mps,
        contract_left_right_mpo_mpo_permute,
    )

    left = {}
    contract_mps_mpo_mps_left_border(left, mps_left, mpo_left, mps_left)
    new_left = {}
    contract_left_bloc_mps(new_left, left, mps_left_two, mpo[0], mps_left_two)

    right = {}
    contract_mps_mpo_mps_right_border(right, mps_right, mpo_right, mps_right)
    new_right = {}
    contract_right_bloc_mps(new_right, right, mps_right_two, mpo[0], mps_right_two)
    env_bloc = {}
    contract_left_right_mpo_mpo_permute(env_bloc, new_left, mpo[0], mpo[1], new_right)

    from pyfhmdot.routine.interface import minimize_theta

    eigval = {}
    eigvec = {}
    # minimize_theta(env_bloc,eigval,eigvec,10)
    pass
