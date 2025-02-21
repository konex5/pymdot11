import pytest


@pytest.mark.skip
def test_mpsQ_svd_th2Um(theta_blocs_small):
    from pyfhmdot.routine import theta_to_mm

    lhs_blocs = {}
    rhs_blocs = {}
    theta_to_mm(
        theta_blocs_small,
        lhs_blocs,
        rhs_blocs,
        {
            "eps_truncation_error": 1e-8,
            "dw_Dmax": 800,
            "dw_Dmax_tot": 900,
            "normalize": True,
            "dw_one_serie": 0,
        },
        is_um=True,
    )
    pass


@pytest.mark.skip
def test_mpsQ_svd_th2mV(theta_blocs_small):
    from pyfhmdot.routine import theta_to_mm

    lhs_blocs = {}
    rhs_blocs = {}
    theta_to_mm(
        theta_blocs_small,
        lhs_blocs,
        rhs_blocs,
        {
            "eps_truncation_error": 1e-8,
            "dw_Dmax": 800,
            "dw_Dmax_tot": 900,
            "normalize": True,
            "dw_one_serie": 0,
        },
        is_um=False,
    )
    pass
