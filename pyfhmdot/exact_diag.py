import numpy as _np
from scipy.linalg import eigh


def outer_product(op1, op2, dest):
    pass


def merge_blocs_same_qnum(array_op, array_dest):
    pass


def eigenvalues():
    """
    eig - Find the eigenvalues and eigenvectors of a square matrix
    eigvals - Find just the eigenvalues of a square matrix
    eigh - Find the e-vals and e-vectors of a Hermitian or symmetric matrix
    eigvalsh - Find just the eigenvalues of a Hermitian or symmetric matrix
    """
    N = 100
    matrix = "blabla"
    initial_eigenvecs = "blablabla"
    eigh(
        a,
        b=None,
        lower=True,
        eigvals_only=False,
        overwrite_a=True,
        overwrite_b=True,
        turbo=True,
        check_finite=False,
        subset_by_index=[0, N],
        subset_by_value=None,
        driver="EVX",
    )
