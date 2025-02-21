import pytest


# @pytest.mark.skip
def test_idmrg_all():
    from pyfhmdot.entrypoint import infinite_to_finite_ground_state

    imps = []
    infinite_to_finite_ground_state(
        imps,
        "sh_xxz-hz_u1",
        {"Jxy": 1, "Jz": 1, "hz": 0},
        {"chi_max": 10, "eps_truncation": 1e-8, "dw_total": 0, "dw_one_serie": 0},
        size=20,
        conserve_total=20,
    )
    pass
