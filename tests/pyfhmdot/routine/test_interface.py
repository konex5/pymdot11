import pytest

@pytest.mark.skip(msg="theta matrix was with wrong indices")
def test_multiply_blocs_sparse_with_gate_real(
    make_maximal_entangled_state_u1, make_single_dummy_dgate
):
    import numpy as np
    from pyfhmdot.routine.interface import (
        mm_to_theta_with_gate,
    )

    all = make_maximal_entangled_state_u1(2, 1 / np.sqrt(2))
    lhs_blocs, rhs_blocs = all[0], all[1]

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
        conserve_direction_left=True,
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
        conserve_direction_left=False,
        is_um=False,
    )
    assert len(dest_mps_left.keys()) == 5
    assert len(dest_mps_right.keys()) == 3
