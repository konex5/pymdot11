import pytest
from automation import is_mdot_available


# @pytest.mark.skip
def test_idmrg_all():
    from pymdot.entrypoint import infinite_to_finite_ground_state

    imps = []
    infinite_to_finite_ground_state(
        imps,
        "sh_xxz-hz_u1",
        {"Jxy": 1, "Jz": 1, "hz": 0},
        {
            "chi_max": 10,
            "normalize": True,
            "eps_truncation": 1e-8,
            "dw_total": 0,
            "dw_one_serie": 0,
        },
        size=12,
        conserve_total=6,
    )

    from pymdot.entrypoint import variational_ground_state
    from pymdot.initialize import create_hamiltonian

    ham = create_hamiltonian("sh_xxz-hz_u1", {"Jxy": 1, "Jz": 1, "hz": 0}, len(imps))
    if is_mdot_available():
        variational_ground_state(
            imps,
            ham,
            {
                "dw_one_serie": 0,
                "nb_sweeps_warmup": 8,
                "nb_sweeps": 5,
                "chi_max_warmup": 30,
                "chi_max": 60,
                "normalize": False,
                "eps_truncation": 10**-8,
                "max_iteration": 30,
                "tolerance": 10**-5,
            },
        )
    pass
