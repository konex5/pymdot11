# Welcome to pymdot

**pymdot** provides scientific simulations for density matrix
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
(C++) whenever it is needed using **mdot** and **mdot11**. In theory,
it could be possible to chain the dmrg simulations using the *TBB*
library (but in practice it is a very hard task).

A nice surprise was to see that mpo hamiltonian representation in such
blocs structure can induce exact diagonalization (ED) simulations as
well for spins. Enjoy!

## Simulations

- [x] T-DMRG
- [x] t-DMRG
- [ ] i-DMRG
- [ ] 0-DMRG
- [ ] t-MPS
- [ ] ED
