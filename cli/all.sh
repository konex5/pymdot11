#!/usr/bin/env bash


./cli/cli_create_hamiltonian.py -i ./tests/example/model.toml -o /tmp/hamiltonian.h5
./cli/cli_create_hamiltonian_gates.py -i tests/example/model.toml -o /tmp/hamiltonian_gates.h5

./cli/cli_create_maximal_entangled_state.py -H /tmp/hamiltonian.h5 -o /tmp/2B_00.0000.h5
