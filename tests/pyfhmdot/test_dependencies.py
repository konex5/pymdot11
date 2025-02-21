import pytest


def test_example():
    from example import view_nocopy

    assert "import example worked!" == "import example worked!"


def test_numpy():
    import numpy

    assert "import numpy worked!" == "import numpy worked!"


def test_scipy():
    import scipy

    assert "import numpy worked!" == "import numpy worked!"
