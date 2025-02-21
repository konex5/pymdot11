import pytest

def test_hamiltonian_read_line():
    from pyfhmdot.models.parser import read_parameters
    name, value=read_parameters("Jz=2.57")
    assert name=="Jz" and value==2.57
    name, value=read_parameters("J_EXP=2,1")
    assert name=="J_EXP" and value==(2,1)
    name, value=read_parameters("J_LIST=2,1,5,6")
    assert name=="J_LIST" and isinstance(value,list) and value[-1] == 6
    
    