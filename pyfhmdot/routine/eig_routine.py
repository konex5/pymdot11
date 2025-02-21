import numpy as _np
from scipy.linalg import eigh as _eigh
from typing import Dict as _Dict


def minimize_theta_with_scipy(
    env_blocs: _Dict[tuple, _np.ndarray],
    eigenvalues: _Dict[tuple, float],
    eigenvectors: _Dict[tuple, _np.ndarray],
    chi_max: int,
) -> None:
    for keys in env_blocs.keys():
        mat = env_blocs[keys][:chi_max, :, :, :chi_max, :chi_max, :, :, :chi_max]
        new_shape = (
            mat.shape[0] * mat.shape[1] * mat.shape[2] * mat.shape[3],
            mat.shape[4] * mat.shape[5] * mat.shape[6] * mat.shape[7],
        )
        E, vec = _eigh(mat.reshape(new_shape), subset_by_index=[0, 0])
        eigenvalues[(keys[0], keys[1], keys[2], keys[3])] = E[0]
        eigenvectors[(keys[0], keys[1], keys[2], keys[3])] = vec.reshape(
            (mat.shape[0], mat.shape[1], mat.shape[2], mat.shape[3])
        )
