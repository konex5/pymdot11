from scipy.linalg import eigh as _eigh


def smallest_eigenvectors_from_scipy(A):
    E, v = _eigh(A, subset_by_index=[0, 0])
    print("Lowest energy is :", E)
    return E, v
