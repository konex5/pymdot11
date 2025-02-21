#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os

from pyfhmdot.utils.general import (
    add_model_bdmrg_simulation,
    add_model_info,
    add_mps,
    load_model_info_model_name,
    load_model_info_size,
    load_model_state,
    load_model_tdmrg_simulation,
    load_mps,
)
from pyfhmdot.intense.splitgroup import group_all, split_all
from pyfhmdot.utils.iotools import (
    check_filename_and_extension_h5,
    create_h5,
)

from pyfhmdot.entrypoint import time_evolve_double


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="cli, run Tdmrg simulation")
    parser.add_argument(
        "-G",
        "--gates",
        type=str,
        action="store",
        help="gates path",
        required=True,
    )
    parser.add_argument(
        "-M",
        "--dmps",
        type=str,
        action="store",
        help="hamiltonian path",
        required=True,
    )
    parser.add_argument(
        "-o", "--output", type=str, action="store", help="output path", required=True
    )

    arguments = parser.parse_args()

    if not check_filename_and_extension_h5(arguments.gates):
        sys.exit(
            f"cli_Tdmrg.py: error: the hamiltonian path {arguments.gates} is not a valid path."
        )
    if not check_filename_and_extension_h5(arguments.dmps):
        sys.exit(
            f"cli_Tdmrg.py: error: the hamiltonian path {arguments.dmps} is not a valid path."
        )
    if not os.path.exists(os.path.dirname(arguments.output)):
        sys.exit(
            f"cli_Tdmrg.py: error: the output dirpath {os.path.dirname(arguments.output)} is not a valid directory path."
        )

    size = load_model_info_size(arguments.gates)
    model_name = load_model_info_model_name(arguments.gates)
    tdmrg_simulation_parameters = load_model_tdmrg_simulation(arguments.gates)
    info_state = load_model_state(arguments.dmps)
    dbeta = info_state["dbeta"]
    time = info_state["time"]

    dmps = group_all(model_name, load_mps(arguments.dmps, size, folder="QMP"))

    ggate = []
    for st in range(4):
        ggate.append(load_mps(arguments.gates, size - 1, folder=f"TIME_GATE_{st:02g}"))

    save = 0
    while (
        time
        + tdmrg_simulation_parameters["save_every"]
        * tdmrg_simulation_parameters["dtau"]
        < tdmrg_simulation_parameters["tau_max"]
    ):
        time_evolve_double(dmps, ggate, tdmrg_simulation_parameters)
        time += tdmrg_simulation_parameters["dtau"]
        save += 1
        tdmrg_simulation_parameters[
            "start_odd_bonds"
        ] = not tdmrg_simulation_parameters["start_odd_bonds"]
        tdmrg_simulation_parameters["start_left"] = not tdmrg_simulation_parameters[
            "start_left"
        ]

        if tdmrg_simulation_parameters["save_every"] == save:
            output_path = f"{arguments.output}/2B_{dbeta:07.4f}_t_{time:07.4f}.h5"
            create_h5(output_path)
            add_model_info(output_path, {model_name: 0, "size": size})
            add_model_bdmrg_simulation(output_path, tdmrg_simulation_parameters)
            add_mps(output_path, split_all(model_name, dmps), folder="QMP")
            save = 0
