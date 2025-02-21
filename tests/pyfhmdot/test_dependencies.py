import pytest


@pytest.mark.skip(msg="module fhmdot not ready yet")
def test_example():
    from example import view_nocopy

    assert "import example worked!" == "import example worked!"


def test_numpy():
    import numpy

    assert "import numpy worked!" == "import numpy worked!"


def test_scipy():
    import scipy

    assert "import numpy worked!" == "import numpy worked!"


@pytest.mark.skip(msg="matplotlib is needed for visualizing benchmarks")
def test_scipy():
    import matplotlib.pyplot

    assert "import matplotlib worked!" == "import matplotlib worked!"
