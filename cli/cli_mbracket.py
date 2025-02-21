#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
from pyfhmdot.intense.interface import measure_dmps

from pyfhmdot.general import (
    add_model_bdmrg_simulation,
    add_mps,
    load_model_bdmrg_simulation,
    load_model_info_model_name,
    load_model_info_size,
    load_mps,
    change_right_index,
)
from pyfhmdot.intense.splitgroup import group_dmps, group_four_dgate
from pyfhmdot.utils.iotools import (
    check_filename_and_extension_h5,
    create_h5,
)


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
    # parser.add_argument(
    #     "-o", "--output", type=str, action="store", help="output path", required=True
    # )

    arguments = parser.parse_args()

    if not check_filename_and_extension_h5(arguments.bra):
        sys.exit(
            f"cli_mbracket.py: error: the hamiltonian path {arguments.bra} is not a valid path."
        )
    if not check_filename_and_extension_h5(arguments.ket):
        sys.exit(
            f"cli_mbracket.py: error: the hamiltonian path {arguments.ket} is not a valid path."
        )
    # if not os.path.exists(os.path.dirname(arguments.output)):
    #     sys.exit(
    #         f"cli_Tdmrg.py: error: the output dirpath {os.path.dirname(arguments.output)} is not a valid directory path."
    #     )

    size = load_model_info_size(arguments.bra)
    if size == load_model_info_size(arguments.ket):
        pass

    bra_dmps = load_mps(arguments.bra, size, folder="QMP")
    ket_dmps = load_mps(arguments.ket, size, folder="QMP")
    
    bra_norm = measure_dmps(bra_dmps)
    print(f"{bra_norm}")
    ket_norm = measure_dmps(ket_dmps)
    print(f"{ket_norm}")    
    # bra_dnorm = measure_dmps_dmps(bra_dmps,bra_dmps)
    # ket_dnorm = measure_dmps_dmps(bra_dmps)
