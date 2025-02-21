import pytest


def test_conftest(make_test):
    assert make_test()


def test_automation_import():
    from automation import automation

    assert automation()


@pytest.mark.skip(msg="module mdot not ready yet")
def test_mdot():
    import mdot_operators

    assert True

    from automation import is_mdot_available

    assert is_mdot_available()


def test_h5py():
    import h5py

    assert True


def test_numpy():
    import numpy

    assert True


def test_scipy():
    import scipy

    assert True


@pytest.mark.skip(msg="matplotlib is needed for visualizing benchmarks")
def test_matplotlib():
    import matplotlib.pyplot

    assert True
