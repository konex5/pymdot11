from numpy import sqrt as _sqrt
from numpy import iscomplex as _iscomplex
from numpy import imag as _imag

import sys

from pyfhmdot.models.pymodels import suzu_trotter_obc_exp
from pyfhmdot.models.pymodels import hamiltonian_obc
from pyfhmdot.models.pyoperators import single_operator


def create_hamiltonian(model_name, parameters, size):
    """
    qnmodel='sh_xxz-hz_no' or 'ru_ldxxz-hz_u1'
    """
    hamiltonian_obc(model_name, parameters, size)


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
            sys.exit(f"The maximal entangled state does not exist for {operator_name}")
        dmps.append(new_blocs)
    return coef, dmps


def change_right_index(mp, new_index):
    dst_mp = {}
    for key, value in mp.items():
        dst_mp[(key[0], key[1], new_index)] = value
    return dst_mp
