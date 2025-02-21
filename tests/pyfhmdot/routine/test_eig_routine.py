import pytest

def test_eig_scipy_routine():
    import numpy as np
    from pyfhmdot.routine.eig_routine import smallest_eigenvectors_from_scipy
    
    a = np.random.random((2*7,2*7))

    w = smallest_eigenvectors_from_scipy(a)
    w.reshape(2,7)