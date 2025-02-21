from pyfhmdot.routine import mpsQ_svd_th2mV, mpsQ_svd_th2Um
from pyfhmdot.contract import (
    multiply_blocs_no_gate_applied,
    multiply_blocs_with_gate_applied,
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


def print_double(size, site_i):
    return "\r" + "".join(
        ["A" for _ in range(1, site_i, 1)]
        + ["*="]
        + ["B" for _ in range(site_i + 1, size, 1)]
    )


""" 
def multiply(ma, mb):  # -> mdest
    mdest = _np.tensordot(ma, mb, (2, 0))
    return mdest


def multiply_with_gate(ma, mb, mtheta):  # -> mdest
    mtmp = _np.tensordot(ma, mb, (3, 0))
    mdest = _np.tensordot(
        mtheta, mtmp, ([0, 1], [1, 2])).transpose([2, 0, 1, 3])
    return mdest """


def apply_UM(lhs_blocs, rhs_blocs, **kwargs):
    tmp_blocs = {}
    multiply_blocs_no_gate_applied(
        tmp_blocs,
        lhs_blocs,
        rhs_blocs,
        conserve_left_right=kwargs["conserve_left_right"],
    )
    lhs_blocs.clear()
    rhs_blocs.clear()
    mpsQ_svd_th2Um(tmp_blocs, lhs_blocs, rhs_blocs, **kwargs)


def apply_MV(lhs_blocs, rhs_blocs, **kwargs):
    tmp_blocs = {}
    multiply_blocs_no_gate_applied(
        tmp_blocs,
        lhs_blocs,
        rhs_blocs,
        conserve_left_right=kwargs["conserve_left_right"],
    )
    lhs_blocs = {}
    rhs_blocs = {}
    mpsQ_svd_th2mV(tmp_blocs, lhs_blocs, rhs_blocs, **kwargs)


def apply_gate_UM(lhs_blocs, rhs_blocs, gate_blocs, **kwargs):
    tmp_blocs = {}
    multiply_blocs_with_gate_applied(
        tmp_blocs,
        lhs_blocs,
        rhs_blocs,
        gate_blocs,
        conserve_left_right=kwargs["conserve_left_right"],
    )


def apply_gate_MV(lhs_blocs, rhs_blocs, gate_blocs, **kwargs):
    tmp_blocs = {}
    multiply_blocs_with_gate_applied(
        tmp_blocs,
        lhs_blocs,
        rhs_blocs,
        gate_blocs,
        conserve_left_right=kwargs["conserve_left_right"],
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
    **kwargs
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
                    **kwargs
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
                    **kwargs
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
    **kwargs
):
    pass


def sweep_eleven_times(
    size,
    *,
    start_position,
    end_position,
    apply_UM,
    apply_MV,
    apply_gate_UM,
    apply_gate_MV,
    start_odd_bonds=True,
    **kwargs
):

    if start_position is None:
        start_position = 1
    if end_position is None:
        end_position = size

    if start_position < size / 2:
        start_position = 1
        right_direction = True
    else:
        start_position = size
        right_direction = False

    for _ in range(11):
        if (_ % 2) == 0:
            # apply_border(size, position=1,apply_UM,apply_MV,apply_gate_UM,apply_gate_MV,start_odd_bonds,**kwargs)
            # sweep_and_apply(size, start_position=2,end_position=end_position-2,apply_UM,apply_MV,apply_gate_UM,apply_gate_MV,start_odd_bonds,**kwargs)
            pass
        else:
            # apply_border(size, position=size-1,apply_UM,apply_MV,apply_gate_UM,apply_gate_MV,start_odd_bonds,**kwargs)
            # sweep_and_apply(size, start_position=size-2,end_position=2,apply_UM,apply_MV,apply_gate_UM,apply_gate_MV,start_odd_bonds,**kwargs)
            pass
