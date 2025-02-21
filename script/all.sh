#!/usr/bin/env bash

./script/cli_create_hamiltonian.py -i ./tests/example/model.toml -o /tmp/hamiltonian.h5
./script/cli_create_hamiltonian_gates.py -i tests/example/model.toml -o /tmp/hamiltonian_gates.h5
./script/cli_create_maximal_entangled_state.py -H /tmp/hamiltonian.h5 -o /tmp/2B_00.0000.h5
./script/cli_Tdmrg.py -G /tmp/hamiltonian_gates.h5 -M /tmp/2B_00.0000.h5 -o /tmp/
./script/cli_tdmrg.py -G /tmp/hamiltonian_gates.h5 -M /tmp/2B_00.0250.h5 -o /tmp/
./script/cli_mbracket.py -b /tmp/2B_00.0000.h5 -k /tmp/2B_00.0250.h5
./script/cli_mbracket.py -b /tmp/2B_00.0250.h5 -k /tmp/2B_00.0250_00.0125.h5

