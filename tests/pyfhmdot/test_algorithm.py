import pytest


def test_should_apply_gate():
    from pyfhmdot.algorithm import should_apply_gate

    L = 11
    layer = 0
    assert not should_apply_gate(L, layer, 4, start_left=True, start_odd_bonds=True)
    assert should_apply_gate(L, layer, 5, start_left=True, start_odd_bonds=True)
    assert should_apply_gate(L, layer, 4, start_left=True, start_odd_bonds=False)
    assert not should_apply_gate(L, layer, 5, start_left=True, start_odd_bonds=False)

    L = 11
    layer = 1
    assert not should_apply_gate(L, 0, 10, start_left=True, start_odd_bonds=True)
    # assert should_apply_gate(L,layer,10,start_left=False,start_odd_bonds=True)
    # assert not should_apply_gate(L,layer,9,start_left=False,start_odd_bonds=True)
    # assert should_apply_gate(L,layer,4,start_left=False,start_odd_bonds=True)
    # assert not should_apply_gate(L,layer,5,start_left=False,start_odd_bonds=True)
    # assert not should_apply_gate(L,layer,4,start_left=False,start_odd_bonds=False)
    # assert should_apply_gate(L,layer,5,start_left=False,start_odd_bonds=False)
