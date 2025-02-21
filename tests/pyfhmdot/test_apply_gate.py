import pytest

def test_valid_gate(make_single_dummy_dgate):
    from pyfhmdot.general import create_hamiltonian_gates
    import numpy as np
    valid_gate = make_single_dummy_dgate()
    gate=create_hamiltonian_gates("sh_xxz-hz_u1",{"Jxy":1/4.,"Jz":2./4.,"hz":3./2.},3,dbeta=0.025,is_dgate=True,in_group=True)[0][0]
    # up and down are inverted.. !!
    for key in valid_gate.keys():
        assert np.all(np.abs(valid_gate[key] - gate[key]) < 1e-8)


def test_apply_gate_previous_code(
    single_ab_before, single_tmp_theta, make_single_dummy_dgate, single_ab_after
):
    from pyfhmdot.routine.interface import (
        mm_to_theta_with_gate,
        theta_to_mm,
        mm_to_theta_with_gate_to_delete_at_some_point,
    )
    import numpy as np

    a_before, b_before = single_ab_before
    tmp_theta = single_tmp_theta
    a_after, b_after = single_ab_after
    gate = make_single_dummy_dgate()

    tmp_blocs = {}
    mm_to_theta_with_gate_to_delete_at_some_point(
        dst_blocs=tmp_blocs,
        lhs_blocs=a_before,
        rhs_blocs=b_before,
        gate_blocs=gate,
        conserve_left_right_before=False,
        conserve_left_right_after=False,
    )
    for key in tmp_theta.keys():
        assert np.all(np.abs(tmp_theta[key] - tmp_blocs[key]) < 1e-8)

    dst_a = {}
    dst_b = {}
    theta_to_mm(
        theta_blocs=tmp_blocs,
        lhs_blocs=dst_a,
        rhs_blocs=dst_b,
        dw_dict={"dw_one_serie": 0},
        chi_max=100,
        normalize=True,
        conserve_direction_left=True,
        eps=10 ** -10,
        is_um=True,
    )

    for key in a_after.keys():
        assert np.all(np.abs(a_after[key] - dst_a[key]) < 1e-8)
    for key in b_after.keys():
        assert np.all(np.abs(b_after[key] - dst_b[key]) < 1e-8)
