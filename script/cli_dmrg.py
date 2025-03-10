#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
from pymdot.entrypoint import variational_ground_state

from pymdot.utils.general import (
    add_model_info,
    add_model_parameters,
    add_mps,
    load_model_info_model_name,
    load_model_parameters,
    load_model_state,
    load_model_zdmrg_simulation,
    load_model_info_size,
    load_mps,
)
from pymdot.utils.iotools import (
    check_filename_and_extension_h5,
    check_filename_and_extension_to_create_h5,
    create_h5,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="cli, create maximal entangled state")
    parser.add_argument(
        "-H",
        "--hamiltonian",
        type=str,
        action="store",
        help="hamiltonian path",
        required=True,
    )
    parser.add_argument(
        "-i",
        "--imps",
        type=str,
        action="store",
        help="imps path",
        required=True,
    )
    parser.add_argument(
        "-o", "--output", type=str, action="store", help="output path", required=True
    )

    arguments = parser.parse_args()

    if not check_filename_and_extension_h5(arguments.hamiltonian):
        sys.exit(
            f"cli_dmrg.py: error: the hamiltonian path {arguments.hamiltonian} is not a valid path."
        )
    if not check_filename_and_extension_to_create_h5(arguments.output):
        sys.exit(
            f"cli_dmrg.py: error: the output dirpath {os.path.dirname(arguments.output)} is not a valid directory path."
        )

    size = load_model_info_size(arguments.hamiltonian)
    model_name = load_model_info_model_name(arguments.hamiltonian)
    parameters = load_model_parameters(arguments.hamiltonian)
    zdmrg_simulation_parameters = load_model_zdmrg_simulation(arguments.hamiltonian)
    mps = load_mps(arguments.imps, size, folder="QMP")
    ham = load_mps(arguments.hamiltonian, size, folder="MPO")

    variational_ground_state(
        mps,
        ham,
        zdmrg_simulation_parameters,
    )

    create_h5(arguments.output)
    add_model_info(arguments.output, {"size": size, model_name: 0})
    add_model_parameters(arguments.output, parameters)
    add_mps(arguments.output, mps, folder="QMP")
