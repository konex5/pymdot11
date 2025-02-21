# Welcome to pyfhmdot (Fast Hilbert Matrix DOT)

**pyfhmdot** provides scientific simulations for density matrix
renormalization group (DMRG) on spins.

From our knowledge, this is the only library providing such
simulations based on quantum numbers without any quantum number
representation. How? When _S^z_tot_ is conserved, it mainly says that
quantum sectors are following a sum of _S^z_i_ which translates in
"indices of blocs simply sums"! For fermions or hardcore bosons, we
can map them on spins with small costs -- and I never understood how
to implement it in fermion representation to be honest.

The advantage of removal of quantum numbers representation is to be
much closer to the computer world so the reshuffling of quantum
sectors are now avoided. In theory, the blocs could even be statically
allocated (but in practice it is a very hard task -- better use a
simple hashmap for the blocs at runtime).

The library purpose is to be able to return to low level languages
(C++) whenever it is needed using **mdot** and **pymdot**. In theory,
it could be possible to chain the dmrg simulations using the __TBB__
library (but in practice it is a very hard task).

A nice surprise was to see that mpo hamiltonian representation in such
blocs structure can induce exact diagonalization (ED) simulations as
well for spins. Enjoy!

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
