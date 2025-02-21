# Welcome to pyfhmdot

**mdot** is a simple python project for dmrg and exact diagonalisation.

It is mainly a high level library. When it uses **fmd** it is already
faster but optimaly, one would need to stay in C++.

The library purpose is to code fast with the option of returning to
lower level whenever it is needed.

# Todo list

hamiltonian.toml
operator.toml

* infinite DMRG (add single/double site)
  idmrg -H hamiltonian.txt > infinite.mps
  
** TODO double site
* variational ground state (single/double site, lanczos/bsomething, longer range interaction to 4 site, keeping or growing chi)
** TODO single site lanczos, nearest neighbor interaction
   dmrg -H hamiltonian.txt < infinite.mps > zero.mps
   
* differential evolution (real/complex, pure/mixed)
** TODO normalized hermitian gate application
   tdmrg -H hamiltonian.txt < zero.mps > time.mps
   Tdmrg -H hamiltonian.txt > temperature.mpo
   tdmrg -H hamiltonian.txt < state.mpo > zero.mpo

* measurement
  mbraket -mpsA -mpsB
  mtrace -mpo
  mtrace -mpoA -mpoB
  # mentangle
  menergie -mpsA -H hamiltonian.txt -mpsB
  menergie -mpo -H hamiltonian.txt
  menergie -mpoA -H hamiltonian.txt -mpoB
  maverage -mpsA --input operator_info.txt -mpsB
  maverage -mpo --input operator_info.txt
  maverage -mpoA --input operator_info.txt -mpoB
  mcorr -mpsA --inputA operator_infoA.txt --inputB operator_infoB.txt -mpsB
  mcorr -mpo --inputA operator_infoA.txt --inputB operator_infoB.txt
  mcorr -mpoA --inputA operator_infoA.txt --inputB operator_infoB.txt -mpoB
  
    ```hamiltonian.txt static-compile-time
    * infinite DMRG
    N=13, inf
    single=false
    single_trunk=10**-10
    chi=2200,1000,400

    * zero DMRG
    sinle=true
    lanczos=true
    lanczos_trunk=10**-10
    single_trunk=10**-12
    chi=3000,1500,800
    
    * t DMRG
    nearest_neighbor=true
    single_trunk=10**-16
    integrated_trunk=10**-8
    chi=3000,1500,800
    deltat=0.01
    
    * T DMRG
    N=12
    nearest_neighbor=true
    single_trunk=10**-16
    integrated_trunk=10**-8
    chi=3000,1500,800
    deltaB=0.01  
    ```
