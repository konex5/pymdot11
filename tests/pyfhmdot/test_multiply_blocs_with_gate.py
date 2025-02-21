from pyfhmdot.routine import mpsQ_svd_th2Um, mpsQ_svd_th2mV
import pytest


def test_multiply_blocs_dense(make_single_dense_mps):
    from pyfhmdot.routine import (
        multiply_blocs_no_gate_applied,
    )

    lhs_blocs = make_single_dense_mps(chiL=3, d=4, chiR=5)
    rhs_blocs = make_single_dense_mps(chiL=5, d=4, chiR=2)
    dest_blocs = {}
    multiply_blocs_no_gate_applied(dest_blocs, lhs_blocs, rhs_blocs)
    assert list(dest_blocs.keys())[0] == (0, 0, 0, 0)
    assert len(dest_blocs.keys()) == 1
    assert dest_blocs[(0, 0, 0, 0)].shape == (3, 4, 4, 2)


def test_multiply_blocs_dense_with_gate(make_single_dense_mps, make_single_dense_gate):
    from pyfhmdot.routine import (
        multiply_blocs_with_gate_applied,
    )

    lhs_blocs = make_single_dense_mps(chiL=3, d=4, chiR=5)
    rhs_blocs = make_single_dense_mps(chiL=5, d=4, chiR=2)
    gate_blocs = make_single_dense_gate(d=4)
    dest_blocs = {}
    multiply_blocs_with_gate_applied(dest_blocs, lhs_blocs, rhs_blocs, gate_blocs)
    assert list(dest_blocs.keys())[0] == (0, 0, 0, 0)
    assert len(dest_blocs.keys()) == 1


def test_multiply_blocs_sparse(
    make_single_blocs_mps, lhs_indices, lhs_chi_shapes, rhs_indices, rhs_chi_shapes
):
    from pyfhmdot.routine import (
        multiply_blocs_no_gate_applied,
    )

    lhs_blocs = make_single_blocs_mps(lhs_indices, lhs_chi_shapes, d=1)
    rhs_blocs = make_single_blocs_mps(rhs_indices, rhs_chi_shapes, d=1)
    dest_blocs = {}
    multiply_blocs_no_gate_applied(dest_blocs, lhs_blocs, rhs_blocs)
    assert list(dest_blocs.keys())[0] == (0, 0, 0, 0)
    assert len(dest_blocs.keys()) == 14
    assert dest_blocs[(0, 0, 0, 0)].shape == (1, 1, 1, 2)


def test_multiply_blocs_sparse_with_qcons(
    make_single_blocs_mps, lhs_indices, lhs_chi_shapes, rhs_indices, rhs_chi_shapes
):
    from pyfhmdot.routine import (
        multiply_blocs_no_gate_applied,
    )

    lhs_blocs = make_single_blocs_mps(lhs_indices, lhs_chi_shapes, d=1)
    rhs_blocs = make_single_blocs_mps(rhs_indices, rhs_chi_shapes, d=1)
    dest_blocs = {}
    multiply_blocs_no_gate_applied(
        dest_blocs, lhs_blocs, rhs_blocs, conserve_left_right=True
    )
    assert list(dest_blocs.keys())[0] == (0, 0, 0, 0)
    assert len(dest_blocs.keys()) == 3
    assert dest_blocs[(0, 0, 0, 0)].shape == (1, 1, 1, 2)


def test_multiply_blocs_sparse_with_gate_fake(
    make_single_blocs_mps,
    make_single_blocs_gate,
    lhs_indices,
    lhs_chi_shapes,
    rhs_indices,
    rhs_chi_shapes,
    gate_indices,
):
    from pyfhmdot.routine import (
        multiply_blocs_with_gate_applied,
    )

    lhs_blocs = make_single_blocs_mps(lhs_indices, lhs_chi_shapes, d=1)
    rhs_blocs = make_single_blocs_mps(rhs_indices, rhs_chi_shapes, d=1)
    gate_blocs = make_single_blocs_gate(gate_indices, d=1)
    dest_blocs = {}
    multiply_blocs_with_gate_applied(
        dest_blocs,
        lhs_blocs,
        rhs_blocs,
        gate_blocs,
        conserve_left_right_before=False,
        conserve_left_right_after=False,
    )
    assert list(dest_blocs.keys())[0] == (0, 0, 0, 0)
    assert len(dest_blocs.keys()) == 16
    return dest_blocs


