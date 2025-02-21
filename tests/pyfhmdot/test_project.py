import pytest


def test_pretty():
    from pyfhmdot.project import Hello

    msg = Hello.pretty("visitor")
    assert msg == "hello visitor"

    new = Hello("guest")
    assert new.dummy_bye() == "hello guest and byebye"
