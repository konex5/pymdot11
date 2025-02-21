#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os

from pyfhmdot.utils.general import (
    add_model_info,
    add_mps,
    load_model_info_model_name,
    load_model_info_size,
)
from pyfhmdot.utils.iotools import (
    check_filename_and_extension_h5,
    check_filename_and_extension_to_create_h5,
    create_h5,
)

from pyfhmdot.create import create_maximal_entangled_state

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
    # args=["-H","/tmp/hamiltonian.h5","-o","/tmp/2B_00.0000.h5"])
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
    add_mps(arguments.output, dmps, folder="QMP")

    print("Maximal entangled state created successfully.")
