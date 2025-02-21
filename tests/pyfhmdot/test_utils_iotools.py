import pytest


def test_add_dictionary(tmp_path, make_single_blocs_mps):
    from pyfhmdot.utils.iotools import (
        create_h5,
        add_dictionary,
        load_dictionary,
        add_single_mp,
        load_single_mp,
    )

    dummypath = str(tmp_path) + "/dummy.h5"
    create_h5(dummypath)
    add_dictionary(dummypath, folder="DUMMY", dictionary={"hello": 2, "world": 3.14})

    mydict = {}
    load_dictionary(dummypath, mydict, folder="DUMMY")
    assert mydict["hello"] == 2
    assert mydict["world"] == 3.14

    real_mps = make_single_blocs_mps(
        [(0, 0, 0), (2, 0, 1), (1, 1, 3)], [(3, 3), (4, 4), (5, 5)], d=2, isreal=True
    )
    add_single_mp(dummypath, real_mps, site=2)
    output_dict = {}
    load_single_mp(dummypath, output_dict, site=2)
    assert real_mps[(2, 0, 1)][1, 1, 0] == output_dict[(2, 0, 1)][1, 1, 0]
    #
    imag_mps = make_single_blocs_mps(
        [(0, 0, 0), (2, 0, 1), (1, 1, 3)], [(3, 3), (4, 4), (5, 5)], d=2, isreal=False
    )
    add_single_mp(dummypath, imag_mps, site=4)
    output_dict = {}
    load_single_mp(dummypath, output_dict, site=4)
    assert imag_mps[(1, 1, 3)][1, 1, 0] == output_dict[(1, 1, 3)][1, 1, 0].conj().conj()
