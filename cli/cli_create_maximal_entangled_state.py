#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os

from pyfhmdot.general import (
    create_maximal_entangled_state,
    load_model_info_model_name,
    load_model_info_size,
)
from pyfhmdot.utils.iotools import (
    add_single_mp,
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
        "-o", "--output", type=str, action="store", help="output path", required=True
    )
    # args=["-H","/tmp/hamiltonian.h5","-o","/tmp/2B_00.0000.h5"])
    arguments = parser.parse_args()

    if not check_filename_and_extension_h5(arguments.hamiltonian):
        sys.exit(
            f"cli_create_maximal_entangled_state.py: error: the hamiltonian path {arguments.hamiltonian} is not a valid path."
        )
    if not check_filename_and_extension_to_create_h5:
        sys.exit(
            f"cli_create_maximal_entangled_state.py: error: the output dirpath {os.path.dirname(arguments.output)} is not a valid directory path."
        )

    size = load_model_info_size(arguments.hamiltonian)
    model_name = load_model_info_model_name(arguments.hamiltonian)
    _, dmps = create_maximal_entangled_state(size, model_name)

    create_h5(arguments.output)
    for i, mp in enumerate(dmps):
        add_single_mp(arguments.output, mp, i, folder="QMP")

    print("Maximal entangled state created successfully.")
