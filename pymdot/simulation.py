"""simulation.py"""

from pymdot.algorithm import apply_mm_at, apply_gate_on_mm_at
from copy import deepcopy as _copy
from pymdot.conservation import conserve_qnum
from pymdot.initialize import finalize_idmrg_even_size

from pymdot.routine.eig_routine import minimize_theta_with_scipy as minimize_theta
from pymdot.routine.eig_routine import apply_eigenvalues
from pymdot.routine.interface import theta_to_mm
from pymdot.dmrg_contraction import (
    create_env_blocs,
    select_quantum_sector,
    update_left,
    update_right,
)
from pymdot.routine.minimize import (
    minimize_and_move as _minimize_and_move,
    minimize_on_mm,
)


def sweep(size, *, from_site=None, to_site=None):
    if from_site is None:
        from_site = 1
    if to_site is None:
        to_site = size
    if from_site < to_site:  # go right
        for _ in range(from_site, to_site, 1):
            yield _
    else:
        for _ in range(from_site, to_site - 1, -1):
            yield _


def print_single(size, site_i):
    return "\r" + "".join(
        ["A" for _ in range(1, site_i, 1)]
        + ["*"]
        + ["B" for _ in range(site_i, size, 1)]
    )


def print_double(size, site_i, sym="*="):
    return "\r" + "".join(
        ["A" for _ in range(1, site_i, 1)]
        + [sym]
        + ["B" for _ in range(site_i + 1, size, 1)]
    )


def should_apply(site_i, start_odd_bonds):
    if start_odd_bonds:
        return site_i % 2 == 1
    else:
        return site_i % 2 == 0


def sweep_move(size, *, start_position, end_position, apply_UM, apply_MV, **kwargs):
    if start_position < end_position:
        for site_i in sweep(size, from_site=start_position, to_site=end_position):
            apply_UM(kwargs["mps_left"][site_i - 1], kwargs["mps_right"][site_i])
    else:
        for site_i in sweep(size, from_site=start_position, to_site=end_position):
            apply_MV(kwargs["mps_left"][site_i - 1], kwargs["mps_right"][site_i])


def should_go_left(size, layer, position, start_left):
    if position <= 2:
        return True
    elif position >= size - 1:
        return False
    elif (layer % 2 == 0) == start_left:
        return True
    else:
        return False


def should_apply_gate(position, start_odd_bonds):
    if start_odd_bonds:
        start_odd_bonds = 0
    else:
        start_odd_bonds = 1

    return (position + start_odd_bonds) % 2 == 0


def sweep_on_layer(size, layer, start_left):
    if start_left:
        start_left = 0
    else:
        start_left = 1

    if (layer + start_left % 2) == 0:
        return sweep(size, from_site=0, to_site=size - 2)
    else:
        return sweep(size, from_site=size - 2, to_site=0)


def conserve_quantum_sector(model_name, position, size, conserve_total):
    head = model_name.split("_")[0]
    if head == "sh":
        d = 2
    elif head == "so":
        d = 3
    elif head == "sf":
        d = 4

    diff = size - conserve_total
    if position < diff or position > size - diff:
        return list(range(d))  # all
    elif diff > size // 2:
        return list(range(d - 1))  # inc
    elif diff <= size // 2:
        return list(range(1, d))  # dec
    else:
        return []  # should never occur


def sweep_eleven_times_hard(
    mps,
    ggate,
    dw_dict,
    chi_max,
    normalize,
    eps,
    start_left=True,
    start_odd_bonds=True,
):
    size = len(mps)

    for layer in range(11):
        print(f"suzuki_trotter fourth order, layer {layer+1}/11")
        if layer in [0, 10]:
            gate = ggate[0]
        elif layer in [4, 6]:
            gate = ggate[2]
        elif layer in [5]:
            gate = ggate[3]
        else:  # [1, 2, 3, 7, 8, 9]:
            gate = ggate[1]

        if start_left:
            direction_right = 2
        else:
            direction_right = -2

        for l in sweep_on_layer(size, layer, start_left):
            if should_apply_gate(l, start_odd_bonds):
                apply_gate_on_mm_at(
                    mps,
                    gate,
                    l + 1,
                    dw_dict,
                    chi_max,
                    normalize,
                    eps,
                    is_um=start_left,
                    conserve_left_right_after_gate=False,
                    direction_right=direction_right,
                )
            else:
                apply_mm_at(
                    mps,
                    l + 1,
                    dw_dict,
                    chi_max,
                    normalize,
                    eps,
                    is_um=start_left,
                    conserve_left_right_before=False,
                    direction_right=direction_right,
                )

        print("dw_one_serie", dw_dict["dw_one_serie"])
        dw_dict["dw_total"] += dw_dict["dw_one_serie"]
        start_left = not start_left
        start_odd_bonds = not start_odd_bonds


