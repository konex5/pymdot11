from pyfhmdot.routine.interface import (
    mm_to_theta_no_gate,
    mm_to_theta_with_gate,
    theta_to_mm,
)


def apply_mm(
    mps_left,
    mps_right,
    dw_dict,
    chi_max,
    normalize,
    eps,
    *,
    is_um,
    conserve_left_right_before=False,
    direction_right=-1,
):
    tmp_blocs = {}
    mm_to_theta_no_gate(
        dst_blocs=tmp_blocs,
        lhs_blocs=mps_left,
        rhs_blocs=mps_right,
        conserve_left_right=conserve_left_right_before,
    )
    mps_left.clear()
    mps_right.clear()
    theta_to_mm(
        theta_blocs=tmp_blocs,
        lhs_blocs=mps_left,
        rhs_blocs=mps_right,
        dw_dict=dw_dict,
        chi_max=chi_max,
        normalize=normalize,
        direction_right=direction_right,
        eps=eps,
        is_um=is_um,
    )
    return mps_left, mps_right


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
    direction_right=-1,
):
    mps[position - 1], mps[position] = apply_mm(
        mps[position - 1],
        mps[position],
        dw_dict,
        chi_max,
        normalize,
        eps,
        is_um=is_um,
        conserve_left_right_before=conserve_left_right_before,
        direction_right=direction_right,
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
    conserve_left_right_after_gate=False,
    direction_right=-1,
):
    tmp_blocs = {}
    mm_to_theta_with_gate(
        dst_blocs=tmp_blocs,
        lhs_blocs=mps[position - 1],
        rhs_blocs=mps[position],
        gate_blocs=gate[position - 1],
        conserve_left_right_before=False,
        conserve_left_right_after=conserve_left_right_after_gate,
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
        direction_right=direction_right,
        eps=eps,
        is_um=is_um,
    )
