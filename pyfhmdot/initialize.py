from copy import deepcopy as _copy
from numpy import sqrt as _sqrt
from numpy import iscomplex as _iscomplex
from numpy import imag as _imag

import sys

from pyfhmdot.models.pymodels import suzu_trotter_obc_exp
from pyfhmdot.models.pymodels import hamiltonian_obc
from pyfhmdot.models.pyoperators import single_operator
from pyfhmdot.conservation import conserve_qnum
from pyfhmdot.routine.indices import internal_qn_sum,internal_qn_sub

from pyfhmdot.intense.contract import (
    contract_left_bloc_mps,
    contract_left_bloc_mps_mpo,
    contract_left_right_mpo_mpo_permute,
    contract_mps_mpo_mpo_mps_left_border,
    contract_mps_mpo_mpo_mps_right_border,
    contract_mps_mpo_mps_left_border,
    contract_mps_mpo_mps_right_border,
    contract_right_bloc_mps,
    contract_right_bloc_mps_mpo,
)

from pyfhmdot.intense.mul_mp import multiply_mp
from pyfhmdot.routine.eig_routine import smallest_eigenvectors_from_scipy
from pyfhmdot.routine.interface import (
    apply_eigenvalues,
    minimize_theta,
    select_lowest_blocs,
    theta_to_mm,
)


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
            sys.exit(f"The maximal entangled state does not exist for {operator_name}.")
        dmps.append(new_blocs)
    return coef, dmps


def create_id_mp(model_name, position, is_left):
    from numpy import eye
    from numpy import array

    head, _, tail = model_name.split("_")

    operator_name = head + "_id_" + tail
    coef = 1 / _sqrt(2)
    if operator_name == "sh_id_no":
        if is_left:
            new_blocs = {
                (0, 0, 0): coef
                * eye(2**position).reshape(2 ** (position - 1), 2, 2**position),
            }
        else:
            new_blocs = {
                (0, 0, 0): coef
                * eye(2**position).reshape(2**position, 2, 2 ** (position - 1)),
            }
    elif operator_name == "sh_id_u1":
        if is_left and position == 1:
            new_blocs = {
                (0, 0, 0): array([coef * 1.0]).reshape(1, 1, 1),
                (0, 1, 1): array([coef * 1.0]).reshape(1, 1, 1),
            }
        elif not is_left and position == 1:
            new_blocs = {
                (0, 0, 0): array([coef * 1.0]).reshape(1, 1, 1),
                (1, 1, 0): array([coef * 1.0]).reshape(1, 1, 1),
            }
        elif is_left and position == 2:
            new_blocs = {
                (0, 0, 0): array([coef * 1.0]).reshape(1, 1, 1),
                (0, 1, 1): array([coef * 1.0]).reshape(1, 1, 1),
                (1, 0, 1): array([coef * 1.0]).reshape(1, 1, 1),
                (1, 1, 2): array([coef * 1.0]).reshape(1, 1, 1),
            }
        elif not is_left and position == 2:
            new_blocs = {
                (0, 0, 0): array([coef * 1.0]).reshape(1, 1, 1),
                (1, 1, 0): array([coef * 1.0]).reshape(1, 1, 1),
                (1, 0, 1): array([coef * 1.0]).reshape(1, 1, 1),
                (2, 1, 1): array([coef * 1.0]).reshape(1, 1, 1),
            }
        else:
            sys.exit(f"The identity mp is usefull for borders only.")
    else:
        sys.exit(f"The identity mp does not exist for {operator_name}.")

    return coef, new_blocs


