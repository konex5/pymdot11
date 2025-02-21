import pytest

@pytest.mark.skip
def test_initialize_even_size():
    from pyfhmdot.initialize import initialize_idmrg_even_size, initialize_idmrg_odd_size
    from pyfhmdot.initialize import create_infinite_hamiltonian

    ham_left, ham_middle, ham_right = create_infinite_hamiltonian(
        "sh_xxz-hz_u1", {"Jxy": 1, "Jz": 1, "hz": 0}
    )

    dst_left_bloc = {}
    imps_left = {}
    dst_right_bloc = {}
    imps_right = {}

    initialize_idmrg_even_size(
        dst_left_bloc,
        imps_left,
        dst_right_bloc,
        imps_right,
        ham_left,
        ham_right,
        position=1,
        size=10,
        conserve_total=5,
        d=2,
    )
    assert sorted(imps_left.keys()) == [(0,0,0),(0,1,1)]
    assert sorted(imps_right.keys()) == [(4,1,5),(5,0,5)]

    dst_left_bloc = {}
    imps_left = {}
    dst_right_bloc = {}
    imps_right = {}
    imps_middle = {}

    initialize_idmrg_odd_size(dst_left_bloc,
    imps_left,
    dst_right_bloc,
    imps_right,
    imps_middle,
    ham_left,
    ham_middle[0],
    ham_right,
    position=1,
    size=10,
    conserve_total=5,
    d=2,
    )

    pass
