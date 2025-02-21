#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
from pyfhmdot.entrypoint import variational_ground_state

from pyfhmdot.utils.general import (
    add_model_info,
    add_mps,
    load_model_state,
    load_model_zdmrg_simulation,
    load_model_info_model_name,
    load_model_info_size,
    load_model_parameters,
)
from pyfhmdot.utils.iotools import (
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
    zdmrg_simulation_parameters = load_model_zdmrg_simulation(arguments.hamiltonian)
    mps = load_model_state(arguments.imps)
    ham = load_model_state(arguments.hamiltonian)
    
    variational_ground_state(
        mps,
        ham,
        zdmrg_simulation_parameters,
    )
