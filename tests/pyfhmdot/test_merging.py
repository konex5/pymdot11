from pyfhmdot.routine import mpsQ_svd_th2Um, mpsQ_svd_th2mV
from tests.pyfhmdot.test_multiply_blocs_with_gate import (
    test_multiply_blocs_sparse_with_gate,
    test_multiply_blocs_sparse_with_gate_onedir_qnum,
    test_multiply_blocs_sparse_with_gate_with_qcons,
)
import pytest
from pyfhmdot.indices import (
    degeneracy_in_theta,
    slices_degenerate_blocs,
    potential_middle_indices,
)


@pytest.fixture
def theta_blocs_large(
    make_single_blocs_mps,
    make_single_blocs_gate,
    lhs_indices,
    lhs_chi_shapes,
    rhs_indices,
    rhs_chi_shapes,
    gate_indices,
):
    return test_multiply_blocs_sparse_with_gate(
        make_single_blocs_mps,
        make_single_blocs_gate,
        lhs_indices,
        lhs_chi_shapes,
        rhs_indices,
        rhs_chi_shapes,
        gate_indices,
    )


@pytest.fixture
def theta_blocs_average(
    make_single_blocs_mps,
    make_single_blocs_gate,
    lhs_indices,
    lhs_chi_shapes,
    rhs_indices,
    rhs_chi_shapes,
    gate_indices,
):
    return test_multiply_blocs_sparse_with_gate_onedir_qnum(
        make_single_blocs_mps,
        make_single_blocs_gate,
        lhs_indices,
        lhs_chi_shapes,
        rhs_indices,
        rhs_chi_shapes,
        gate_indices,
    )


@pytest.fixture
def theta_blocs_small(
    make_single_blocs_mps,
    make_single_blocs_gate,
    lhs_indices,
    lhs_chi_shapes,
    rhs_indices,
    rhs_chi_shapes,
    gate_indices,
):
    return test_multiply_blocs_sparse_with_gate_with_qcons(
        make_single_blocs_mps,
        make_single_blocs_gate,
        lhs_indices,
        lhs_chi_shapes,
        rhs_indices,
        rhs_chi_shapes,
        gate_indices,
    )


def test_potential_middle(theta_blocs_large, theta_blocs_average, theta_blocs_small):
    middle_list = potential_middle_indices(theta_blocs_large.keys())
    assert middle_list == [0, 1, 2, 3, 4]
    middle_list = potential_middle_indices(
        theta_blocs_large.keys(), direction_right=True
    )
    assert middle_list == [0, 1]
    middle_list = potential_middle_indices(
        theta_blocs_large.keys(), direction_right=False
    )
    assert middle_list == [0, 1, 2, 3, 4]
    #
    middle_list = potential_middle_indices(theta_blocs_average.keys())
    assert middle_list == [0, 1]
    middle_list = potential_middle_indices(
        theta_blocs_average.keys(), direction_right=True
    )
    assert middle_list == [0, 1]
    middle_list = potential_middle_indices(
        theta_blocs_average.keys(), direction_right=False
    )
    assert middle_list == [0, 1]
    #
    middle_list = potential_middle_indices(theta_blocs_small.keys())
    assert middle_list == [0, 1]
    middle_list = potential_middle_indices(
        theta_blocs_small.keys(), direction_right=True
    )
    assert middle_list == [0, 1]
    middle_list = potential_middle_indices(
        theta_blocs_small.keys(), direction_right=False
    )
    assert middle_list == [0, 1]


def test_find_degeneracy_in_theta(theta_blocs_large):
    middle_list = potential_middle_indices(theta_blocs_large.keys())
    nondeg, degenerate = degeneracy_in_theta(
        theta_blocs_large.keys(), middle_list, direction_right=True
    )
    assert len(nondeg) == 0
    assert len(degenerate) == 2
    assert degenerate[0][-1][0] == (0, 0, 0, 0)
    assert degenerate[0][-1][1] == (0, 0, 0, 1)
    assert degenerate[0][-1][2] == (0, 0, 0, 2)
    assert degenerate[0][-1][-1] == (0, 0, 1, 4)
    assert degenerate[1][-1][0] == (0, 1, 0, 0)
    assert degenerate[1][-1][2] == (0, 1, 0, 2)


def test_find_degeneracy_in_theta_with_qcons(theta_blocs_small):
    middle_list = potential_middle_indices(theta_blocs_small.keys())
    nondeg, degenerate = degeneracy_in_theta(theta_blocs_small.keys(), middle_list)
    assert len(nondeg) == 1
    assert nondeg[0][-1] == (0, 1, 0, 1)
    assert len(degenerate) == 1
    assert degenerate[0][-1][0] == (0, 0, 0, 0)
    assert degenerate[0][-1][1] == (0, 0, 1, 1)


def test_check_slices_degenerate_blocs_dimone(theta_blocs_small):
    middle_list = potential_middle_indices(theta_blocs_small.keys())
    nondeg, degenerate = degeneracy_in_theta(theta_blocs_small.keys(), middle_list)
    newsubsize = []
    slices_degenerate_blocs(theta_blocs_small, degenerate, newsubsize)
    assert len(newsubsize) == 1


def test_check_slices_degenerate_blocs_dimtwo(theta_blocs_large):
    middle_list = potential_middle_indices(theta_blocs_large.keys())
    nondeg, degenerate = degeneracy_in_theta(
        theta_blocs_large.keys(), middle_list, direction_right=True
    )
    newsubsize = []
    slices_degenerate_blocs(theta_blocs_large, degenerate, newsubsize)
    assert len(newsubsize) == 2


def test_mpsQ_svd_th2Um(theta_blocs_small):
    mpsL = {}
    mpsR = {}
    mpsQ_svd_th2Um(
        theta_blocs_small,
        mpsL,
        mpsR,
        {
            "eps_truncation_error": 1e-8,
            "dw_Dmax": 800,
            "dw_Dmax_tot": 900,
            "normalize": True,
            "dw_one_serie": 0,
        },
    )


def test_mpsQ_svd_th2mV(theta_blocs_small):
    mpsL = {}
    mpsR = {}
    mpsQ_svd_th2mV(
        theta_blocs_small,
        mpsL,
        mpsR,
        {
            "eps_truncation_error": 1e-8,
            "dw_Dmax": 800,
            "dw_Dmax_tot": 900,
            "normalize": True,
            "dw_one_serie": 0,
        },
    )
    pass
