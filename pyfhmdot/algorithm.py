from pyfhmdot.routine.interface import (
    mm_to_theta_no_gate,
    mm_to_theta_with_gate,
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
        for _ in range(from_site - 1, to_site - 2, -1):
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


def apply_mm_at(
    mps,
    position,
    dw_dict,
    chi_max,
    normalize,
    eps,
    *,
    is_um,
    conserve_left_right_before=False,
    conserve_direction_left_after=None,
):
    tmp_blocs = {}
    mm_to_theta_no_gate(
        dst_blocs=tmp_blocs,
        lhs_blocs=mps[position - 1],
        rhs_blocs=mps[position],
        conserve_left_right=conserve_left_right_before,
    )
    mps[position - 1].clear()
    mps[position].clear()
    theta_to_mm(
        theta_blocs=tmp_blocs,
        lhs_blocs=mps[position - 1],
        rhs_blocs=mps[position],
        dw_dict=dw_dict,
        chi_max=chi_max,
        normalize=normalize,
        conserve_direction_left=conserve_direction_left_after,
        eps=eps,
        is_um=is_um,
    )


def apply_gate_on_mm_at(
    mps,
    gate,
    position,
    dw_dict,
    chi_max,
    normalize,
    eps,
    *,
    is_um,
    conserve_left_right_before=False,
    conserve_direction_left_after=None,
):
    tmp_blocs = {}
    mm_to_theta_with_gate(
        dst_blocs=tmp_blocs,
        lhs_blocs=mps[position - 1],
        rhs_blocs=mps[position],
        gate_blocs=gate[position - 1],
        conserve_left_right=conserve_left_right_before,
    )
    mps[position - 1].clear()
    mps[position].clear()
    theta_to_mm(
        theta_blocs=tmp_blocs,
        lhs_blocs=mps[position - 1],
        rhs_blocs=mps[position],
        dw_dict=dw_dict,
        chi_max=chi_max,
        normalize=normalize,
        conserve_direction_left=conserve_direction_left_after,
        eps=eps,
        is_um=is_um,
    )


def sweep_move(size, *, start_position, end_position, apply_UM, apply_MV, **kwargs):
    if start_position < end_position:
        for site_i in sweep(size, from_site=start_position, to_site=end_position):
            apply_UM(kwargs["mps_left"][site_i - 1], kwargs["mps_right"][site_i])
    else:
        for site_i in sweep(size, from_site=start_position, to_site=end_position):
            apply_MV(kwargs["mps_left"][site_i - 1], kwargs["mps_right"][site_i])


def sweep_and_apply(
    size,
    *,
    start_position,
    end_position,
    apply_UM,
    apply_MV,
    apply_gate_UM,
    apply_gate_MV,
    start_odd_bonds,
    **kwargs,
):

    should_apply_gate = (start_position % 2) == 0
    if start_odd_bonds:
        should_apply_gate = not should_apply_gate

    if start_position < end_position:
        for site_i in sweep(size, from_site=start_position, to_site=end_position):
            if should_apply_gate:
                apply_gate_UM(
                    kwargs["mps"][site_i - 1],
                    kwargs["mps"][site_i],
                    gate_blocs=kwargs["gate"][site_i],
                    **kwargs,
                )
            else:
                apply_UM(kwargs["mps"][site_i - 1], kwargs["mps"][site_i], **kwargs)
            should_apply_gate = not should_apply_gate
    else:
        for site_i in sweep(size, from_site=start_position, to_site=end_position):
            if should_apply_gate:
                apply_gate_MV(
                    kwargs["mps"][site_i - 1],
                    kwargs["mps"][site_i],
                    gate_blocs=kwargs["gate"][site_i],
                    **kwargs,
                )
            else:
                apply_MV(kwargs["mps"][site_i - 1], kwargs["mps"][site_i], **kwargs)
            should_apply_gate = not should_apply_gate


def apply_border(
    size,
    *,
    position,
    apply_UM,
    apply_MV,
    apply_gate_UM,
    apply_gate_MV,
    start_odd_bonds=True,
    **kwargs,
):
    pass


def sweep_eleven_times(
    size,
    mps,
    ggate,
    dw_dict,
    chi_max,
    normalize,
    eps,
    start_left=True,
    start_odd_bonds=True,
):

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
            # apply_mm_at(mps,1,dw_dict,chi_max,normalize,eps,is_um=True,conserve_left_right_before=False,conserve_direction_left_after=True)
            print_double(size, 1, sym="A*")
    else:
        if (is_even and not start_odd_bonds) or (not is_even and start_odd_bonds):
            # apply_mm_at(mps,size,dw_dict,chi_max,normalize,eps,is_um=False,conserve_left_right_before=False,conserve_direction_left_after=False)
            print_double(size, size, sym="*B")
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

        if start_left and start_odd_bonds:
            for l in range(1, size - 2, 2):
                print_double(size, l, "A=")
                # apply_gate_UM(mps, gate, l - 1, simdict)
                print_double(size, l + 1, "A*")
                # apply_UM(mps, [], l, simdict)

            if is_even:
                print_double(size, size - 1, "=B")
                # apply_gate_MV(mps, gate, L - 2, simdict)
            else:
                print_double(size, size - 2, "A=")
                # apply_gate_UM(mps, gate, L - 3, simdict)

        elif not start_left and not start_odd_bonds:
            for l in range(right_border, 2, -2):
                print_double(size, l + 1, "=B")
                # apply_gate_MV(mps, gate, l, simdict)
                print_double(size, l, "*B")
                # apply_MV(mps, [], l - 1, simdict)

            # left border
            print_double(size, 2, "=B")
            # apply_gate_MV(mps, gate, 1, simdict)

        elif start_left and not start_odd_bonds:
            for l in range(2, size - 2, 2):
                print_double(size, l, "A=")
                # apply_gate_UM(mps, gate, l - 1, simdict)
                print_double(size, l + 1, "A*")
                # apply_UM(mps, [], l, simdict)

            if is_even:
                print_double(size, size - 2, "A=")
                # apply_gate_UM(mps, gate, L - 3, simdict)
            else:
                print_double(size, size - 1, "=B")
                # apply_gate_MV(mps, gate, L - 2, simdict)

        elif not start_left and start_odd_bonds:
            for l in range(right_border, 1, -2):
                print_double(size, l + 1, "=B")
                # apply_gate_MV(mps, gate, l, simdict)
                print_double(size, l, "*B")
                # apply_MV(mps, [], l - 1, simdict)

            # left border
            print_double(size, 1, "A=")
            # apply_gate_UM(mps, gate, 0, simdict)

        start_left = not start_left
        start_odd_bonds = not start_odd_bonds
        print("dw_one_serie", dw_dict["dw_one_serie"])
