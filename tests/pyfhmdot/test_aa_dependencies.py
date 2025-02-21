import pytest


def test_conftest(make_test):
    make_test()


def test_automation_import():
    from automation import automation

    automation()


@pytest.mark.skip(msg="module fhmdot not ready yet")
def test_fhmdot():
    import fmd_operators

    assert True


def test_fhmdot():
    import h5py

    assert True


def test_numpy():
    import numpy

    assert True


def test_scipy():
    import scipy

    assert True


@pytest.mark.skip(msg="matplotlib is needed for visualizing benchmarks")
def test_scipy():
    import matplotlib.pyplot

    assert True