def test_multiply_blocs_sparse_with_gate_fake_onedir_qnum(
    make_single_blocs_mps,
    make_single_blocs_gate,
    lhs_indices,
    lhs_chi_shapes,
    rhs_indices,
    rhs_chi_shapes,
    gate_indices,
):
    from pyfhmdot.routine import (
        multiply_blocs_with_gate_applied,
    )

    lhs_blocs = make_single_blocs_mps(lhs_indices, lhs_chi_shapes, d=1)
    rhs_blocs = make_single_blocs_mps(rhs_indices, rhs_chi_shapes, d=1)
    gate_blocs = make_single_blocs_gate(gate_indices, d=1)
    dest_blocs = {}
    multiply_blocs_with_gate_applied(
        dest_blocs,
        lhs_blocs,
        rhs_blocs,
        gate_blocs,
        conserve_left_right_before=False,
        conserve_left_right_after=True,
    )
    assert list(dest_blocs.keys())[0] == (0, 0, 0, 0)
    assert len(dest_blocs.keys()) == 3
    return dest_blocs


def test_multiply_blocs_sparse_with_gate_fake_with_qcons(
    make_single_blocs_mps,
    make_single_blocs_gate,
    lhs_indices,
    lhs_chi_shapes,
    rhs_indices,
    rhs_chi_shapes,
    gate_indices,
):
    from pyfhmdot.routine import (
        multiply_blocs_with_gate_applied,
    )

    lhs_blocs = make_single_blocs_mps(lhs_indices, lhs_chi_shapes, d=1)
    rhs_blocs = make_single_blocs_mps(rhs_indices, rhs_chi_shapes, d=1)
    gate_blocs = make_single_blocs_gate(gate_indices, d=1)
    dest_blocs = {}
    multiply_blocs_with_gate_applied(
        dest_blocs,
        lhs_blocs,
        rhs_blocs,
        gate_blocs,
        conserve_left_right_before=True,
        conserve_left_right_after=True,
    )
    assert list(dest_blocs.keys())[0] == (0, 0, 0, 0)
    assert len(dest_blocs.keys()) == 3
    return dest_blocs


def test_multiply_blocs_sparse_with_gate_real(
    make_maximal_entangled_state_u1, make_single_dummy_dgate
):
    import numpy as np
    from pyfhmdot.routine import (
        multiply_blocs_with_gate_applied,
    )

    all = make_maximal_entangled_state_u1(2, 1 / np.sqrt(2))
    lhs_blocs, rhs_blocs = all[0], all[1]

    gate_blocs = make_single_dummy_dgate()
    dest_blocs = {}
    multiply_blocs_with_gate_applied(
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
    dest_mps_left = {}
    dest_mps_right = {}
    mpsQ_svd_th2Um(
        dest_blocs,
        dest_mps_left,
        dest_mps_right,
        {
            "discarded_weights": 1e-8,
            "eps_truncation_error": 1e-8,
            "dw_Dmax": 100,
            "dw_Dmax_tot": 100,
            "normalize": True,
            "dw_one_serie": 0,
        },
    )
    assert len(dest_mps_left.keys()) == 3
    assert len(dest_mps_right.keys()) == 5
    #
    new_dest_blocs = {}
    for keys in dest_blocs.keys():
        new_dest_blocs[(keys[0], keys[1], keys[2], 2)] = dest_blocs[keys]
    dest_mps_left = {}
    dest_mps_right = {}
    mpsQ_svd_th2mV(
        new_dest_blocs,
        dest_mps_left,
        dest_mps_right,
        {
            "discarded_weights": 1e-8,
            "eps_truncation_error": 1e-8,
            "dw_Dmax": 100,
            "dw_Dmax_tot": 100,
            "normalize": True,
            "dw_one_serie": 0,
        },
    )
    assert len(dest_mps_left.keys()) == 5
    assert len(dest_mps_right.keys()) == 3


def test_multiply_blocs_sparse_with_gate_real_with_qcons(
    make_maximal_entangled_state_u1, make_single_dummy_dgate
):
    import numpy as np
    from pyfhmdot.routine import (
        multiply_blocs_with_gate_applied,
    )

    all = make_maximal_entangled_state_u1(2, 1 / np.sqrt(2))
    lhs_blocs, rhs_blocs = all[0], all[1]

    gate_blocs = make_single_dummy_dgate()
    dest_blocs = {}
    multiply_blocs_with_gate_applied(
        dest_blocs,
        lhs_blocs,
        rhs_blocs,
        gate_blocs,
        conserve_left_right_before=False,
        conserve_left_right_after=True,
    )
    assert list(dest_blocs.keys())[0] == (0, 0, 0, 0)
    assert len(dest_blocs.keys()) == 1
