"""initialize.py"""

from copy import deepcopy as _copy
from numpy import sqrt as _sqrt
from numpy import iscomplex as _iscomplex
from numpy import imag as _imag
from sys import exit as _exit
from pymdot.dmrg_contraction import (
    create_env_blocs,
    create_three_sites_env_blocs,
    create_two_sites_env_blocs,
    select_quantum_sector,
)

from pymdot.models.pymodels import suzu_trotter_obc_exp
from pymdot.models.pymodels import hamiltonian_obc
from pymdot.models.pyoperators import single_operator
from pymdot.conservation import conserve_qnum
from pymdot.routine.indices import internal_qn_sum, internal_qn_sub

from pymdot.intense.contract import (
    contract_left_bloc_mps,
    contract_left_bloc_mps_mpo,
    contract_left_right_mpo_mpo_permute,
    contract_mps_mpo_mpo_mps_left_border,
    contract_mps_mpo_mpo_mps_right_border,
    contract_mps_mpo_mps_left_border,
    contract_mps_mpo_mps_right_border,
    contract_right_bloc_mps,
    contract_right_bloc_mps_mpo,
    filter_left_right,
)

from pymdot.routine.eig_routine import minimize_theta_with_scipy as minimize_theta
from pymdot.routine.eig_routine import apply_eigenvalues
from pymdot.routine.interface import theta_to_mm
from pymdot.routine.minimize import minimize_on_mm


def create_infinite_hamiltonian(model_name, parameters):
    """
    qnmodel='sh_xxz-hz_no' or 'ru_ldxxz-hz_u1'
    """
    ham = hamiltonian_obc(model_name, parameters, 4)
    return ham[0], (ham[1], ham[2]), ham[3]


def create_hamiltonian(model_name, parameters, size):
    """
    qnmodel='sh_xxz-hz_no' or 'ru_ldxxz-hz_u1'
    """
    return hamiltonian_obc(model_name, parameters, size)


def create_hamiltonian_gates(
    model_name, parameters, size, *, dbeta, is_dgate, in_group
):
    """
    To avoid problems, only the physical direction
    e^-{i dbeta H} or e^{- dbeta H} will be selected.
    Negative values are rejected.
    """
    if _iscomplex(dbeta):
        db = abs(_imag(dbeta)) * 1j
    else:
        db = abs(dbeta)

    # suzuki trotter
    factor1 = 1.0 / ((4.0 - 4 ** (1.0 / 3.0)))
    factor2 = 1.0 - 4.0 * factor1
    print(
        "4th order suzuki trotter... can take some time!\n"
        "(automatisation prefered than performance at this level ;-) )\n"
        "(take it easy, go and drink a coffee! =D)\n"
    )

    dgate_imaginary_time = []
    mdb = -db
    db1F = mdb * factor1 / 2.0
    db1S = mdb * factor1
    db2F = mdb * (factor1 + factor2) / 2.0
    db2S = mdb * factor2
    print("dgate suzuki_trotter 4th order, serie 1/4")
    dgate_imaginary_time.append(
        suzu_trotter_obc_exp(
            db1F, model_name, parameters, size, is_dgate=is_dgate, in_group=in_group
        )
    )
    print("dgate suzuki_trotter 4th order, serie 2/4")
    dgate_imaginary_time.append(
        suzu_trotter_obc_exp(
            db1S, model_name, parameters, size, is_dgate=is_dgate, in_group=in_group
        )
    )
    print("dgate suzuki_trotter 4th order, serie 3/4")
    dgate_imaginary_time.append(
        suzu_trotter_obc_exp(
            db2F, model_name, parameters, size, is_dgate=is_dgate, in_group=in_group
        )
    )
    print("dgate suzuki_trotter 4th order, serie 4/4\n")
    dgate_imaginary_time.append(
        suzu_trotter_obc_exp(
            db2S, model_name, parameters, size, is_dgate=is_dgate, in_group=in_group
        )
    )

    return dgate_imaginary_time


