from mdot_routine import minimize_lanczos_on_m, minimize_lanczos_on_mm
from pyfhmdot.intense.contract import (
    contract_left_right_bloc_with_mpo,
    contract_left_right_mpo_mpo_permute,
)
from pyfhmdot.routine.interface import mm_to_theta_no_gate, theta_to_mm
from numpy import all as _all


def minimize_lanczos_and_move(
    l,
    mps,
    ham,
    left_right,
    max_iteration,
    tolerance,
    chi_max,
    eps,
    *,
    direction_right,
    is_um
):
    env_blocs = {}
    contract_left_right_mpo_mpo_permute(
        env_blocs, left_right[l - 2], ham[l - 1], ham[l], left_right[l]
    )
    th_blocs = {}
    mm_to_theta_no_gate(
        dst_blocs=th_blocs,
        lhs_blocs=mps[l - 1],
        rhs_blocs=mps[l],
        conserve_left_right=False,
    )
    # for key in list(th_blocs.keys()):
    #     if _all(th_blocs[key] == 0):
    #         th_blocs.pop(key)

    # for key in list(env_blocs.keys()):
    #     fst_key = (key[0], key[1], key[2], key[3])
    #     snd_key = (key[4], key[5], key[6], key[7])
    #     if fst_key not in th_blocs.keys() and snd_key not in th_blocs.keys():
    #         env_blocs.pop(key)

    new_th_blocs = minimize_lanczos_on_mm(env_blocs, th_blocs, max_iteration, tolerance)
    mps[l - 1].clear()
    mps[l].clear()
    theta_to_mm(
        theta_blocs=new_th_blocs,
        lhs_blocs=mps[l - 1],
        rhs_blocs=mps[l],
        dw_dict={"dw_one_serie": 0},
        chi_max=chi_max,
        normalize=True,
        direction_right=direction_right,
        eps=eps,
        is_um=is_um,
    )


def minimize_lanczos(l, mps, ham, left_right, max_iteration, tolerance):
    env_bloc = {}
    contract_left_right_bloc_with_mpo(
        env_bloc, left_right[l - 1], ham[l], left_right[l]
    )
    # for key in list(env_bloc.keys()):
    #     tmp_shape = env_bloc[key].shape
    #     if tmp_shape[0] != tmp_shape[3] and tmp_shape[2] != tmp_shape[5]:
    #         env_bloc.pop(key)

    # for key in env_bloc.keys():
    #     tmp_shape = env_bloc[key].shape
    #     if (key[0],key[1],key[2]) in mps[l].keys():
    #         if mps[l][(key[0],key[1],key[2])].shape != (tmp_shape[0], tmp_shape[1], tmp_shape[2]):
    #             mps[l].pop((key[0],key[1],key[2]))

    mps[l] = minimize_lanczos_on_m(env_bloc, mps[l], 100, tolerance)
