from pyfhmdot.simulation import sweep_eleven_times as _sweep_eleven_times


def infinite_to_finite_ground_state(size,left, ham, right, imps, idmrg_dict):
    pass


def variational_ground_state(mps, mpo, zdmrg_dict):
    # left_bloc right_bloc
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
