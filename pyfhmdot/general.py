from numpy import sqrt as _sqrt
from numpy import iscomplex as _iscomplex
from numpy import imag as _imag

import sys

from pyfhmdot.models.pymodels import hamiltonian_obc, suzu_trotter_obc_exp
from pyfhmdot.models.pyoperators import single_operator
from pyfhmdot.utils.iotools import add_dictionary, load_dictionary


def translate_qn_name(model_name):
    head, _, tail = model_name.split("_")
    if head == "no":
        qn_num = 0
    elif head == "u1":
        qn_num == 1
    else:
        qn_num = -10
    if tail == "sh":
        spin_num = 0
    elif tail == "so":
        spin_num = 1
    elif tail == "ru":
        spin_num = 2
    elif tail == "sf":
        spin_num = 3
    else:
        spin_num = -10
    return 4 * qn_num + spin_num


def add_model_info(filepath, info):
    """
    {
        "sh_xxz-hz_u1" : 0, # number is a unique identifiers for spin size (sh) and qn (u1)
        "size": 10,
    }
    """
    size = info.pop("size")
    for key in info.keys():
        model_name = key
    add_dictionary(
        filepath,
        {model_name: translate_qn_name(model_name), "size": size},
        folder="INFO",
    )


def add_model_parameters(filepath, parameters):
    """
    {
        "Jxy" : 2.0,
        "hz": 3.4,
    }
    """
    add_dictionary(filepath, parameters, folder="INFO_PARAMETERS")


def add_model_simulation(filepath, parameters):
    """TODO
    {
        "eps_truncation": 10 ** -8,
        "chi_max": 600,
        "nb_warmup_sweep": 6,
        "nb_sweep": 6,
        "store_state": 2,
    }
    {
        "discarded_weights": 0,
        "eps_truncation": 10 ** -8,
        "chi_max": 600,
        "delta": 0.025,
        "store_state": 0.5,
        "stop_value": 4,
    }
    """
    # add_dictionary(filepath,"INFO_SIM_0DMRG",parameters)
    # add_dictionary(filepath,"INFO_SIM_TDMRG",parameters)
    pass


# def get_details_zdmrg():
#     return
#
# def get_details_tdmrg():
#     return
#
# def get_all_details():
#     pass


def load_model_info_size(filepath):
    info = {}
    load_dictionary(filepath, info, folder="INFO")
    return info["size"]


def load_model_info_model_name(filepath):
    info = {}
    load_dictionary(filepath, info, folder="INFO")
    size = info.pop("size")
    for key in info.keys():
        model_name = key
    return model_name


def load_model_parameters(filepath):
    return load_dictionary(filepath, "INFO_PARAMETERS")


def load_model_simulation(filepath):
    # return load_dictionary(filepath,"INFO_PARAMETERS")
    pass


def create_hamiltonian(model_name, parameters, size):
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
    db = abs(dbeta)
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


def create_maximal_entangled_state(size, model_name):
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
