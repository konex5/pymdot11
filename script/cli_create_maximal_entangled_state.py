#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os

from pymdot.utils.general import (
    add_model_info,
    add_mps,
    add_state_info,
    load_model_info_model_name,
    load_model_info_size,
)
from pymdot.utils.iotools import (
    check_filename_and_extension_h5,
    check_filename_and_extension_to_create_h5,
    create_h5,
)

from pymdot.initialize import create_maximal_entangled_state

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
        "-o", "--output", type=str, action="store", help="output path", required=True
    )

    arguments = parser.parse_args()

    if not check_filename_and_extension_h5(arguments.hamiltonian):
        sys.exit(
            f"cli_create_maximal_entangled_state.py: error: the hamiltonian path {arguments.hamiltonian} is not a valid path."
        )
    if not check_filename_and_extension_to_create_h5(arguments.output):
        sys.exit(
            f"cli_create_maximal_entangled_state.py: error: the output dirpath {os.path.dirname(arguments.output)} is not a valid directory path."
        )

    size = load_model_info_size(arguments.hamiltonian)
    model_name = load_model_info_model_name(arguments.hamiltonian)
    _, dmps = create_maximal_entangled_state(size, model_name)

    create_h5(arguments.output)
    add_model_info(arguments.output, {"size": size, model_name: 0})
    add_state_info(
        arguments.output,
        {"size": size, "dw_total": 0, "chi_middle": 1, "dbeta": 0, "time": 0},
    )
    add_mps(arguments.output, dmps, folder="QMP")

    print("Maximal entangled state created successfully.")
