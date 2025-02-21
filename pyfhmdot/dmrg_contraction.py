from pyfhmdot.intense.contract import (
    contract_left_bloc_mps,
    contract_left_right_mpo_mpo_permute,
    contract_mps_mpo_mps_left_border,
    contract_mps_mpo_mps_right_border,
    contract_right_bloc_mps,
    filter_left_right,
)
from pyfhmdot.intense.mul_mp import multiply_mp
from pyfhmdot.conservation import conserve_qnum
from pyfhmdot.routine.indices import internal_qn_sub, internal_qn_sum


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


def create_two_sites_env_blocs(ham_left, ham_right, conserve_total):
    tmp_env_blocs = {}
    multiply_mp(tmp_env_blocs, ham_left, ham_right, [3], [0])
    # tmp_env_blocs
    #    2| |4
    # 0 -|___|- 5
    #    1| |3
    env_bloc = {}
    for key in tmp_env_blocs.keys():
        new_key = (0, key[1], key[3], conserve_total, 0, key[2], key[4], conserve_total)
        tmp_shape = tmp_env_blocs[key].shape
        new_shape = (1, tmp_shape[1], tmp_shape[3], 1, 1, tmp_shape[2], tmp_shape[4], 1)
        env_bloc[new_key] = (
            tmp_env_blocs[key].transpose([0, 1, 3, 2, 4, 5]).reshape(new_shape)
        )
    return env_bloc


def create_three_sites_env_blocs(ham_left, ham_middle, ham_right, conserve_total):
    tmp_tmp_env_blocs = {}
    multiply_mp(tmp_tmp_env_blocs, ham_left, ham_middle, [3], [0])
    # tmp_tmp_env_blocs
    #    2| |4
    # 0 -|___|- 5
    #    1| |3
    tmp_env_blocs = {}
    multiply_mp(tmp_env_blocs, tmp_tmp_env_blocs, ham_right, [5], [0])
    # tmp_env_blocs
    #    2| |4 |6
    # 0 -|_____ _|- 7
    #    1| |3 |5
    env_bloc = {}
    for key in tmp_env_blocs.keys():
        new_key = (
            0,
            key[1],
            key[3],
            key[5],
            conserve_total,
            0,
            key[2],
            key[4],
            key[6],
            conserve_total,
        )
        tmp_shape = tmp_env_blocs[key].shape
        new_shape = (
            1,
            tmp_shape[1],
            tmp_shape[3],
            tmp_shape[5],
            1,
            1,
            tmp_shape[2],
            tmp_shape[4],
            tmp_shape[5],
            1,
        )
        env_bloc[new_key] = (
            tmp_env_blocs[key].transpose([0, 1, 3, 5, 2, 4, 6, 7]).reshape(new_shape)
        )
    return env_bloc


def select_quantum_sector(env_bloc, position, *, size, qnum_conserved, d):
    allowed_sector_left = conserve_qnum(
        position, size=size, qnum_conserved=qnum_conserved, d=d
    )
    allowed_sector_right = conserve_qnum(
        size - position, size=size, qnum_conserved=qnum_conserved, d=d
    )
    for key in list(env_bloc.keys()):
        if not (
            internal_qn_sum(key[0], key[1]) in allowed_sector_left
            and internal_qn_sum(key[0], key[1]) == internal_qn_sum(key[4], key[5])
        ) or not (
            internal_qn_sub(key[3], key[2]) in allowed_sector_right
            and internal_qn_sub(key[3], key[2]) == internal_qn_sub(key[7], key[6])
        ):
            env_bloc.pop(key)  # quantum conserved is used here