def initialize_idmrg_odd_size(
    dst_left_bloc,
    imps_left,
    dst_right_bloc,
    imps_right,
    imps_middle,
    ham_left,
    ham_right,
    ham_middle,
    *,
    position,
    size,
    conserve_total,
    d,
):
    tmp_tmp_env_blocs = {}
    multiply_mp(tmp_tmp_env_blocs, ham_left, ham_middle, [3], [0])
    # tmp_tmp_env_blocs
    #    2| |4
    # 0 -|___|- 5
    #    1| |3
    tmp_env_blocs = {}
    multiply_mp(tmp_env_blocs, tmp_tmp_env_blocs, ham_right, [5], [0])
    # tmp_env_blocs
    #    2| |4 |6
    # 0 -|_____ _|- 7
    #    1| |3 |5
    env_bloc = {}
    for key in tmp_env_blocs.keys():
        new_key = (0, key[1], key[3], key[5], 0, 0, key[2], key[4], key[6], 0)
        tmp_shape = tmp_env_blocs[key].shape
        new_shape = (
            1,
            tmp_shape[1],
            tmp_shape[3],
            tmp_shape[5],
            1,
            1,
            tmp_shape[2],
            tmp_shape[4],
            tmp_shape[5],
            1,
        )
        env_bloc[new_key] = (
            tmp_env_blocs[key].transpose([0, 1, 3, 5, 2, 4, 6, 7]).reshape(new_shape)
        )

    sim_dict = {
        "dw_one_serie": 0,
        "dw_total": 0,
        "chi_max": 10,
        "eps_truncation": 1e-20,
    }
    # minimize energy
    eigenvalues = {}
    eigenvectors = {}
    for keys in env_bloc.keys():
        mat = env_bloc[keys]
        new_shape = (
            mat.shape[0] * mat.shape[1] * mat.shape[2] * mat.shape[3] * mat.shape[4],
            mat.shape[5] * mat.shape[6] * mat.shape[7] * mat.shape[8] * mat.shape[9],
        )
        E, vec = smallest_eigenvectors_from_scipy(mat.reshape(new_shape))
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
    # select_lowest_blocs(eigenvalues, eigenvectors)
    # apply_eigenvalues(eigenvalues, eigenvectors)

    # TODO!
    theta_to_mm(
        eigenvectors,
        imps_middle,
        imps_right,
        sim_dict,
        sim_dict["chi_max"],
        True,
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
    tmp_env_blocs = {}
    multiply_mp(tmp_env_blocs, ham_left, ham_right, [3], [0])
    # tmp_env_blocs
    #    2| |4
    # 0 -|___|- 5
    #    1| |3
    env_bloc = {}
    for key in tmp_env_blocs.keys():
        new_key = (0, key[1], key[3], conserve_total, 0, key[2], key[4], conserve_total)
        tmp_shape = tmp_env_blocs[key].shape
        new_shape = (1, tmp_shape[1], tmp_shape[3], 1, 1, tmp_shape[2], tmp_shape[4], 1)
        env_bloc[new_key] = (
            tmp_env_blocs[key].transpose([0, 1, 3, 2, 4, 5]).reshape(new_shape)
        )

    allowed_sector_left = conserve_qnum(1,size=size,qnum_conserved=conserve_total,d=d)
    allowed_sector_right = conserve_qnum(size-1,size=size,qnum_conserved=conserve_total,d=d)
    for key in list(env_bloc.keys()):
        shape = env_bloc[key].shape
        if (
            not (internal_qn_sum(key[0],key[1]) in allowed_sector_left)
            or not (internal_qn_sub(key[3],key[2]) in allowed_sector_right)
            or not (internal_qn_sum(key[4],key[5]) in allowed_sector_left)
            or not (internal_qn_sub(key[7],key[6]) in allowed_sector_right)
        ):
            env_bloc.pop(key)  # quantum conserved is used here
        elif not (
            shape[0] * shape[1] * shape[2] * shape[3]
            == shape[4] * shape[5] * shape[6] * shape[7]
        ):
            env_bloc.pop(key)  # non physical blocs
        

    sim_dict = {
        "dw_one_serie": 0,
        "dw_total": 0,
        "chi_max": 10,
        "eps_truncation": 1e-20,
    }
    # minimize energy
    eigenvalues = {}
    eigenvectors = {}
    minimize_theta(env_bloc, eigenvalues, eigenvectors, sim_dict["chi_max"])
    
    # select_lowest_blocs(eigenvalues, eigenvectors)
    # apply_eigenvalues(eigenvalues, eigenvectors)

    theta_to_mm(
        eigenvectors,
        imps_left,
        {},
        sim_dict,
        sim_dict["chi_max"],
        True,
        True,
        -3,
        sim_dict["eps_truncation"],
    )
    theta_to_mm(
        eigenvectors,
        {},
        imps_right,
        sim_dict,
        sim_dict["chi_max"],
        True,
        False,
        2,
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
    # select_quantum_sector
    allowed_sector_left = conserve_qnum(position,size=size,qnum_conserved=conserve_total,d=d)
    allowed_sector_right = conserve_qnum(size-position,size=size,qnum_conserved=conserve_total,d=d)

    # contract and permute
    env_bloc = {}
    contract_left_right_mpo_mpo_permute(
        env_bloc, bloc_left, ham_mpo_left, ham_mpo_right, bloc_right
    )
    for key in list(env_bloc.keys()):
        shape = env_bloc[key].shape
        if (
            not (internal_qn_sum(key[0],key[1]) in allowed_sector_left)
            or not (internal_qn_sub(key[3],key[2]) in allowed_sector_right)
            or not (internal_qn_sum(key[4],key[5]) in allowed_sector_left)
            or not (internal_qn_sub(key[7],key[6]) in allowed_sector_right)
        ):
            env_bloc.pop(key)  # quantum conserved is used here
        elif not (
            shape[0] * shape[1] * shape[2] * shape[3]
            == shape[4] * shape[5] * shape[6] * shape[7]
        ):
            env_bloc.pop(key)  # non physical blocs
    
    # minimize energy
    eigenvalues = {}
    eigenvectors = {}
    minimize_theta(env_bloc, eigenvalues, eigenvectors, sim_dict["chi_max"])

    # for key in list(eigenvectors.keys()):
    #     if not (
    #         key[1] in allowed_sector and key[2] in allowed_sector and key[1] == key[2]
    #     ):
    #         eigenvectors.pop(key)
    #         eigenvalues.pop(key)
    #         _warning("eigenvectors removed a posteriori.")
    #select_lowest_blocs(eigenvalues, eigenvectors)
    # select_quantum_sector(eigenvalues, eigenvectors)
    #apply_eigenvalues(eigenvalues, eigenvectors)

    theta_to_mm(
        eigenvectors,
        dst_left,
        dst_right,
        sim_dict,
        sim_dict["chi_max"],
        True,
        None,
        -3,
        sim_dict["eps_truncation"],
    )


def initialize_left_right(mps, ham):
    left_blocs = []
    right_blocs = []
    tmp_dst = {}
    contract_mps_mpo_mps_left_border(tmp_dst, mps[0], ham[0], mps[0])
    left_blocs.append(_copy(tmp_dst))
    tmp_dst.clear()
    contract_mps_mpo_mps_right_border(tmp_dst, mps[-1], ham[-1], mps[-1])
    right_blocs.append(_copy(tmp_dst))
    tmp_dst.clear()

    for l in range(1, len(mps) - 1):
        tmp_dst = {}
        contract_left_bloc_mps(tmp_dst, left_blocs[-1], mps[l], ham[l], mps[l])
        left_blocs.append(_copy(tmp_dst))
        tmp_dst.clear()

    for l in range(len(mps) - 1, 1, -1):
        tmp_dst = {}
        contract_right_bloc_mps(tmp_dst, right_blocs[-1], mps[l], ham[l], mps[l])
        right_blocs.append(_copy(tmp_dst))
        tmp_dst.clear()

    return left_blocs, right_blocs[::-1]


def initialize_left_right_variance(mps, ham):
    left_blocs = []
    right_blocs = []
    tmp_dst = {}
    contract_mps_mpo_mpo_mps_left_border(tmp_dst, mps[0], ham[0], ham[0], mps[0])
    left_blocs.append(_copy(tmp_dst))
    tmp_dst.clear()
    contract_mps_mpo_mpo_mps_right_border(tmp_dst, mps[-1], ham[-1], ham[-1], mps[-1])
    right_blocs.append(_copy(tmp_dst))
    tmp_dst.clear()

    for l in range(1, len(mps) - 1):
        tmp_dst = {}
        contract_left_bloc_mps_mpo(
            tmp_dst, left_blocs[-1], mps[l], ham[l], ham[l], mps[l]
        )
        left_blocs.append(_copy(tmp_dst))
        tmp_dst.clear()

    for l in range(len(mps) - 1, 1, -1):
        tmp_dst = {}
        contract_right_bloc_mps_mpo(
            tmp_dst, right_blocs[-1], mps[l], ham[l], ham[l], mps[l]
        )
        right_blocs.append(_copy(tmp_dst))
        tmp_dst.clear()

    return left_blocs, right_blocs[::-1]
