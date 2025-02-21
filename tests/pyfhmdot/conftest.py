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


@pytest.fixture
def lhs_chi_shapes():
    return [(1, 1), (1, 1), (3, 4), (1, 2), (1, 2), (3, 5), (3, 4)]


@pytest.fixture
def rhs_chi_shapes():
    return [
        (1, 2),
        (1, 2),
        (5, 2),
        (1, 3),
        (1, 3),
        (2, 4),
        (5, 6),
        (2, 8),
        (2, 3),
        (2, 3),
    ]


@pytest.fixture
def gate_indices():
    return [
        (0, 0, 0, 0),
        (0, 0, 1, 1),
        (1, 1, 1, 1),
        (0, 1, 0, 1),
        (0, 1, 1, 0),
        (1, 0, 1, 0),
    ]


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
def make_single_blocs_mps():
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

        return mps_out

    def _make_single_blocs_mps(indices, chi_shapes, d=2, isreal=True):
        blocs_out = {}
        for i in range(len(indices)):
            blocs_out[indices[i]] = _make_single_dense_mps(
                chi_shapes[i][0], d, chi_shapes[i][-1], isreal
            )
        return blocs_out

    return _make_single_blocs_mps


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


@pytest.fixture
def make_single_blocs_gate():
    import numpy as np

    def _make_single_dense_gate(d=1, isreal=True):
        if isreal:
            gate = np.random.random(d * d * d * d)
        else:
            gate = (
                np.random.random(d * d * d * d) + np.random.random(d * d * d * d) * 1j
            )
        gate_out = gate.reshape(d, d, d, d) / np.sum(gate ** 2)
        return gate_out

    def _make_single_blocs_gate(gate_indices, d=1, isreal=True):
        blocs_out = {}
        for i in range(len(gate_indices)):
            blocs_out[gate_indices[i]] = _make_single_dense_gate(d, isreal)
        return blocs_out

    return _make_single_blocs_gate


@pytest.fixture
def make_maximal_entangled_state_u1():
    def _make_maximal_entangled_state_u1(L, local_coef=1.0 / 2.0):
        import numpy as np
        dmps = []
        for l in range(L):
            dest_blocs = {}
            if l == L-1:
                dest_blocs[(0, 1, 2*L)] = np.array([1/np.sqrt(2),1/np.sqrt(2)]).reshape(1, 2, 1)
            else:
                dest_blocs[(0, 1, 0)] = np.array([1/np.sqrt(2),1/np.sqrt(2)]).reshape(1, 2, 1)
            dmps.append(dest_blocs)

        return dmps

    return _make_maximal_entangled_state_u1

@pytest.fixture
def make_single_dummy_dgate():
    def _make_single_dummy_dgate():
        import numpy as np
        dgate = {}
        dgate[(0,0,0,0)] = np.array([0.994832]).reshape(1,1,1,1).transpose(0,1,3,2)
        dgate[(0,0,1,1)] = np.array([0.992262, 0, 0, 1.00781]).reshape(1,1,2,2).transpose(0,1,3,2)
        dgate[(0,1,1,0)] = np.array([ -0.00257052, 0, 0, -0.00261078]).reshape(1,2,1,2).transpose(0,1,3,2)
        dgate[(0,1,2,1)] = np.array([0,-0.00260404,-0.00260404,0]).reshape(1,2,2,1).transpose(0,1,3,2)
        dgate[(0,2,2,0)] = np.array([6.74592e-06]).reshape(1,1,1,1).transpose(0,1,3,2)
        dgate[(1,0,0,1)] = np.array([-0.00257052,0,0,-0.00261078]).reshape(2,1,2,1).transpose(0,1,3,2)
        dgate[(1,0,1,2)] = np.array([0, -0.00260404,-0.00260404, 0]).reshape(2,1,1,2).transpose(0,1,3,2)
        dgate[(1,1,0,0)] = np.array([0.992262,0,0,1.00781]).reshape(2,2,1,1).transpose(0,1,3,2)
        dgate[(1,1,1,1)] = np.array([0.979489, 0,0, 1.0052,0, 6.74592e-06,0, 0,0, 0,6.74592e-06, 0,1.0052, 0, 0, 1.01042]).reshape(2,2,2,2).transpose(0,1,3,2)
        dgate[(1,1,2,2)] = np.array([0.992262,0,0,1.00781]).reshape(2,2,1,1).transpose(0,1,3,2)
        dgate[(1,2,1,0)] = np.array([0, -0.00260404,0, -0.00260404]).reshape(2,1,1,2).transpose(0,1,3,2)
        dgate[(1,2,2,1)] = np.array([-0.00257052,0,0,-0.00261078]).reshape(2,1,2,1).transpose(0,1,3,2)
        dgate[(2,0,0,2)] = np.array([6.74592e-06]).reshape(1,1,1,1).transpose(0,1,3,2)
        dgate[(2,1,0,1)] = np.array([0, -0.00260404,-0.00260404,0]).reshape(1,2,2,1).transpose(0,1,3,2)
        dgate[(2,1,1,2)] = np.array([-0.00257052, 0,0, -0.00261078]).reshape(1,2,1,2).transpose(0,1,3,2)
        dgate[(2,2,0,0)] = np.array([1.0052]).reshape(1,1,1,1).transpose(0,1,3,2)
        dgate[(2,2,1,1)] = np.array([0.992262, 0,0, 1.00781]).reshape(1,1,2,2).transpose(0,1,3,2)
        dgate[(2,2,2,2)] = np.array([0.994832]).reshape(1,1,1,1).transpose(0,1,3,2)
        return dgate
    return _make_single_dummy_dgate



def mps(make_mps):
    return make_mps()
