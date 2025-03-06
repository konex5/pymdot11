from pymdot.intense.contract import (
    contract_left_right_bloc_with_mpo,
    contract_left_right_mpo_mpo_permute,
)
from pymdot.routine.interface import mm_to_theta_no_gate, theta_to_mm
from pymdot.algorithm import apply_mm_at
from numpy import all as _all

from pymdot.dmrg_contraction import update_left, update_right


def minimize_on_mm(env_blocs, th_blocs, max_iteration, tolerance, *, driver):
    if driver == "lanczos":
        from mdot_routine import minimize_lanczos_on_mm

        new_th_blocs = minimize_lanczos_on_mm(
            env_blocs, th_blocs, max_iteration, tolerance
        )
    elif driver == "jacobi":
        # from mdot_routine import minimize_jacobi_on_mm
        pass
    elif driver == "scipy":
        from pymdot.routine.eig_routine import minimize_scipy_on_mm

        new_th_blocs = minimize_scipy_on_mm(
            env_blocs, th_blocs, max_iteration, tolerance
        )
    else:
        raise ValueError("The driver value is either 'lanczos', 'jacobi' or 'scipy'.")
    return new_th_blocs


def minimize_and_move(
    l,
    mps,
    ham,
    left_right,
    max_iteration,
    tolerance,
    chi_max,
    normalize,
    eps,
    *,
    direction_right,
    is_um,
    driver="lanczos",
):
    if direction_right == 1:
        apply_mm_at(
            mps,
            l,
            {"dw_one_serie": 0},
            chi_max,
            normalize,
            eps,
            is_um=True,
            direction_right=1,
        )
        if l == 1:
            left_right[l - 1] = update_left(mps[l - 1], ham[l - 1], [None], True)
        else:
            left_right[l - 1] = update_left(
                mps[l - 1], ham[l - 1], left_right[l - 2], False
            )
    else:
        apply_mm_at(
            mps,
            l + 2,
            {"dw_one_serie": 0},
            chi_max,
            normalize,
            eps,
            is_um=False,
            direction_right=-1,
        )
        if l == len(mps) - 3:
            left_right[l + 1] = update_right(mps[l + 2], ham[l + 2], [None], True)
        else:
            left_right[l + 1] = update_right(
                mps[l + 2], ham[l + 2], left_right[l + 2], False
            )

    env_blocs = {}
    contract_left_right_mpo_mpo_permute(
        env_blocs, left_right[l - 1], ham[l], ham[l + 1], left_right[l + 1]
    )
    th_blocs = {}
    mm_to_theta_no_gate(
        dst_blocs=th_blocs,
        lhs_blocs=mps[l],
        rhs_blocs=mps[l + 1],
        conserve_left_right=False,
    )
    valid_keys = []
    for key in list(env_blocs.keys()):
        fst_key = (key[0], key[1], key[2], key[3])
        snd_key = (key[4], key[5], key[6], key[7])
        if (
            fst_key not in th_blocs.keys()
            or fst_key != snd_key
            or fst_key[0] + fst_key[1] + fst_key[2] != fst_key[3]
        ):
            env_blocs.pop(key)
        else:
            valid_keys.append(fst_key)
    for key in list(th_blocs.keys()):
        if key not in valid_keys:
            th_blocs.pop(key)

    new_th_blocs = minimize_on_mm(
        env_blocs, th_blocs, max_iteration, tolerance, driver=driver
    )
    mps[l].clear()
    mps[l + 1].clear()
    theta_to_mm(
        theta_blocs=new_th_blocs,
        lhs_blocs=mps[l],
        rhs_blocs=mps[l + 1],
        dw_dict={"dw_one_serie": 0},
        chi_max=chi_max,
        normalize=normalize,
        direction_right=direction_right,
        eps=eps,
        is_um=is_um,
    )
