from pyfhmdot.initialize import (
    create_infinite_hamiltonian as _create_infinite_hamiltonian,
    initialize_idmrg_even_size as _initialize_idmrg_even_size,
    initialize_idmrg_odd_size as _initialize_idmrg_odd_size,
    initialize_left_right,
    initialize_left_right_variance,
)

from pyfhmdot.simulation import (
    compress_mps,
    dmrg_sweeps as _dmrg_sweeps,
    dmrg_warmup as _dmrg_warmup,
    sweep_eleven_times as _sweep_eleven_times,
    idmrg_even as _idmrg_even,
)


def infinite_to_finite_ground_state(
    dst_imps, model_name, parameters, idmrg_dict, *, size, conserve_total
):
    """
    conserve is minimal at 0 and maximal at size by increment of 1.
    """
    dst_imps_left = []
    dst_imps_right = []
    ham_left, ham_mpo, ham_right = _create_infinite_hamiltonian(model_name, parameters)

    head = model_name.split("_")[0]
    if head == "sh":
        d = 2
    elif head == "so":
        d = 3
    elif head == "sf":
        d = 4

    imps_left, imps_right = {}, {}
    bloc_left, bloc_right = {}, {}
    if size % 2 == 0:
        _initialize_idmrg_even_size(
            bloc_left,
            imps_left,
            bloc_right,
            imps_right,
            ham_left,
            ham_right,
            position=1,
            size=size,
            conserve_total=conserve_total,
            d=d,
        )
        dst_imps_left.append(imps_left)
        dst_imps_right.append(imps_right)
    else:
        imps_middle = {}
        _initialize_idmrg_odd_size(
            bloc_left,
            imps_left,
            bloc_right,
            imps_right,
            imps_middle,
            ham_left,
            ham_right,
            ham_mpo[0],
            position=1,
            size=size,
            conserve_total=conserve_total,
            d=d,
        )

    _idmrg_even(
        dst_imps_left,
        dst_imps_right,
        bloc_left,
        bloc_right,
        ham_mpo,
        idmrg_dict,
        iterations=(size - len(dst_imps_left) - 3) // 2,
        size=size,
        conserve_total=conserve_total,
        d=d,
    )

    for i in range(len(dst_imps_left)):
        dst_imps.append(dst_imps_left[i])
    for i in range(len(dst_imps_right)):
        dst_imps.append(dst_imps_right[len(dst_imps_right) - 1 - i])


def variational_ground_state(mps, ham, zdmrg_dict):
    # compress mps
    compress_mps(
        mps,
        zdmrg_dict["chi_max_warmup"],
        True,
        zdmrg_dict["eps_truncation"],
        start_left=True,
    )
    # initialize
    left_right = initialize_left_right(mps, ham, 2)
    left_right_var = initialize_left_right_variance(mps, ham, 2)
    # warmup
    _dmrg_warmup(mps, ham, left_right, zdmrg_dict, start_left=True)  # nb_warmup
    # initialize
    # left_right_var = initialize_left_right_variance(mps, ham, 2)
    # converge
    _dmrg_sweeps(mps, ham, left_right, left_right_var, zdmrg_dict, start_left=True)


def time_evolve_single(mps, ggate, sim_dict):
    """
    sim_dict["tau_max"]
    sim_dict["dtau"]
    sim_dict["eps"]
    sim_dict["dw_total"]
    sim_dict["dw_one_serie"]
    sim_dict["chi_max"]
    sim_dict["normalize"]
    sim_dict["start_left"]
    sim_dict["start_odd_bonds"]
    sim_dict["save_every"]
    info_dict["central_matrix"]
    info_dict["chi_middle_chain"]
    """

    dw_dict = {"dw_one_serie": 0, "dw_total": sim_dict["dw_total"]}
    _sweep_eleven_times(
        mps,
        ggate,
        dw_dict=dw_dict,
        chi_max=sim_dict["chi_max"],
        normalize=sim_dict["normalize"],
        eps=sim_dict["eps_truncation"],
        strategy=0,  # conservation of qnum
        start_left=sim_dict["start_left"],
        start_odd_bonds=sim_dict["start_odd_bonds"],
    )
    sim_dict["dw_one_serie"] = dw_dict["dw_one_serie"]
    sim_dict["dw_total"] += dw_dict["dw_total"]
    print("discarded weight in one step :", sim_dict["dw_one_serie"])
    print("discarded weight accumulate  :", sim_dict["dw_total"])


def dynamical_dmps(dmps, dggate, sim_dict):
    """
    sim_dict["tau_max"]
    sim_dict["dtau"]
    sim_dict["eps"]
    sim_dict["dw_total"]
    sim_dict["dw_one_serie"]
    sim_dict["chi_max"]
    sim_dict["normalize"]
    sim_dict["start_left"]
    sim_dict["start_odd_bonds"]
    sim_dict["save_every"]
    info_dict["central_matrix"]
    info_dict["chi_middle_chain"]
    """

    dw_dict = {"dw_one_serie": 0, "dw_total": sim_dict["dw_total"]}
    _sweep_eleven_times(
        dmps,
        dggate,
        dw_dict=dw_dict,
        chi_max=sim_dict["chi_max"],
        normalize=sim_dict["normalize"],
        eps=sim_dict["eps_truncation"],
        start_left=sim_dict["start_left"],
        start_odd_bonds=sim_dict["start_odd_bonds"],
    )
    sim_dict["dw_one_serie"] = dw_dict["dw_one_serie"]
    sim_dict["dw_total"] += dw_dict["dw_total"]
    print("discarded weight in one step :", sim_dict["dw_one_serie"])
    print("discarded weight accumulate  :", sim_dict["dw_total"])


def time_evolve_double(dmps, dggate, ddmrg_dict):
    # while
    dynamical_dmps(dmps, dggate, ddmrg_dict)


def lowering_temperature(dmps, dggate, ldmrg_dict):
    dynamical_dmps(dmps, dggate, ldmrg_dict)
