import pytest


def test_multiply_blocs_sparse_with_gate_real(
    make_maximal_entangled_state_u1, make_single_dummy_dgate
):
    import numpy as np
    from pyfhmdot.routine.interface import (
        mm_to_theta_with_gate,
    )

    lhs_blocs = {
        (0, 0, 0): np.array([1]).reshape(1, 1, 1),
        (0, 2, 0): np.array([1]).reshape(1, 1, 1),
    }
    rhs_blocs = {
        (0, 0, 0): np.array([1]).reshape(1, 1, 1),
        (0, 2, 0): np.array([1]).reshape(1, 1, 1),
    }

    gate_blocs = make_single_dummy_dgate()
    dest_blocs = {}
    mm_to_theta_with_gate(
        dest_blocs,
        lhs_blocs,
        rhs_blocs,
        gate_blocs,
        conserve_left_right_before=False,
        conserve_left_right_after=False,
    )
    assert list(dest_blocs.keys())[0] == (0, 0, 0, 0)
    assert len(dest_blocs.keys()) == 5
    #
    from pyfhmdot.routine.interface import theta_to_mm

    dest_mps_left = {}
    dest_mps_right = {}
    theta_to_mm(
        dest_blocs,
        dest_mps_left,
        dest_mps_right,
        chi_max=100,
        normalize=True,
        dw_dict={
            "dw_total": 0,
            "dw_one_serie": 0,
        },
        direction_right=2,
        is_um=True,
    )
    assert len(dest_mps_left.keys()) == 3
    assert len(dest_mps_right.keys()) == 5
    #
    new_dest_blocs = {}
    for keys in dest_blocs.keys():
        new_dest_blocs[(keys[0], keys[1], keys[2], 2)] = dest_blocs[keys]
    dest_mps_left = {}
    dest_mps_right = {}
    theta_to_mm(
        new_dest_blocs,
        dest_mps_left,
        dest_mps_right,
        chi_max=100,
        normalize=True,
        dw_dict={
            "dw_total": 0,
            "dw_one_serie": 0,
        },
        direction_right=-1,
        is_um=False,
    )
    assert len(dest_mps_left.keys()) == 5
    assert len(dest_mps_right.keys()) == 3


def test_routine_interface_minimize_theta():
    from pyfhmdot.initialize import create_infinite_hamiltonian
    from pyfhmdot.initialize import initialize_idmrg_even_size
    from pyfhmdot.intense.contract import contract_left_right_mpo_mpo_permute
    from pyfhmdot.routine.eig_routine import minimize_theta_with_scipy as minimize_theta

    ham = create_infinite_hamiltonian("sh_xxz-hz_u1", {"Jxy": 0, "Jz": 0, "hz": -6})
    mp_left = {}
    mp_right = {}
    left = {}
    right = {}
    initialize_idmrg_even_size(
        left,
        mp_left,
        right,
        mp_right,
        ham[0],
        ham[-1],
        position=2,
        size=4,
        conserve_total=0,
        d=2,
    )
    env_bloc = {}
    contract_left_right_mpo_mpo_permute(env_bloc, left, ham[1][0], ham[1][1], right)
    eigvals = {}
    eigvecs = {}
    minimize_theta(env_bloc, eigvals, eigvecs, 10)
    assert eigvecs[(0, 0, 0, 0)][0, 0, 0, 0] == 1
