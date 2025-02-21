from pyfhmdot.algorithm import sweep
import pytest


def test_sweeps():
    from pyfhmdot.algorithm import sweep

    for i, j in enumerate(sweep(5)):
        assert i + 1 == j

    for i, j in enumerate(sweep(5, from_site=3)):
        assert i + 2 + 1 == j

    for i, j in enumerate(sweep(5, to_site=4)):
        assert i + 1 == j
    assert j + 1 == 4

    for i, j in enumerate(sweep(5, from_site=3, to_site=4)):
        assert i + 2 + 1 == j

    assert j + 1 == 4


def test_print_single():
    from pyfhmdot.algorithm import print_single, print_double

    assert print_single(5, 2) == "\rA*BBB"
    assert print_double(5, 2) == "\rA*=BB"


@pytest.mark.parametrize("size", [10, 11])
def test_sweep_move(size):
    from pyfhmdot.algorithm import sweep_move

    assert size == size
    pass
