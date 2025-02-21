#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import toml

from pyfhmdot.utils.iotools import *
from pyfhmdot.utils.iodicts import *

from pyfhmdot.general import create_model_info, create_hamiltonian

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

    if check_filename_and_extension(arguments.input):
        sys.exit(
            f"cli_create_hamiltonian.py: error: the hamiltonian path {arguments.input} is not a valid path."
        )
    if not check_filename_and_extension_h5(arguments.output):
        sys.exit(
            f"cli_create_hamiltonian.py: error: the output dirpath {os.path.dirname(arguments.output)} is not a valid directory path."
        )

    large_dictionary = read_dictionary(arguments.input)
    info = large_dictionary.pop("model")
    parameters = large_dictionary.pop("parameters")
    
    # ham_mpo, ggdgate_db, ggsgate_dt, ggdgate_dt = create_hamiltonian(info["model_name"],parameters,info["size"],info_sim["dbeta"],info_sim["dtime"])
    create_h5(arguments.output)

    """
    hdf5_create_mpo(output, mpo, coefsite, modeldict, info, sim_TDMRG, "TDMRG")

    if not os.path.exists(output.split("2B_")[0] + "2B.lock"):
        addlocker_write_beta(output)

    """
    print("Maximal entangled state created successfully.")
