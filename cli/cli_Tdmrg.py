#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
from pyfhmdot.dynamical import dynamical_dmps

from pyfhmdot.general import (
    create_maximal_entangled_state,
    load_model_bdmrg_simulation,
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

    size = load_model_info_size(arguments.gates)
    bdmrg_simulation_parameters = load_model_bdmrg_simulation(arguments.gates)

    # dynamical_dmps(dmps,ggate,bdmrg_simulation_parameters)
