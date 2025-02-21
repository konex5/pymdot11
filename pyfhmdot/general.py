from numpy import sqrt as _sqrt


def get_model_info(hamiltonian_path):
    return {"size": 10, "spin_name": "sh", "qn_name": "u1", "interaction_range": 2}


def get_simulation_info():
    return {
        "dw_weights": 0,
        "eps_trunkation": 10 ** -8,
        "chi_max": 600,
        "conserve_qnum": True,
    }


def create_maximal_entangled_state(size, spin_name, qn_name, **kwargs):
    from pyfhmdot.pyoperators import single_operator

    operator_name = spin_name + "_id_" + qn_name
    coef = []
    dmps = []
    for l in range(size):
        coef.append(1 / _sqrt(2))
        tmp_blocs = single_operator(operator_name, 1 / _sqrt(2))
        new_blocs = {
            (0, 0, 0, 0): tmp_blocs[(0, 0)].reshape(1, 1, 1, 1),
            (0, 1, 1, 0): tmp_blocs[(1, 1)].reshape(1, 1, 1, 1),
        }
        dmps.append(new_blocs)
    return coef, dmps
