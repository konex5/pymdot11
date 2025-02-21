from mdot_routine import minimize_lanczos_on_m
from pyfhmdot.intense.contract import contract_left_right_bloc_with_mpo


def minimize_lanczos(l, mps, ham, left_right, max_iteration, tolerance):
    env_bloc = {}
    contract_left_right_bloc_with_mpo(env_bloc, left_right[l - 1], ham[l], left_right[l])
    mps[l] = minimize_lanczos_on_m(env_bloc, mps[l], 100, tolerance)
