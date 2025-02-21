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
        apply_UM=apply_UM,
        apply_MV=apply_MV,
        apply_gate_UM=apply_UM,
        apply_gate_MV=apply_MV,
        start_odd_bonds=False,
        conserve_left_right=False,
    )
