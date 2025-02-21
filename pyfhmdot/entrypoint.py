from pyfhmdot.initialize import (
    create_infinite_hamiltonian as _create_infinite_hamiltonian,
    initialize_idmrg_even_size as _initialize_idmrg_even_size,
    initialize_idmrg_odd_size as _initialize_idmrg_odd_size,
    initialize_left_right,
    initialize_left_right_variance,
)

from pyfhmdot.simulation import (
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
    # initialize
    left_blocs, right_blocs = initialize_left_right(mps, ham)
    left_var, right_var = initialize_left_right_variance(mps, ham)
    # warmup
    for i in range(zdmrg_dict["nb_warmup"]):
        chi_max = max(zdmrg_dict["chi_max"] // 4, 1)

    # converge
    for i in range(zdmrg_dict["nb_sweeps"]):
        pass


def time_evolve_single(mps, ggate, sdmrg_dict):
    # while
    # dynamical_mps(mps, ggate, sdmrg_dict)
    pass


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
    """
        if ( sim_dict["beta"] / (sim_dict["save_every"]*sim_dict["dbeta"])):

            output = outputHEAD + f"{sim_dict['beta']}.h5"

            if sim_dict["right_direction"]:
                info["central_matrix"] = 2
            else:
                info["central_matrix"] = L - 1

            info["chi_middle_chain"] = list(
                (_.shape[0] for _ in dmps[L / 2]._blocks.values())
            )

            mps2save = [_.split_pair(("s", l + 1)) for l, _ in enumerate(dmps)]

            _a_mps = list2gen_with_coef(mps2save, coefsite)

             info["dnorm"] = 1.0
            info["norm"] = Qmeasure.obc_norm_density(L, _a_mps)
            del _a_mps
            info["2B"] = beta

            hdf5_create_mpo(output, mps2save, coefsite, model, info, sim_dict, "TDMRG")
    """
