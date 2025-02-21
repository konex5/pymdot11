import pytest


@pytest.fixture
def make_test():
    def _make_test():
        assert True

    return _make_test


@pytest.fixture
def make_single_dense_mps():
    import numpy as np

    def _make_single_dense_mps(chiL=13, d=2, chiR=13, isreal=True):
        if isreal:
            mps = np.random.random(chiL * d * chiR)
        else:
            mps = (
                np.random.random(chiL * d * chiR)
                + np.random.random(chiL * d * chiR) * 1j
            )
        mps_out = mps.reshape(chiL, d, chiR) / np.sum(mps ** 2)
        return {(0, 0, 0): mps_out}

    return _make_single_dense_mps


@pytest.fixture
def make_single_dense_mpo():
    import numpy as np

    def _make_single_dense_mpo(chi=1, d=2, isreal=True):
        if isreal:
            mpo = np.random.random.rand(chi * d * d * chi, dtype="float64")
        else:
            mpo = np.random.random.rand(chi * d * d * chi, dtype="complex128")
        mpo_out = mpo.reshape(chi, d, d, chi) / np.sum(mpo ** 2)
        return {(0, 0, 0, 0): mpo_out}

    return _make_single_dense_mpo


def mps(make_mps):
    return make_mps()
