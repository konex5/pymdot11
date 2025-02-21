import pytest


def test_measure_dmps():
    from pyfhmdot.initialize import create_maximal_entangled_state
    from pyfhmdot.intense.interface import measure_dmps, measure_dmps_dmps
    import numpy as _np

    _, dmps = create_maximal_entangled_state(11, "sh_xxz_u1")
    for l in range(-1, len(dmps) - 1):
        val = measure_dmps(dmps, l)
        assert _np.abs(val - _np.sqrt(2) ** 11) < 1e-8
        val = measure_dmps_dmps(dmps, dmps, l)
        assert _np.abs(val - 1) < 1e-8


def test_measure_dmps_dmps(make_maximal_entangled_state_u1):
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
