import pytest


def test_apply_gate_previous_code(single_ab_before,single_tmp_theta,make_single_dummy_dgate,single_ab_after):
    from pyfhmdot.routine.interface import mm_to_theta_with_gate, theta_to_mm
    import numpy as np

    a_before, b_before = single_ab_before
    tmp_theta = single_tmp_theta
    a_after, b_after = single_ab_after
    gate = make_single_dummy_dgate()


    tmp_blocs = {}
    mm_to_theta_with_gate(
        dst_blocs=tmp_blocs,
        lhs_blocs=a_before,
        rhs_blocs=b_before,
        gate_blocs=gate,
        conserve_left_right_before=False,
        conserve_left_right_after=False,
    )
    dst_a = {}
    dst_b = {}
    theta_to_mm(
        theta_blocs=tmp_blocs,
        lhs_blocs=dst_a,
        rhs_blocs=dst_b,
        dw_dict={"dw_one_serie":0},
        chi_max=100,
        normalize=True,
        conserve_direction_left=False,
        eps=10**-10,
        is_um=True,
    )

    for key in a_after.keys():
        assert np.all(a_after[key] == dst_a[key])
    for key in b_after.keys():
        assert np.all(b_after[key] == dst_b[key])