def create_maximal_entangled_state(size, model_name, in_group=False):
    head, _, tail = model_name.split("_")

    operator_name = head + "_id_" + tail
    coef = []
    dmps = []
    for l in range(size):
        coef.append(1 / _sqrt(2))
        tmp_blocs = single_operator(operator_name, 1 / _sqrt(2))
        if operator_name == "sh_id_no":
            new_blocs = {
                (0, 0, 0, 0): tmp_blocs[(0, 0)].reshape(1, 2, 2, 1),
            }
        elif operator_name == "sh_id_u1":
            new_blocs = {
                (0, 0, 0, 0): tmp_blocs[(0, 0)].reshape(1, 1, 1, 1),
                (0, 1, 1, 0): tmp_blocs[(1, 1)].reshape(1, 1, 1, 1),
            }
        else:
            _exit(f"The maximal entangled state does not exist for {operator_name}.")
        dmps.append(new_blocs)
    return coef, dmps


def initialize_idmrg_odd_size(
    dst_left_bloc,
    imps_left,
    dst_right_bloc,
    imps_right,
    imps_middle,
    ham_left,
    ham_middle,
    ham_right,
    *,
    position,
    size,
    conserve_total,
    d,
):
    env_bloc = create_three_sites_env_blocs(
        ham_left, ham_middle, ham_right, conserve_total
    )

    sim_dict = {
        "dw_one_serie": 0,
        "dw_total": 0,
        "chi_max": 10,
        "eps_truncation": 1e-20,
    }
    # minimize energy
    eigenvalues, eigenvectors = {}, {}
    for keys in env_bloc.keys():
        mat = env_bloc[keys]
        new_shape = (
            mat.shape[0] * mat.shape[1] * mat.shape[2] * mat.shape[3] * mat.shape[4],
            mat.shape[5] * mat.shape[6] * mat.shape[7] * mat.shape[8] * mat.shape[9],
        )
        # E, vec = smallest_eigenvectors_from_scipy(mat.reshape(new_shape))
        eigenvalues[(keys[0], keys[1], keys[2], keys[3], keys[4])] = E[0]
        eigenvectors[(keys[0], keys[1], keys[2], keys[3], keys[4])] = vec.reshape(
            (mat.shape[0], mat.shape[1], mat.shape[2], mat.shape[3], mat.shape[4])
        )

    # select_quantum_sector
    diff = min(size - conserve_total, conserve_total)
    if position < diff or position > size - diff:
        allowed_sector = list(range(d))  # all
    elif conserve_total <= size // 2:
        allowed_sector = list(range(d - 1))  # inc
    elif size - conserve_total <= size // 2:
        allowed_sector = list(range(1, d))  # dec
    else:
        allowed_sector = []  # should never occur

    for key in list(eigenvectors.keys()):
        if not (key[1] in allowed_sector and key[2] in allowed_sector and key[3]):
            eigenvectors.pop(key)
            eigenvalues.pop(key)
    apply_eigenvalues(eigenvalues, eigenvectors)

    # TODO!
    theta_to_mm(
        eigenvectors,
        imps_middle,
        imps_right,
        sim_dict,
        sim_dict["chi_max"],
        sim_dict["normalize"],
        None,
        1,
        sim_dict["eps_truncation"],
    )

    contract_mps_mpo_mps_left_border(dst_left_bloc, imps_left, ham_left, imps_left)
    contract_mps_mpo_mps_right_border(dst_right_bloc, imps_right, ham_right, imps_right)


