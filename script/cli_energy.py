#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os

from pyfhmdot.utils.general import (
    load_model_info_size,
    load_mps,
)
from pyfhmdot.utils.iotools import check_filename_and_extension_h5

from pyfhmdot.intense.interface import measure_dmps_mpo_dmps, measure_dmps_mpo_mpo_dmps


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="cli, measure energy")
    parser.add_argument(
        "-b",
        "--bra",
        type=str,
        action="store",
        help="gates path",
        required=True,
    )
    parser.add_argument(
        "-k",
        "--ket",
        type=str,
        action="store",
        help="hamiltonian path",
        required=True,
    )
    parser.add_argument(
        "-H",
        "--hamiltonian",
        type=str,
        action="store",
        help="hamiltonian path",
        required=True,
    )

    arguments = parser.parse_args()

    if not check_filename_and_extension_h5(arguments.bra):
        sys.exit(
            f"cli_menergie.py: error: the hamiltonian path {arguments.bra} is not a valid path."
        )
    if not check_filename_and_extension_h5(arguments.ket):
        sys.exit(
            f"cli_menergie.py: error: the hamiltonian path {arguments.ket} is not a valid path."
        )
    if not check_filename_and_extension_h5(arguments.hamiltonian):
        sys.exit(
            f"cli_menergie.py: error: the hamiltonian path {arguments.hamiltonian} is not a valid path."
        )

    size = load_model_info_size(arguments.bra)
    if size != load_model_info_size(arguments.ket) or size != load_model_info_size(
        arguments.hamiltonian
    ):
        sys.exit(
            f"cli_menergie.py: error: bra, ket or hamiltonian have different sizes."
        )

    ket_dmps = load_mps(arguments.ket, size, folder="QMP")
    bra_dmps = load_mps(arguments.bra, size, folder="QMP")
    ham_mpo = load_mps(arguments.hamiltonian, size, folder="MPO")

    energy = measure_dmps_mpo_dmps(ket_dmps, ham_mpo, bra_dmps)
    print(f"<bra|H|ket>= {energy}")
    hsquare = measure_dmps_mpo_mpo_dmps(ket_dmps, ham_mpo, ham_mpo, bra_dmps)
    print(f"<bra|H^2|ket>= {hsquare}")
    print(f"<bra|(H-E)^2|ket>= {hsquare-energy**2}")