def sweep_eleven_times(
    mps,
    ggate,
    dw_dict,
    chi_max,
    normalize,
    eps,
    strategy=2,
    start_left=True,
    start_odd_bonds=True,
):
    size = len(mps)
    is_even = size % 2 == 0
    right_border = 0
    if (start_left and start_odd_bonds) or (not start_left and not start_odd_bonds):
        if is_even:
            right_border = size - 3
        else:
            right_border = size - 2
    elif (start_left and not start_odd_bonds) or (not start_left and start_odd_bonds):
        if is_even:
            right_border = size - 2
        else:
            right_border = size - 3

    # this is to ensure the first steps without gate
    if start_left:
        if not start_odd_bonds:
            apply_mm_at(
                mps,
                1,
                dw_dict,
                chi_max,
                normalize,
                eps,
                is_um=True,
                conserve_left_right_before=False,
                direction_right=2,
            )
            print_double(size, 1, sym="A*")
    else:
        if (is_even and not start_odd_bonds) or (not is_even and start_odd_bonds):
            apply_mm_at(
                mps,
                size - 1,
                dw_dict,
                chi_max,
                normalize,
                eps,
                is_um=False,
                conserve_left_right_before=False,
                direction_right=-2,
            )
            print_double(size, size - 1, sym="*B")
    # without the above, quantum numbers are not taken into account

    for layer in range(11):
        print(f"suzuki_trotter fourth order, layer {layer+1}/11")
        if layer in [0, 10]:
            gate = ggate[0]
        elif layer in [4, 6]:
            gate = ggate[2]
        elif layer in [5]:
            gate = ggate[3]
        else:  # [1, 2, 3, 7, 8, 9]:
            gate = ggate[1]

        # logic of the loop: always apply gate first
        if start_left and start_odd_bonds:
            for l in range(1, size - 2, 2):
                print_double(size, l, "A=")
                apply_gate_on_mm_at(
                    mps,
                    gate,
                    l,
                    dw_dict,
                    chi_max,
                    normalize,
                    eps,
                    is_um=True,
                    conserve_left_right_after_gate=False,
                    direction_right=strategy,
                )
                print_double(size, l + 1, "A*")
                apply_mm_at(
                    mps,
                    l + 1,
                    dw_dict,
                    chi_max,
                    normalize,
                    eps,
                    is_um=True,
                    conserve_left_right_before=False,
                    direction_right=strategy,
                )

            if is_even:
                print_double(size, size - 1, "=B")
                apply_gate_on_mm_at(
                    mps,
                    gate,
                    size - 1,
                    dw_dict,
                    chi_max,
                    normalize,
                    eps,
                    is_um=False,
                    conserve_left_right_after_gate=False,
                    direction_right=-strategy,
                )
            else:
                print_double(size, size - 2, "A=")
                apply_gate_on_mm_at(
                    mps,
                    gate,
                    size - 2,
                    dw_dict,
                    chi_max,
                    normalize,
                    eps,
                    is_um=True,
                    conserve_left_right_after_gate=False,
                    direction_right=strategy,
                )

        elif not start_left and not start_odd_bonds:
            for l in range(right_border, 2, -2):
                print_double(size, l + 1, "=B")
                apply_gate_on_mm_at(
                    mps,
                    gate,
                    l + 1,
                    dw_dict,
                    chi_max,
                    normalize,
                    eps,
                    is_um=False,
                    conserve_left_right_after_gate=False,
                    direction_right=-strategy,
                )
                print_double(size, l, "*B")
                apply_mm_at(
                    mps,
                    l,
                    dw_dict,
                    chi_max,
                    normalize,
                    eps,
                    is_um=False,
                    conserve_left_right_before=False,
                    direction_right=-strategy,
                )

            # left border
            print_double(size, 2, "=B")
            apply_gate_on_mm_at(
                mps,
                gate,
                2,
                dw_dict,
                chi_max,
                normalize,
                eps,
                is_um=False,
                conserve_left_right_after_gate=False,
                direction_right=-strategy,
            )

        elif start_left and not start_odd_bonds:
            for l in range(2, size - 2, 2):
                print_double(size, l, "A=")
                apply_gate_on_mm_at(
                    mps,
                    gate,
                    l,
                    dw_dict,
                    chi_max,
                    normalize,
                    eps,
                    is_um=True,
                    conserve_left_right_after_gate=False,
                    direction_right=strategy,
                )
                print_double(size, l + 1, "A*")
                apply_mm_at(
                    mps,
                    l + 1,
                    dw_dict,
                    chi_max,
                    normalize,
                    eps,
                    is_um=True,
                    conserve_left_right_before=False,
                    direction_right=strategy,
                )

            if is_even:
                print_double(size, size - 2, "A=")
                apply_gate_on_mm_at(
                    mps,
                    gate,
                    size - 2,
                    dw_dict,
                    chi_max,
                    normalize,
                    eps,
                    is_um=True,
                    conserve_left_right_after_gate=False,
                    direction_right=strategy,
                )
            else:
                print_double(size, size - 1, "=B")
                apply_gate_on_mm_at(
                    mps,
                    gate,
                    size - 1,
                    dw_dict,
                    chi_max,
                    normalize,
                    eps,
                    is_um=False,
                    conserve_left_right_after_gate=False,
                    direction_right=-strategy,
                )

        elif not start_left and start_odd_bonds:
            for l in range(right_border, 1, -2):
                print_double(size, l + 1, "=B")
                apply_gate_on_mm_at(
                    mps,
                    gate,
                    l + 1,
                    dw_dict,
                    chi_max,
                    normalize,
                    eps,
                    is_um=False,
                    conserve_left_right_after_gate=False,
                    direction_right=-strategy,
                )
                print_double(size, l, "*B")
                apply_mm_at(
                    mps,
                    l,
                    dw_dict,
                    chi_max,
                    normalize,
                    eps,
                    is_um=False,
                    conserve_left_right_before=False,
                    direction_right=-strategy,
                )

            # left border
            print_double(size, 1, "A=")
            apply_gate_on_mm_at(
                mps,
                gate,
                1,
                dw_dict,
                chi_max,
                normalize,
                eps,
                is_um=True,
                conserve_left_right_after_gate=False,
                direction_right=strategy,
            )

        start_left = not start_left
        start_odd_bonds = not start_odd_bonds
        print("dw_one_serie", dw_dict["dw_one_serie"])
        dw_dict["dw_total"] += dw_dict["dw_one_serie"]


