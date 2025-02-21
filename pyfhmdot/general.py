from numpy import sqrt as _sqrt
import sys


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


def create_hamiltonian(size, spin_name, qn_name, model_name, parameters, **kwargs):
    pass


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
