from numpy import sqrt as _sqrt
import sys

from pyfhmdot.models.pymodels import suzu_trotter_obc_exp


def translate_qn_name(qn_num):
    if qn_num == 0:
        return "no"
    elif qn_num == 1:
        return "u1"
    else:
        return ""


def translate_spin_name(spin_num):
    if spin_num == 0:
        return "sh"
    elif spin_num == 1:
        return "so"
    elif spin_num == 2:
        return "sf"
    elif spin_num == 3:
        return "ldsh"
    else:
        return ""


def get_model_name(hamiltonian_path):
    return "hamiltonian description"


def get_model_info(hamiltonian_path):
    return {
        "size": 10,
        "spin_name": 0,
        "qn_name": 1,
        "interaction_range": 2,
        "periodicity": 2,
    }


def get_model_parameters(hamiltonian_path):
    return {"J": 1.0, "Jz": 2.0}


def get_details_zdmrg():
    return {
        "eps_truncation": 10 ** -8,
        "chi_max": 600,
        "nb_warmup_sweep": 6,
        "nb_sweep": 6,
        "store_state": 2,
    }


def get_details_tdmrg():
    return {
        "discarded_weights": 0,
        "eps_truncation": 10 ** -8,
        "chi_max": 600,
        "delta": 0.025,
        "store_state": 0.5,
        "stop_value": 4,
    }


def create_hamiltonian(model_name, parameters, size, dbeta, dtime):
    from pyfhmdot.models.pymodels import hamiltonian_obc, suzu_trotter_obc_exp

    info = parameters
    info["size"] = size
    info["model_name"] = model_name
    info["dbeta"] = dbeta
    info["dtime"] = dtime

    ham_mpo = hamiltonian_obc(model_name, parameters, size)

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
    dbmiddle = db1S
    print("dgate suzuki_trotter imaginary time 4th order, serie 1/4")
    dgate_imaginary_time.append(
        suzu_trotter_obc_exp(
            db1F, model_name, parameters, size, is_dgate=False, in_group=True
        )
    )
    print("dgate suzuki_trotter imaginary time 4th order, serie 2/4")
    dgate_imaginary_time.append(
        suzu_trotter_obc_exp(
            db1S, model_name, parameters, size, is_dgate=False, in_group=True
        )
    )
    print("dgate suzuki_trotter imaginary time 4th order, serie 3/4")
    dgate_imaginary_time.append(
        suzu_trotter_obc_exp(
            db2F, model_name, parameters, size, is_dgate=False, in_group=True
        )
    )
    print("dgate suzuki_trotter imaginary time 4th order, serie 4/4\n")
    dgate_imaginary_time.append(
        suzu_trotter_obc_exp(
            db2S, model_name, parameters, size, is_dgate=False, in_group=True
        )
    )
    info["dbeta"] = db

    dgate_real_time = []
    sgate_real_time = []

    dt = abs(dtime)
    mIdt = -1.0j * dt
    dt1F = mIdt * factor1 / 2.0
    dt1S = mIdt * factor1
    dt2F = mIdt * (factor1 + factor2) / 2.0
    dt2S = mIdt * factor2
    dtmiddle = dt1S
    print("dgate suzuki_trotter real time 4th order, serie 1/4")
    dgate_real_time.append(
        suzu_trotter_obc_exp(
            dt1F, model_name, parameters, size, is_dgate=True, in_group=True
        )
    )
    print("dgate suzuki_trotter real time 4th order, serie 2/4")
    dgate_real_time.append(
        suzu_trotter_obc_exp(
            dt1S, model_name, parameters, size, is_dgate=True, in_group=True
        )
    )
    print("dgate suzuki_trotter real time 4th order, serie 3/4")
    dgate_real_time.append(
        suzu_trotter_obc_exp(
            dt2F, model_name, parameters, size, is_dgate=True, in_group=True
        )
    )
    print("dgate suzuki_trotter real time 4th order, serie 4/4\n")
    dgate_real_time.append(
        suzu_trotter_obc_exp(
            dt2S, model_name, parameters, size, is_dgate=True, in_group=True
        )
    )
    #
    print("sgate suzuki_trotter real time 4th order, serie 1/4")
    sgate_real_time.append(
        suzu_trotter_obc_exp(
            dt1F, model_name, parameters, size, is_dgate=False, in_group=False
        )
    )
    print("sgate suzuki_trotter real time 4th order, serie 2/4")
    sgate_real_time.append(
        suzu_trotter_obc_exp(
            dt1S, model_name, parameters, size, is_dgate=False, in_group=False
        )
    )
    print("sgate suzuki_trotter real time 4th order, serie 3/4")
    sgate_real_time.append(
        suzu_trotter_obc_exp(
            dt2F, model_name, parameters, size, is_dgate=False, in_group=False
        )
    )
    print("sgate suzuki_trotter real time 4th order, serie 4/4\n")
    sgate_real_time.append(
        suzu_trotter_obc_exp(
            dt2S, model_name, parameters, size, is_dgate=False, in_group=False
        )
    )
    info["dtime"] = dt

    return info, ham_mpo, dgate_imaginary_time, sgate_real_time, dgate_real_time


def create_maximal_entangled_state(size, spin_name, qn_name, **kwargs):
    from pyfhmdot.pyoperators import single_operator

    operator_name = translate_spin_name(spin_name) + "_id_" + translate_qn_name(qn_name)
    coef = []
    dmps = []
    for l in range(size):
        coef.append(1 / _sqrt(2))
        tmp_blocs = single_operator(operator_name, 1 / _sqrt(2))
        if operator_name == "sh_id_no":
            new_blocs = {
                (0, 0, 0, 0): tmp_blocs[(0, 0)].reshape(1, 2, 2, 1),
            }
        elif operator_name == "sh_id_no":
            new_blocs = {
                (0, 0, 0, 0): tmp_blocs[(0, 0)].reshape(1, 1, 1, 1),
                (0, 1, 1, 0): tmp_blocs[(1, 1)].reshape(1, 1, 1, 1),
            }
        else:
            sys.exit(f"The maximal entangled state does not exist for {operator_name}")
        dmps.append(new_blocs)
    return coef, dmps
