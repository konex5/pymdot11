import pytest


@pytest.fixture
def make_test():
    def _make_test():
        assert True

    return _make_test


@pytest.fixture
def lhs_indices():
    return [
        (0, 0, 0),
        (0, 1, 0),
        (1, 1, 3),
        (0, 0, 1),
        (0, 1, 1),
        (1, 0, 2),
        (1, 0, 3),
    ]


@pytest.fixture
def rhs_indices():
    return [
        (0, 0, 0),
        (0, 1, 0),
        (2, 1, 0),
        (0, 0, 1),
        (0, 1, 1),
        (1, 0, 2),
        (2, 0, 3),
        (1, 0, 4),
        (1, 0, 1),
        (1, 1, 1),
    ]


def theta_indices():
    return [
        (0, 0, 0, 0),
        (0, 0, 1, 1),
        (1, 1, 1, 1),
        (0, 1, 0, 1),
        (0, 1, 1, 0),
        (1, 0, 1, 0),
    ]

@pytest.fixture
def gate_indices():
    return theta_indices()


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

    def _make_single_dense_mpo(chiL=1, d=2, chiR=1, isreal=True):
        if isreal:
            mpo = np.random.random(chiL * d * d * chiR)
        else:
            mpo = (
                np.random.random(chiL * d * d * chiR)
                + np.random.random(chiL * d * d * chiR) * 1j
            )
        mpo_out = mpo.reshape(chiL, d, d, chiR) / np.sum(mpo ** 2)
        return {(0, 0, 0, 0): mpo_out}

    return _make_single_dense_mpo


@pytest.fixture
def make_single_dense_gate():
    import numpy as np

    def _make_single_dense_gate(d=2, isreal=True):
        if isreal:
            gate = np.random.random(d * d * d * d)
        else:
            gate = (
                np.random.random(d * d * d * d) + np.random.random(d * d * d * d) * 1j
            )
        gate_out = gate.reshape(d, d, d, d) / np.sum(gate ** 2)
        return {(0, 0, 0, 0): gate_out}

    return _make_single_dense_gate


def mps(make_mps):
    return make_mps()