def idmrg_minimize_two_sites(
    dst_left,
    dst_right,
    bloc_left,
    bloc_right,
    ham_mpo_left,
    ham_mpo_right,
    sim_dict,
    *,
    position,
    size,
    conserve_total,
    d,
):

    env_bloc = create_env_blocs(bloc_left, ham_mpo_left, ham_mpo_right, bloc_right)
    select_quantum_sector(
        env_bloc, position, size=size, qnum_conserved=conserve_total, d=d
    )

    # minimize energy
    theta = minimize_on_mm(env_bloc, None, None, None, driver="scipy")

    theta_to_mm(
        theta,
        dst_left,
        {},
        sim_dict,
        sim_dict["chi_max"],
        True,
        True,
        1,
        sim_dict["eps_truncation"],
    )
    theta_to_mm(
        theta,
        {},
        dst_right,
        sim_dict,
        sim_dict["chi_max"],
        True,
        False,
        -1,
        sim_dict["eps_truncation"],
    )


def idmrg_even(
    dst_imps_left,
    dst_imps_right,
    bloc_left,
    bloc_right,
    ham_mpo,
    idmrg_dict,
    *,
    iterations,
    size,
    conserve_total,
    d,
):
    for pos in range(2, iterations + 2):
        tmp_imps_left = {}
        tmp_imps_right = {}

        idmrg_minimize_two_sites(
            tmp_imps_left,
            tmp_imps_right,
            bloc_left,
            bloc_right,
            ham_mpo[0],
            ham_mpo[1],
            idmrg_dict,
            position=pos,
            size=size,
            conserve_total=conserve_total,
            d=d,
        )
        bloc_left = update_left(tmp_imps_left, ham_mpo[0], bloc_left)
        bloc_right = update_right(tmp_imps_right, ham_mpo[1], bloc_right)

        dst_imps_left.append(_copy(tmp_imps_left))
        dst_imps_right.append(_copy(tmp_imps_right))
        tmp_imps_left.clear()
        tmp_imps_right.clear()

    finalize_idmrg_even_size(
        tmp_imps_left,
        tmp_imps_right,
        bloc_left,
        bloc_right,
        ham_mpo[0],
        ham_mpo[1],
        idmrg_dict,
        position=(size) // 2,
        size=size,
        conserve_total=conserve_total,
        d=d,
    )

    dst_imps_left.append(_copy(tmp_imps_left))
    dst_imps_right.append(_copy(tmp_imps_right))


