import pytest


def test_hamiltonian_obc():
    from pyfhmdot.models.pymodels import hamiltonian_obc
    from pyfhmdot.intense.mul_mp import multiply_mp

    ham = hamiltonian_obc("sh_hz_u1", {"hz": 7.0}, 2)
    assert ham[0][(0, 1, 1, 0)][0, 0, 0, 0] == 7
    assert ham[1][(0, 1, 1, 0)][0, 0, 0, 0] == 1
    assert ham[0][(0, 1, 1, 1)][0, 0, 0, 0] == 1
    assert ham[1][(1, 1, 1, 0)][0, 0, 0, 0] == 7

    dst = {}
    multiply_mp(dst, ham[0], ham[1], [3], [0])
    assert dst[(0, 0, 0, 0, 0, 0)][0, 0, 0, 0, 0, 0] == -14
    dst.clear()

    ham = hamiltonian_obc("sh_hz_u1", {"hz": 7.0}, 3)
    assert ham[1][(0, 1, 1, 0)][0, 0, 0, 0] == 1
    assert ham[1][(1, 1, 1, 1)][0, 0, 0, 0] == 1
    # assert ham[0][(1,1,1,0)][0,0,0,0] == 3.5
    tmp = {}
    multiply_mp(tmp, ham[0], ham[1], [3], [0])

    dst = {}
    multiply_mp(dst, tmp, ham[2], [5], [0])
    assert dst[(0, 0, 0, 0, 0, 0, 0, 0)][0, 0, 0, 0, 0, 0, 0, 0] == -21
    dst.clear()

    ham = hamiltonian_obc("sh_xy_u1", {"Jxy": 200}, 2)
    assert ham[0][(0, 0, 1, 1)][0, 0, 0, 0] == 20

    dst = {}
    multiply_mp(dst, ham[0], ham[1], [3], [0])
    assert (
        dst[(0, 0, 1, 1, 0, 0)][0, 0, 0, 0, 0, 0] == 400
    )  # if non pauli it would be 100!
    dst.clear()

    ham = hamiltonian_obc("sh_xy_u1", {"Jxy": 200}, 3)

    tmp = {}
    multiply_mp(tmp, ham[0], ham[1], [3], [0])

    dst = {}
    multiply_mp(dst, tmp, ham[2], [5], [0])
    assert dst[(0, 0, 0, 0, 1, 0, 1, 0)][0, 0, 0, 0, 0, 0, 0, 0] == 400
    dst.clear()

    # submodel
    ham = hamiltonian_obc("sh_xxz-hz_u1", {"Jxy": 0, "Jz": 0, "hz": 7.0}, 2)
    assert ham[0][(0, 1, 1, 0)][0, 0, 0, 0] == 7
    assert ham[1][(0, 1, 1, 0)][0, 0, 0, 0] == 1
    assert ham[0][(0, 1, 1, 4)][0, 0, 0, 0] == 1
    assert ham[1][(4, 1, 1, 0)][0, 0, 0, 0] == 7

    dst = {}
    multiply_mp(dst, ham[0], ham[1], [3], [0])
    assert dst[(0, 0, 0, 0, 0, 0)][0, 0, 0, 0, 0, 0] == -14
    dst.clear()
