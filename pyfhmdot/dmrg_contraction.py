from pyfhmdot.intense.contract import (
    contract_left_bloc_mps,
    contract_left_right_mpo_mpo_permute,
    contract_mps_mpo_mps_left_border,
    contract_mps_mpo_mps_right_border,
    contract_right_bloc_mps,
    filter_left_right,
)


def create_env_blocs(bloc_left, ham_mpo_left, ham_mpo_right, bloc_right):
    env_bloc = {}
    contract_left_right_mpo_mpo_permute(
        env_bloc, bloc_left, ham_mpo_left, ham_mpo_right, bloc_right
    )
    return env_bloc


def update_left(mps, ham, left, is_border=False):
    new_bloc_left = {}
    if is_border:
        contract_mps_mpo_mps_left_border(new_bloc_left, mps, ham, mps)
    else:
        contract_left_bloc_mps(new_bloc_left, left, mps, ham, mps)
    filter_left_right(new_bloc_left)

    return new_bloc_left


def update_right(mps, ham, right, is_border=False):
    new_bloc_right = {}
    if is_border:
        contract_mps_mpo_mps_right_border(new_bloc_right, mps, ham, mps)
    else:
        contract_right_bloc_mps(new_bloc_right, right, mps, ham, mps)
    filter_left_right(new_bloc_right)
    return new_bloc_right
