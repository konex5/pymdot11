import pytest


def test_create_id_mp():
    from pyfhmdot.create import create_id_mp

    _, a = create_id_mp("sh_id_no", 1, True)
    _, b = create_id_mp("sh_id_u1", 1, True)
    assert a[(0, 0, 0)][0, 0, 0] == b[(0, 0, 0)][0, 0, 0]
    assert a[(0, 0, 0)][0, 1, 1] == b[(0, 1, 1)][0, 0, 0]
    #
    _, a = create_id_mp("sh_id_no", 1, False)
    _, b = create_id_mp("sh_id_u1", 1, False)
    assert a[(0, 0, 0)][0, 0, 0] == b[(0, 0, 0)][0, 0, 0]
    assert a[(0, 0, 0)][1, 1, 0] == b[(1, 1, 0)][0, 0, 0]
    #
    _, a = create_id_mp("sh_id_no", 2, True)
    _, b = create_id_mp("sh_id_u1", 2, True)
    assert a[(0, 0, 0)][0, 1, 1] == b[(0, 1, 1)][0, 0, 0]
    #
    #
    _, a = create_id_mp("sh_id_no", 2, False)
    _, b = create_id_mp("sh_id_u1", 2, False)
    assert a[(0, 0, 0)][1, 0, 1] == b[(1, 0, 1)][0, 0, 0]
