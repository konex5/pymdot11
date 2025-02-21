from pyfhmdot.algorithm import apply_mm_at, apply_gate_on_mm_at
from copy import deepcopy as _copy
from logging import warning as _warning
from pyfhmdot.initialize import finalize_idmrg_even_size

from pyfhmdot.intense.contract import (
    contract_left_bloc_mps,
    contract_left_right_mpo_mpo_permute,
    contract_right_bloc_mps,
)
from pyfhmdot.routine.interface import (
    apply_eigenvalues,
    minimize_theta,
    select_lowest_blocs,
    theta_to_mm,
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
            direction_right = 1
        else:
            direction_right = 3

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
                direction_right=1,
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
                direction_right=3,
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

        if start_left:
            direction_right = 1
        else:
            direction_right = 3

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
                    direction_right=direction_right,
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
                    direction_right=direction_right,
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
                    direction_right=3,
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
                    direction_right=1,
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
                    direction_right=direction_right,
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
                    direction_right=direction_right,
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
                direction_right=3,
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
                    direction_right=direction_right,
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
                    direction_right=direction_right,
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
                    direction_right=1,
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
                    direction_right=3,
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
                    direction_right=direction_right,
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
                    direction_right=direction_right,
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
                direction_right=1,
            )

        start_left = not start_left
        start_odd_bonds = not start_odd_bonds
        print("dw_one_serie", dw_dict["dw_one_serie"])
        dw_dict["dw_total"] += dw_dict["dw_one_serie"]


def dmrg_minimize_two_sites(
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
    # select_quantum_sector
    diff = min(size - conserve_total, conserve_total)
    if position < diff or position > size - diff:
        allowed_sector = list(range(d))  # all
    elif conserve_total <= size // 2:
        allowed_sector = list(range(d - 1))  # inc
    elif size - conserve_total <= size // 2:
        allowed_sector = list(range(1, d))  # dec
    else:
        allowed_sector = []  # should never occur

    # contract and permute
    env_bloc = {}
    contract_left_right_mpo_mpo_permute(
        env_bloc, bloc_left, ham_mpo_left, ham_mpo_right, bloc_right
    )
    for key in list(env_bloc.keys()):
        shape = env_bloc[key].shape
        if not (
            shape[0] * shape[1] * shape[2] * shape[3]
            == shape[4] * shape[5] * shape[6] * shape[7]
        ):
            env_bloc.pop(key)  # non physical blocs
        elif (
            not (key[1] in allowed_sector)
            or not (key[2] in allowed_sector)
            or not (key[5] in allowed_sector)
            or not (key[6] in allowed_sector)
        ):
            env_bloc.pop(key)  # quantum conserved is used here
        elif not (
            key[0] + key[1] - key[2] - key[3] == 0
            and key[4] + key[5] - key[6] - key[7] == 0
        ):
            env_bloc.pop(
                key
            )  # quantum sum is preserved here (left sum is same as right sum)
    # minimize energy
    eigenvalues = {}
    eigenvectors = {}
    minimize_theta(env_bloc, eigenvalues, eigenvectors, sim_dict["chi_max"])

    # for key in list(eigenvectors.keys()):
    #     if not (
    #         key[1] in allowed_sector and key[2] in allowed_sector and key[1] == key[2]
    #     ):
    #         eigenvectors.pop(key)
    #         eigenvalues.pop(key)
    #         _warning("eigenvectors removed a posteriori.")
    select_lowest_blocs(eigenvalues, eigenvectors)
    # select_quantum_sector(eigenvalues, eigenvectors)
    apply_eigenvalues(eigenvalues, eigenvectors)

    theta_to_mm(
        eigenvectors,
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
        eigenvectors,
        {},
        dst_right,
        sim_dict,
        sim_dict["chi_max"],
        True,
        False,
        3,
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
    for _ in range(iterations):
        tmp_imps_left = {}
        tmp_imps_right = {}

        dmrg_minimize_two_sites(
            tmp_imps_left,
            tmp_imps_right,
            bloc_left,
            bloc_right,
            ham_mpo[0],
            ham_mpo[1],
            idmrg_dict,
            position=iterations,
            size=size,
            conserve_total=conserve_total,
            d=d,
        )
        #
        new_bloc_left = {}
        new_bloc_right = {}
        contract_right_bloc_mps(
            new_bloc_right, bloc_right, tmp_imps_right, ham_mpo[1], tmp_imps_right
        )
        contract_left_bloc_mps(
            new_bloc_left, bloc_left, tmp_imps_left, ham_mpo[0], tmp_imps_left
        )
        bloc_left.clear()
        bloc_right.clear()
        bloc_left, bloc_right = new_bloc_left, new_bloc_right

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
        position=(size - len(dst_imps_left) - 1) // 2,
        size=size,
        conserve_total=conserve_total,
        d=d,
    )

    dst_imps_left.append(_copy(tmp_imps_left))
    dst_imps_right.append(_copy(tmp_imps_right))


def dmrg_warmup(mps, ham, left, right, sim_dict, *, chi_max):
    pass


def dmrg_sweeps(mps, ham, left, right, left_var, right_var, sim_dict, *, chi_max):
    pass
