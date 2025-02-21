import pytest

from pyfhmdot.algorithm import sweep_and_apply, apply_UM, apply_MV


def test_sweep_and_no_apply(make_maximal_entangled_state_u1):
    size = 7
    mps = make_maximal_entangled_state_u1(size)

    sweep_and_apply(
        size=size,
        start_position=1,
        end_position=size,
        mps=mps,
        gate=[None] * size,
        apply_UM=apply_UM,
        apply_MV=apply_MV,
        apply_gate_UM=apply_UM,
        apply_gate_MV=apply_MV,
        start_odd_bonds=False,
        conserve_left_right=False,
        simdict={
            "discarded_weights": 1e-8,
            "eps_truncation_error": 1e-8,
            "dw_Dmax": 100,
            "dw_Dmax_tot": 100,
            "normalize": True,
            "dw_one_serie": 0,
        },
    )
    assert mps[0][(0, 0, 0)][0, 0, 0] == -1
    assert mps[0][(0, 1, 1)][0, 0, 0] == -1

    sweep_and_apply(
        size=size,
        start_position=size,
        end_position=1,
        mps=mps,
        gate=[None] * size,
        apply_UM=apply_UM,
        apply_MV=apply_MV,
        apply_gate_UM=apply_UM,
        apply_gate_MV=apply_MV,
        start_odd_bonds=True,
        conserve_left_right=True,
        simdict={
            "discarded_weights": 1e-8,
            "eps_truncation_error": 1e-8,
            "dw_Dmax": 100,
            "dw_Dmax_tot": 100,
            "normalize": True,
            "dw_one_serie": 0,
        },
    )
    pass


def test_sweep_and_apply(make_maximal_entangled_state_u1):
    size = 7
    mps = make_maximal_entangled_state_u1(size)

    sweep_and_apply(
        size=size,
        start_position=1,
        end_position=size,
        mps=mps,
        gate=[None] * size,
        apply_UM=apply_UM,
        apply_MV=apply_MV,
        apply_gate_UM=apply_UM,
        apply_gate_MV=apply_MV,
        start_odd_bonds=False,
        conserve_left_right=False,
        simdict={
            "discarded_weights": 1e-8,
            "eps_truncation_error": 1e-8,
            "dw_Dmax": 100,
            "dw_Dmax_tot": 100,
            "normalize": True,
            "dw_one_serie": 0,
        },
    )