def compress_mps(
    mps,
    chi_max,
    normalize,
    eps,
    *,
    start_left=True,
):
    size = len(mps)
    for _ in range(2):
        if start_left:
            direction_right = 1
        else:
            direction_right = -1

        if start_left:
            for l in range(1, size, 1):
                apply_mm_at(
                    mps,
                    l,
                    {"dw_one_serie": 0},
                    chi_max,
                    normalize,
                    eps,
                    is_um=True,
                    conserve_left_right_before=False,
                    direction_right=direction_right,
                )
                print_double(size, l, "A=")
        else:
            for l in range(size - 1, 0, -1):
                apply_mm_at(
                    mps,
                    l,
                    {"dw_one_serie": 0},
                    chi_max,
                    normalize,
                    eps,
                    is_um=False,
                    conserve_left_right_before=False,
                    direction_right=direction_right,
                )
                print_double(size, l, "=B")

        start_left = not start_left


def dmrg_sweep(
    mps,
    ham,
    left_right,
    left_right_var,
    chi_max,
    normalize,
    eps,
    max_iteration,
    tolerance,
    nb_sweeps,
    *,
    start_left=True,
    driver="lanczos",
):

    size = len(mps)

    for layer in range(nb_sweeps):
        print(f"dmrg sweep {layer+1}/{nb_sweeps}")

        if start_left:
            for l in range(1, size - 2, 1):
                print_double(size, l, "MM")
                _minimize_and_move(
                    l,
                    mps,
                    ham,
                    left_right,
                    max_iteration,
                    tolerance,
                    chi_max,
                    normalize,
                    eps,
                    direction_right=1,
                    is_um=True,
                    driver=driver,
                )
                print_double(size, l, "A=")
        else:
            for l in range(size - 3, 0, -1):
                print_double(size, l, "MM")
                _minimize_and_move(
                    l,
                    mps,
                    ham,
                    left_right,
                    max_iteration,
                    tolerance,
                    chi_max,
                    normalize,
                    eps,
                    direction_right=-1,
                    is_um=False,
                    driver=driver,
                )
                print_double(size, l, "=B")

        start_left = not start_left


def dmrg_warmup(mps, ham, left_right, sim_dict, *, start_left):
    dmrg_sweep(
        mps,
        ham,
        left_right,
        None,
        chi_max=sim_dict["chi_max_warmup"],
        normalize=sim_dict["normalize"],
        eps=sim_dict["eps_truncation"],
        max_iteration=sim_dict["max_iteration"],
        tolerance=sim_dict["tolerance"],
        nb_sweeps=sim_dict["nb_sweeps_warmup"],
        start_left=start_left,
        driver="lanczos",
    )


def dmrg_sweeps(mps, ham, left_right, left_right_var, sim_dict, *, start_left):
    dmrg_sweep(
        mps,
        ham,
        left_right,
        left_right_var,
        chi_max=sim_dict["chi_max"],
        normalize=sim_dict["normalize"],
        eps=sim_dict["eps_truncation"],
        max_iteration=sim_dict["max_iteration"],
        tolerance=sim_dict["tolerance"],
        nb_sweeps=sim_dict["nb_sweeps"],
        start_left=start_left,
        driver="lanczos",  # TODO = "jacobi"
    )
