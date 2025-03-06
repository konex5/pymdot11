#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os

from pymdot.utils.general import (
    load_model_info_model_name,
    load_model_info_size,
    load_mps,
)
from pymdot.utils.iotools import check_filename_and_extension_h5

from pymdot.intense.interface import (
    measure_dmps_mpo_dmps,
    measure_dmps_mpo_mpo_dmps,
    measure_mps_mpo_mpo_mps,
    measure_mps_mpo_mps,
)
from pymdot.models.pyoperators import operator_mpo

from numpy import mean


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="cli, measure average")
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
        "-n",
        "--name",
        type=str,
        action="store",
        help="operator name",
        required=True,
    )

    arguments = parser.parse_args()

    if not check_filename_and_extension_h5(arguments.bra):
        sys.exit(
            f"cli_maverage.py: error: the hamiltonian path {arguments.bra} is not a valid path."
        )
    if not check_filename_and_extension_h5(arguments.ket):
        sys.exit(
            f"cli_maverage.py: error: the hamiltonian path {arguments.ket} is not a valid path."
        )

    size = load_model_info_size(arguments.bra)
    if size != load_model_info_size(arguments.ket):
        sys.exit(f"cli_maverage.py: error: bra and ket have different sizes.")

    model_name = load_model_info_model_name(arguments.ket)
    head, _, tail = model_name.split("_")
    op_head = arguments.name.split("_")[0]
    op_tail = arguments.name.split("_")[-1]

    if op_head != head and op_tail != tail:
        sys.exit(
            f"cli_maverage.py: error: the operator name {arguments.name} has wrong prefix or sufix."
        )

    ket_dmps = load_mps(arguments.ket, size, folder="QMP")
    bra_dmps = load_mps(arguments.bra, size, folder="QMP")

    if (
        len(list(bra_dmps[0].values())[0].shape) == 4
        and len(list(ket_dmps[0].values())[0].shape) == 4
    ):
        average = []
        if "-" in arguments.name:
            for l in range(size - 1):
                average.append(
                    measure_dmps_mpo_dmps(
                        bra_dmps,
                        operator_mpo(arguments.name, 1.0, position=l + 1, size=size),
                        ket_dmps,
                    )
                )
        else:
            for l in range(size):
                average.append(
                    measure_dmps_mpo_dmps(
                        bra_dmps,
                        operator_mpo(arguments.name, 1.0, position=l + 1, size=size),
                        ket_dmps,
                    )
                )

    if (
        len(list(bra_dmps[0].values())[0].shape) == 3
        and len(list(ket_dmps[0].values())[0].shape) == 3
    ):
        pass

    print(f"<bra|A|ket>= {average}")
    print(f"1/N sum <bra|A|ket>= {mean(average)}")
