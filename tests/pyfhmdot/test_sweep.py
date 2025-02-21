import pytest


def test_sweeps():
    from pyfhmdot.algorithm import sweep

    for i, j in enumerate(sweep(5)):
        assert i + 1 == j
