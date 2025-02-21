#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os

from pyfhmdot.general import (
    load_model_bdmrg_simulation,
    load_model_info_size,
    load_mps,
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

    dmps = load_mps(arguments.dmps, size, folder="QMP")
    ggate = []
    for st in range(4):
        ggate.append(load_mps(arguments.gates, size - 1, folder=f"TEMP_GATE_{st:02g}"))

    # dynamical_dmps(dmps,ggate,bdmrg_simulation_parameters)
