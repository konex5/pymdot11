from pyfhmdot.utils.iotools import (
    add_dictionary,
    load_dictionary,
    add_single_mp,
    load_single_mp,
)


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


def add_state_info(filepath, d):
    """
    {
        "size" : 12
        "dbeta": 2.0
        "time": 0.5
        "dw_total": 1e-5
        "normalize": 1 #True
        "chi_middle": 30
    }
    """
    add_dictionary(filepath, d, folder="INFO_STATE")


def add_model_idmrg_simulation(filepath, parameters):
    """
    {
        "eps_truncation": 10 ** -8,
        "chi_max": 600,
    }
    """
    add_dictionary(filepath, parameters, folder="INFO_SIM_IDMRG")


def add_model_zdmrg_simulation(filepath, parameters):
    """
    {
        "eps_truncation": 10 ** -8,
        "chi_max": 600,
        "nb_warmup_sweep": 6,
        "nb_sweep": 6,
        "store_state": 2,
    }
    """
    pass


def add_model_tdmrg_simulation(filepath, parameters):
    """
    {
        "dtau": 0.025,
        "normalize": 1, #True
        "dw_one_step": 0,
        "dw_total": 0,
        "eps_truncation": 10 ** -8,
        "chi_max": 600,
        "save_every": -1,
        "tau_max": 4,
    }
    """
    add_dictionary(filepath, parameters, folder="INFO_SIM_TIME_DMRG")


def add_model_bdmrg_simulation(filepath, parameters):
    """
    {
        "dtau": 0.025
        "normalize" : 0, #False
        "dw_one_step": 0,
        "dw_total": 0,
        "eps_truncation": 10 ** -8,
        "chi_max": 600,
        "save_every": -1,
        "tau_max": 4,
    }
    """
    add_dictionary(filepath, parameters, folder="INFO_SIM_BETA_DMRG")


def add_mps(filepath, mps, *, folder):
    for i, mp in enumerate(mps):
        add_single_mp(filepath, mp, i, folder=folder)


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
    d = {}
    load_dictionary(filepath, d, folder="INFO_PARAMETERS")
    return d


def load_model_state(filepath):
    d = {}
    load_dictionary(filepath, d, folder="INFO_STATE")
    return d


def load_model_idmrg_simulation(filepath):
    d = {}
    load_dictionary(filepath, d, folder="INFO_SIM_IDMRG")
    return d


def load_model_tdmrg_simulation(filepath):
    d = {}
    load_dictionary(filepath, d, folder="INFO_SIM_TIME_DMRG")
    return d


def load_model_bdmrg_simulation(filepath):
    d = {}
    load_dictionary(filepath, d, folder="INFO_SIM_BETA_DMRG")
    return d


def load_mps(filepath, size, *, folder):
    mps = []
    for i in range(size):
        mp = {}
        load_single_mp(filepath, mp, i, folder=folder)
        mps.append(mp)
    return mps
