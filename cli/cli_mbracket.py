#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
from pyfhmdot.dynamical import dynamical_dmps

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
        "-l",
        "--left",
        type=str,
        action="store",
        help="gates path",
        required=True,
    )
    parser.add_argument(
        "-r",
        "--right",
        type=str,
        action="store",
        help="hamiltonian path",
        required=True,
    )
    # parser.add_argument(
    #     "-o", "--output", type=str, action="store", help="output path", required=True
    # )

    arguments = parser.parse_args()

    if not check_filename_and_extension_h5(arguments.left):
        sys.exit(
            f"cli_mbracket.py: error: the hamiltonian path {arguments.left} is not a valid path."
        )
    if not check_filename_and_extension_h5(arguments.right):
        sys.exit(
            f"cli_mbracket.py: error: the hamiltonian path {arguments.right} is not a valid path."
        )
    # if not os.path.exists(os.path.dirname(arguments.output)):
    #     sys.exit(
    #         f"cli_Tdmrg.py: error: the output dirpath {os.path.dirname(arguments.output)} is not a valid directory path."
    #     )

    size = load_model_info_size(arguments.left)
    if size == load_model_info_size(arguments.right):
        pass

    tmp_dmps = load_mps(arguments.left, size, folder="QMP")
    tmp_dmps = load_mps(arguments.right, size, folder="QMP")
    # dmps = []
    # for i, tmp in enumerate(tmp_dmps):
    #     _ = {}
    #     group_dmps(model_name, _, tmp)
    #     if i == size - 1:
    #         _ = change_right_index(_, 2 * size)
    #     dmps.append(_)
