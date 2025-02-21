#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
from pyfhmdot.dynamical import dynamical_dmps

from pyfhmdot.general import (
    add_model_bdmrg_simulation,
    add_model_info,
    add_mps,
    load_model_bdmrg_simulation,
    load_model_info_model_name,
    load_model_info_size,
    load_mps,
    change_right_index,
)
from pyfhmdot.intense.splitgroup import group_dmps, group_four_dgate, split_dmps
from pyfhmdot.utils.iotools import (
    check_filename_and_extension_h5,
    create_h5,
)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="cli, run Tdmrg simulation")
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

    if not check_filename_and_extension_h5(arguments.gates):
        sys.exit(
            f"cli_Tdmrg.py: error: the hamiltonian path {arguments.gates} is not a valid path."
        )
    if not check_filename_and_extension_h5(arguments.dmps):
        sys.exit(
            f"cli_Tdmrg.py: error: the hamiltonian path {arguments.dmps} is not a valid path."
        )
    if not os.path.exists(os.path.dirname(arguments.output)):
        sys.exit(
            f"cli_Tdmrg.py: error: the output dirpath {os.path.dirname(arguments.output)} is not a valid directory path."
        )

    size = load_model_info_size(arguments.gates)
    model_name = load_model_info_model_name(arguments.gates)
    bdmrg_simulation_parameters = load_model_bdmrg_simulation(arguments.gates)

    tmp_dmps = load_mps(arguments.dmps, size, folder="QMP")
    dmps = []
    for i, tmp in enumerate(tmp_dmps):
        _ = {}
        group_dmps(model_name, _, tmp)
        dmps.append(_)

    ggate = []
    for st in range(4):
        ggate.append(load_mps(arguments.gates, size - 1, folder=f"TEMP_GATE_{st:02g}"))

    dynamical_dmps(dmps, ggate, bdmrg_simulation_parameters)

    dmps_out = []
    for i, tmp in enumerate(dmps):
        _ = {}
        split_dmps(model_name, _, tmp)
        dmps_out.append(_)

    output_path = arguments.output + "/2B_00.0250.h5"
    create_h5(output_path)
    add_model_info(output_path,{model_name:0,"size":size})
    add_model_bdmrg_simulation(output_path, bdmrg_simulation_parameters)
    add_mps(output_path, dmps_out, folder="QMP")
