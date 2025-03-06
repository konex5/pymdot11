import pytest


@pytest.mark.skip
def test_should_apply():
    from pymdot.algorithm import should_apply_gate

    # odd size
    assert should_apply_gate(position=0, start_odd_bonds=True)
    assert not should_apply_gate(position=1, start_odd_bonds=True)
    assert should_apply_gate(position=2, start_odd_bonds=True)
    assert not should_apply_gate(position=3, start_odd_bonds=True)

    assert not should_apply_gate(position=0, start_odd_bonds=False)
    assert should_apply_gate(position=1, start_odd_bonds=False)
    assert not should_apply_gate(position=2, start_odd_bonds=False)
    assert should_apply_gate(position=3, start_odd_bonds=False)

    # even size
    assert should_apply_gate(position=0, start_odd_bonds=True)
    assert not should_apply_gate(position=1, start_odd_bonds=True)
    assert should_apply_gate(position=2, start_odd_bonds=True)

    assert not should_apply_gate(position=0, start_odd_bonds=False)
    assert should_apply_gate(position=1, start_odd_bonds=False)
    assert not should_apply_gate(position=2, start_odd_bonds=False)


@pytest.mark.skip
def test_sweep_and_apply(make_maximal_entangled_state_u1):
    from pymdot.algorithm import sweep_and_apply, apply_UM, apply_MV

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