def initialize_idmrg_even_size(
    dst_left_bloc,
    imps_left,
    dst_right_bloc,
    imps_right,
    ham_left,
    ham_right,
    *,
    position,
    size,
    conserve_total,
    d,
):
    env_bloc = create_two_sites_env_blocs(ham_left, ham_right, conserve_total)
    select_quantum_sector(
        env_bloc, position, size=size, qnum_conserved=conserve_total, d=d
    )
    sim_dict = {
        "dw_one_serie": 0,
        "dw_total": 0,
        "chi_max": 10,
        "eps_truncation": 1e-20,
        "normalize": True,
    }
    # minimize energy
    eigenvalues, eigenvectors = {}, {}
    minimize_theta(env_bloc, eigenvalues, eigenvectors, sim_dict["chi_max"])
    apply_eigenvalues(eigenvalues, eigenvectors)

    theta_to_mm(
        eigenvectors,
        imps_left,
        {},
        sim_dict,
        sim_dict["chi_max"],
        sim_dict["normalize"],
        True,
        1,
        sim_dict["eps_truncation"],
    )
    theta_to_mm(
        eigenvectors,
        {},
        imps_right,
        sim_dict,
        sim_dict["chi_max"],
        sim_dict["normalize"],
        False,
        -1,
        sim_dict["eps_truncation"],
    )

    contract_mps_mpo_mps_left_border(dst_left_bloc, imps_left, ham_left, imps_left)
    contract_mps_mpo_mps_right_border(dst_right_bloc, imps_right, ham_right, imps_right)


def finalize_idmrg_even_size(
    dst_left,
    dst_right,
    bloc_left,
    bloc_right,
    ham_mpo_left,
    ham_mpo_right,
    sim_dict,
    *,
    position,
    size,
    conserve_total,
    d,
):
    # contract and permute
    env_bloc = create_env_blocs(bloc_left, ham_mpo_left, ham_mpo_right, bloc_right)
    select_quantum_sector(
        env_bloc, position, size=size, qnum_conserved=conserve_total, d=d
    )
    theta = minimize_on_mm(env_bloc, None, None, None, driver="scipy")
    theta_to_mm(
        theta,
        dst_left,
        dst_right,
        sim_dict,
        sim_dict["chi_max"],
        True,
        None,
        0,
        sim_dict["eps_truncation"],
    )


def initialize_left_right(mps, ham, position):
    left_blocs = []
    right_blocs = []
    tmp_dst = {}
    contract_mps_mpo_mps_left_border(tmp_dst, mps[0], ham[0], mps[0])
    filter_left_right(tmp_dst)
    left_blocs.append(_copy(tmp_dst))
    tmp_dst.clear()
    contract_mps_mpo_mps_right_border(tmp_dst, mps[-1], ham[-1], mps[-1])
    filter_left_right(tmp_dst)
    right_blocs.append(_copy(tmp_dst))
    tmp_dst.clear()

    for l in range(1, position - 1):
        tmp_dst = {}
        contract_left_bloc_mps(tmp_dst, left_blocs[-1], mps[l], ham[l], mps[l])
        filter_left_right(tmp_dst)
        left_blocs.append(_copy(tmp_dst))
        tmp_dst.clear()

    for l in range(len(mps) - 1, position - 1, -1):
        tmp_dst = {}
        contract_right_bloc_mps(tmp_dst, right_blocs[-1], mps[l], ham[l], mps[l])
        filter_left_right(tmp_dst)
        right_blocs.append(_copy(tmp_dst))
        tmp_dst.clear()

    return left_blocs + right_blocs[::-1]


def initialize_left_right_variance(mps, ham, position):
    left_blocs = []
    right_blocs = []
    tmp_dst = {}
    contract_mps_mpo_mpo_mps_left_border(tmp_dst, mps[0], ham[0], ham[0], mps[0])
    left_blocs.append(_copy(tmp_dst))
    tmp_dst.clear()
    contract_mps_mpo_mpo_mps_right_border(tmp_dst, mps[-1], ham[-1], ham[-1], mps[-1])
    right_blocs.append(_copy(tmp_dst))
    tmp_dst.clear()

    for l in range(1, position - 1):
        tmp_dst = {}
        contract_left_bloc_mps_mpo(
            tmp_dst, left_blocs[-1], mps[l], ham[l], ham[l], mps[l]
        )
        left_blocs.append(_copy(tmp_dst))
        tmp_dst.clear()

    for l in range(len(mps) - 1, position - 1, -1):
        tmp_dst = {}
        contract_right_bloc_mps_mpo(
            tmp_dst, right_blocs[-1], mps[l], ham[l], ham[l], mps[l]
        )
        right_blocs.append(_copy(tmp_dst))
        tmp_dst.clear()

    return left_blocs + right_blocs[::-1]
