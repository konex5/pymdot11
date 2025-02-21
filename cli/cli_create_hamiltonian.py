#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os

from pyfhmdot.utils.iotools import (
    check_filename_and_extension_h5,
    create_h5,
    add_single_mp,
)
from pyfhmdot.utils.iodicts import check_filename_and_extension, read_dictionary

from pyfhmdot.general import (
    add_model_info,
    add_model_parameters,
    create_hamiltonian,
    load_model_info_model_name,
    load_model_info_size,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="cli, create maximal entangled state")
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
            f"cli_create_hamiltonian.py: error: the input path {arguments.input} is not a valid path."
        )
    if not check_filename_and_extension_h5(arguments.output):
        sys.exit(
            f"cli_create_hamiltonian.py: error: the output dirpath {os.path.dirname(arguments.output)} is not a valid directory path."
        )

    large_dictionary = read_dictionary(arguments.input)
    info = large_dictionary.pop("model")
    parameters = large_dictionary.pop("parameters")

    create_h5(arguments.output)
    add_model_info(arguments.output, info)
    add_model_parameters(arguments.output, parameters)
    model_name = load_model_info_model_name(arguments.output)
    size = load_model_info_size(arguments.output)
    ham_mpo = create_hamiltonian(model_name, parameters, size)
    for i, mp in enumerate(ham_mpo):
        add_single_mp(arguments.output, mp, i, folder="MPO")

    print("Hamiltonian mpo created successfully.")
