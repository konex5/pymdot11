#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
from pyfhmdot.intense.mul_mp import multiply_mp, permute_blocs
from pyfhmdot.models.pyoperators import single_operator

from pyfhmdot.utils.general import (
    add_model_info,
    add_mps,
    add_state_info,
    load_model_info_model_name,
    load_model_info_size,
    load_mps,
)
from pyfhmdot.utils.iotools import (
    check_filename_and_extension_h5,
    check_filename_and_extension_to_create_h5,
    create_h5,
)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="cli, combine operator")

    parser.add_argument(
        "-k",
        "--ket",
        type=str,
        action="store",
        help="dmps or mps path",
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
    parser.add_argument(
        "-i",
        "--position",
        type=int,
        action="store",
        help="operator position",
        required=True,
    )
    parser.add_argument(
        "-o", "--output", type=str, action="store", help="output path", required=True
    )

    arguments = parser.parse_args()

    if not check_filename_and_extension_h5(arguments.ket):
        sys.exit(
            f"cli_combine_operator.py: error: the hamiltonian path {arguments.ket} is not a valid path."
        )

    if not check_filename_and_extension_to_create_h5(arguments.output):
        sys.exit(
            f"cli_create_maximal_entangled_state.py: error: the output dirpath {os.path.dirname(arguments.output)} is not a valid directory path."
        )

    size = load_model_info_size(arguments.ket)
    if arguments.position > size:
        sys.exit(
            f"cli_combine_operator.py: error: the position {arguments.position} can not be greater than {size}."
        )
    elif arguments.position < 1:
        sys.exit(
            f"cli_combine_operator.py: error: the position {arguments.position} can not be smaller than 1."
        )

    model_name = load_model_info_model_name(arguments.ket)
    head, _, tail = model_name.split("_")
    op_head, _, op_tail = arguments.name.split("_")

    if op_head != head and op_tail != tail:
        sys.exit(
            f"cli_combine_operator.py: error: the operator name {arguments.name} has wrong prefix or sufix."
        )

    operator = single_operator(arguments.name, 1.0)
    ket_dmps = load_mps(arguments.ket, size, folder="QMP")

    if len(list(ket_dmps[0].values())[0].shape) == 4:
        new_mp = {}
        multiply_mp(new_mp, operator, ket_dmps[arguments.position - 1], [0], [2])
        #    0|
        #  1-|_|-3
        #    2|
        new_dst = {}
        permute_blocs(new_dst, new_mp, [(0, 1, 2, 3), (2, 0, 1, 3)])

        ket_dmps[arguments.position - 1].clear()
        ket_dmps[arguments.position - 1] = new_dst
        # no update indices required since we only sum the indices.

    else:
        new_mp = {}
        multiply_mp(new_mp, operator, ket_dmps[arguments.position - 1], [0], [1])
        #    0|
        #  1-|_|-2
        new_dst = {}
        permute_blocs(new_dst, new_mp, [(0, 1, 2), (1, 0, 2)])

        ket_dmps[arguments.position - 1].clear()
        ket_dmps[arguments.position - 1] = new_dst
        # TODO Sp, Sm requires to increase, lower all the following blocks
        # update_indices(ket_dmps,arguments.position,operator)

    create_h5(arguments.output)
    add_model_info(arguments.output, {"size": size, model_name: 0})
    add_state_info(
        arguments.output,
        {
            "size": size,
            "dw_total": 0,
            "chi_middle": 1,
            "dbeta": 0,
            "time": 0,
            arguments.name: arguments.position,
        },
    )
    add_mps(arguments.output, ket_dmps, folder="QMP")

    print("Operator was applied on state. Results created successfully.")
