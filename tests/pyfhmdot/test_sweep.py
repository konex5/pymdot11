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
