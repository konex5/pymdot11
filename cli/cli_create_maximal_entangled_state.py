# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

import argparse
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


# from pyfhmdot.general import getargs_maximal_entangled_state, create_maximal_entangled_state

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="cli, create maximal entangled state")
    parser.add_argument(
        "-H",
        "--hamiltonian",
        type=str,
        action="store",
        help="hamiltonian path",
        required=True,
    )
    parser.add_argument(
        "-o", "--output", type=str, action="store", help="output path", required=True
    )
    # args=["-H","/tmp/hamiltonian.h5","-o","/tmp/2B_00.0000.h5"])
    arguments = parser.parse_args()

    if not os.path.exists(arguments.hamiltonian):
        sys.exit(
            f"cli_create_maximal_entangled_state.py: error: the hamiltonian path {arguments.hamiltonian} is not a valid path."
        )
    if not os.path.exists(os.path.dirname(arguments.output)):
        sys.exit(
            f"cli_create_maximal_entangled_state.py: error: the output dirpath {os.path.dirname(arguments.output)} is not a valid directory path."
        )

    # coefsite, mpo, info, sim_TDMRG = create_maximal_entangled_state(size=size,qname='sh_id_no')

    """
    modeldict, output = getArgs_create_maximal_entangled_state(argvals)

    manybody.models.quantum_name = modeldict["quantum_name"]

    coefsite, mpo, info, sim_TDMRG = main_create_maximal_entangled_state(
        modeldict["qnmodel"], modeldict["L"]
    )

    hdf5_create_mpo(output, mpo, coefsite, modeldict, info, sim_TDMRG, "TDMRG")

    if not os.path.exists(output.split("2B_")[0] + "2B.lock"):
        addlocker_write_beta(output)

    print("Maximal entangled state created!")
    """
