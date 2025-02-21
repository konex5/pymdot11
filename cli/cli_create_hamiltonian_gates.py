#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os

from pyfhmdot.utils.iotools import (
    check_filename_and_extension_to_create_h5,
    create_h5,
)
from pyfhmdot.utils.iodicts import check_filename_and_extension, read_dictionary

from pyfhmdot.general import (
    add_model_bdmrg_simulation,
    add_model_tdmrg_simulation,
    add_model_info,
    add_model_parameters,
    add_mps,
    create_hamiltonian_gates,
    load_model_info_model_name,
    load_model_info_size,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="cli, create hamiltonian gates")
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        action="store",
        help="model info path (json or toml)",
        required=True,
    )
    parser.add_argument(
        "-o", "--output", type=str, action="store", help="output path", required=True
    )
    arguments = parser.parse_args()

    if not check_filename_and_extension(arguments.input):
        sys.exit(
            f"cli_create_hamiltonian_gates.py: error: the input path {arguments.input} is not a valid path."
        )
    if not check_filename_and_extension_to_create_h5(arguments.output):
        sys.exit(
            f"cli_create_hamiltonian_gates.py: error: the output dirpath {os.path.dirname(arguments.output)} is not a valid directory path."
        )

    large_dictionary = read_dictionary(arguments.input)
    is_beta_simulation = "Tdmrg_simulation" in large_dictionary.keys()
    is_time_simulation = "tdmrg_simulation" in large_dictionary.keys()

    if not (is_time_simulation or is_beta_simulation):
        sys.exit(
            f"cli_create_hamiltonian_gates.py: error: no 'Tdmrg_simulation' or 'tdmrg_simulation' in input path {arguments.input}."
        )
    info = large_dictionary.pop("model")
    parameters = large_dictionary.pop("parameters")

    create_h5(arguments.output)
    add_model_info(arguments.output, info)
    add_model_parameters(arguments.output, parameters)
    model_name = load_model_info_model_name(arguments.output)
    size = load_model_info_size(arguments.output)

    if is_beta_simulation:
        bdmrg_simulation_parameters = large_dictionary.pop("Tdmrg_simulation")
        add_model_bdmrg_simulation(arguments.output, bdmrg_simulation_parameters)
        ham_mpo = create_hamiltonian_gates(
            model_name,
            parameters,
            size,
            dbeta=bdmrg_simulation_parameters["dtau"],
            is_dgate=False,
            in_group=False,
        )
        for st, step in enumerate(ham_mpo):
            add_mps(arguments.output, step, folder=f"TEMP_GATE_{st:02g}")

    if is_time_simulation:
        tdmrg_simulation_parameters = large_dictionary.pop("tdmrg_simulation")
        add_model_tdmrg_simulation(arguments.output, tdmrg_simulation_parameters)
        ham_mpo = create_hamiltonian_gates(
            model_name,
            parameters,
            size,
            dbeta=tdmrg_simulation_parameters["dtau"] * 1j,
            is_dgate=False,
            in_group=False,
        )

        for st, step in enumerate(ham_mpo):
            add_mps(arguments.output, step, folder=f"TIME_GATE_{st:02g}")

    print("Hamiltonian gates created successfully.")
