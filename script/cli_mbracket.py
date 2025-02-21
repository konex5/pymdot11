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

from pyfhmdot.intense.interface import measure_dmps, measure_dmps_dmps, measure_mps_mps


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="cli, run Tdmrg simulation")
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

    arguments = parser.parse_args()

    if not check_filename_and_extension_h5(arguments.bra):
        sys.exit(
            f"cli_mbracket.py: error: the hamiltonian path {arguments.bra} is not a valid path."
        )
    if not check_filename_and_extension_h5(arguments.ket):
        sys.exit(
            f"cli_mbracket.py: error: the hamiltonian path {arguments.ket} is not a valid path."
        )

    size = load_model_info_size(arguments.bra)
    if size != load_model_info_size(arguments.ket):
        sys.exit(f"cli_mbracket.py: error: bra and ket have different sizes.")

    bra_dmps = load_mps(arguments.bra, size, folder="QMP")
    ket_dmps = load_mps(arguments.ket, size, folder="QMP")

    if (
        len(list(bra_dmps[0].values())[0].shape) == 4
        and len(list(ket_dmps[0].values())[0].shape) == 4
    ):
        bra_norm = measure_dmps(bra_dmps)
        print(f"Tr(rho_bra)= {bra_norm}")
        ket_norm = measure_dmps(ket_dmps)
        print(f"Tr(rho_ket)= {ket_norm}")
        bra_dnorm = measure_dmps_dmps(bra_dmps, bra_dmps)
        print(f"<<rho_bra|rho_bra>>= {bra_dnorm}")
        ket_dnorm = measure_dmps_dmps(ket_dmps, ket_dmps)
        print(f"<<rho_ket|rho_ket>>= {ket_dnorm}")
        braket_dnorm = measure_dmps_dmps(bra_dmps, ket_dmps)
        print(f"<<rho_bra|rho_ket>>= {braket_dnorm}")

    if (
        len(list(bra_dmps[0].values())[0].shape) == 3
        and len(list(ket_dmps[0].values())[0].shape) == 3
    ):
        # bra_norm = measure_mps_mps(bra_dmps,bra_dmps)
        # print(f"{bra_norm}")
        # ket_norm = measure_dmps(ket_dmps)
        # print(f"{ket_norm}")
        # braket_norm = measure_mps_mps(bra_mps,ket_mps)
        # print(f"{braket_norm}")
        pass
