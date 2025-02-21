import pytest


def test_measure(make_maximal_entangled_state_u1):
    import numpy as _np

    mps_down = make_maximal_entangled_state_u1(10)
    mps_up = make_maximal_entangled_state_u1(10)

    from pyfhmdot.intense.interface import measure_mps_mps

    val = measure_mps_mps(mps_up, mps_down)
    assert _np.abs(val - 1) < 1e-8
    val = measure_mps_mps(mps_up, mps_down, position=3)
    assert _np.abs(val - 1) < 1e-8
    val = measure_mps_mps(mps_up, mps_down, position=7)
    assert _np.abs(val - 1) < 1e-8
