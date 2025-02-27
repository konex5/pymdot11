#!/usr/bin/env bash

./script/cli_create_hamiltonian.py -i ./tests/example/model.toml -o /tmp/hamiltonian.h5
./script/cli_create_hamiltonian_gates.py -i tests/example/model.toml -o /tmp/hamiltonian_gates.h5

echo "BETA TEMPERATURE"
./script/cli_create_maximal_entangled_state.py -H /tmp/hamiltonian.h5 -o /tmp/2B_00.0000.h5
./script/cli_Tdmrg.py -G /tmp/hamiltonian_gates.h5 -M /tmp/2B_00.0000.h5 -o /tmp/
./script/cli_tdmrg.py -G /tmp/hamiltonian_gates.h5 -M /tmp/2B_00.0250.h5 -o /tmp/
mkdir -p /tmp/2B_00.0250_sz_0005/
./script/cli_combine_operator.py -k /tmp/2B_00.0250.h5 -i 5 -n sh_sz_u1 -o /tmp/2B_00.0250_sz_0005/t_00.0000.h5
mkdir -p /tmp/2B_00.0000_sz_0005/
./script/cli_combine_operator.py -k /tmp/2B_00.0000.h5 -i 5 -n sh_sz_u1 -o /tmp/2B_00.0000_sz_0005/t_00.0000.h5
./script/cli_tdmrg.py -G /tmp/hamiltonian_gates.h5 -M /tmp/2B_00.0250_sz_0005/t_00.0000.h5 -o /tmp/2B_00.0250_sz_0005/

./script/cli_mbracket.py -b /tmp/2B_00.0000.h5 -k /tmp/2B_00.0250.h5
echo "2B_00.0250"
./script/cli_mbracket.py -b /tmp/2B_00.0250.h5 -k /tmp/2B_00.0250.h5
echo "2B_00.0500"
./script/cli_mbracket.py -b /tmp/2B_00.0500.h5 -k /tmp/2B_00.0500.h5
./script/cli_mbracket.py -b /tmp/2B_00.0250.h5 -k /tmp/2B_00.0250_t_00.0250.h5

echo "observables"
./script/cli_mbracket.py -b /tmp/2B_00.0250_sz_0005/t_00.0000.h5 -k /tmp/2B_00.0250_sz_0005/t_00.0000.h5
./script/cli_mbracket.py -b /tmp/2B_00.0000_sz_0005/t_00.0000.h5 -k /tmp/2B_00.0000.h5

./script/cli_maverage.py -b /tmp/2B_00.0500.h5 -k /tmp/2B_00.0500.h5 -n sh_sz_u1
./script/cli_maverage.py -b /tmp/2B_00.0500.h5 -k /tmp/2B_00.0500.h5 -n sh_sz_u1-sh_sz_u1

echo "correlation"
./script/cli_maverage.py -b /tmp/2B_00.0250_sz_0005/t_00.0000.h5 -k /tmp/2B_00.0250.h5 -n sh_sz_u1

echo "energies"
./script/cli_energy.py -b /tmp/2B_00.0000.h5 -k /tmp/2B_00.0000.h5 -H /tmp/hamiltonian.h5
./script/cli_energy.py -b /tmp/2B_00.0250.h5 -k /tmp/2B_00.0250.h5 -H /tmp/hamiltonian.h5


echo "ZERO TEMPERATURE"
./script/cli_idmrg.py -H /tmp/hamiltonian.h5 -o /tmp/2B_inf.h5
./script/cli_dmrg.py -H /tmp/hamiltonian.h5 -i /tmp/2B_inf.h5 -o /tmp/2B_inf_01.h5
mkdir -p /tmp/2B_inf_01_sz_0005
./script/cli_combine_operator.py -k /tmp/2B_inf_01.h5 -i 5 -n sh_sz_u1 -o /tmp/2B_inf_01_sz_0005/t_00.0000.h5

echo "energies"
./script/cli_energy.py -b /tmp/2B_inf.h5 -k /tmp/2B_inf.h5 -H /tmp/hamiltonian.h5
./script/cli_energy.py -b /tmp/2B_inf_01.h5 -k /tmp/2B_inf_01.h5 -H /tmp/hamiltonian.h5
mkdir -p /tmp/2B_inf_01_sz_0005/
./script/cli_combine_operator.py -k /tmp/2B_inf_01.h5 -i 5 -n sh_sz_u1 -o /tmp/2B_inf_01_sz_0005/t_00.0000.h5
./script/cli_tmps.py -G /tmp/hamiltonian_gates.h5 -M /tmp/2B_inf_01_sz_0005/t_00.0000.h5 -o /tmp/2B_inf_01_0000/
