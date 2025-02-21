import pytest


def test_add_dictionary(tmp_path):
    from pyfhmdot.utils.iotools import create_h5, add_dictionary, load_dictionary

    dummypath = str(tmp_path) + "/dummy.h5"
    create_h5(dummypath)
    add_dictionary(dummypath, folder="DUMMY", dictionary={"hello": 2, "world": 3.14})

    mydict = {}
    load_dictionary(dummypath, mydict, folder="DUMMY")
    assert mydict["hello"] == 2
    assert mydict["world"] == 3.14
