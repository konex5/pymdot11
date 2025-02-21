import pytest

from tests.pyfhmdot.routine.test_multiply_blocs_with_gate import (
    test_multiply_blocs_sparse_with_gate_fake,
    test_multiply_blocs_sparse_with_gate_fake_onedir_qnum,
    test_multiply_blocs_sparse_with_gate_fake_with_qcons,
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
    return test_multiply_blocs_sparse_with_gate_fake(
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
    return test_multiply_blocs_sparse_with_gate_fake_onedir_qnum(
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
    return test_multiply_blocs_sparse_with_gate_fake_with_qcons(
        make_single_blocs_mps,
        make_single_blocs_gate,
        lhs_indices,
        lhs_chi_shapes,
        rhs_indices,
        rhs_chi_shapes,
        gate_indices,
    )


@pytest.mark.skip
def test_potential_middle(theta_blocs_large, theta_blocs_average, theta_blocs_small):
    from pyfhmdot.routine.indices import (
        potential_middle_indices,
    )

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


@pytest.mark.skip
def test_find_degeneracy_in_theta(theta_blocs_large):
    from pyfhmdot.routine.indices import (
        degeneracy_in_theta,
        potential_middle_indices,
    )

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
    from pyfhmdot.routine.indices import (
        degeneracy_in_theta,
        potential_middle_indices,
    )

    middle_list = potential_middle_indices(theta_blocs_small.keys(), direction_right=1)
    nondeg, degenerate = degeneracy_in_theta(
        theta_blocs_small.keys(), middle_list, direction_right=1
    )
    assert len(nondeg) == 1
    assert nondeg[0][-1] == (0, 1, 0, 1)
    assert len(degenerate) == 1
    assert degenerate[0][-1][0] == (0, 0, 0, 0)
    assert degenerate[0][-1][1] == (0, 0, 1, 1)


def test_check_slices_degenerate_blocs_dimone(theta_blocs_small):
    from pyfhmdot.routine.indices import (
        degeneracy_in_theta,
        slices_degenerate_blocs,
        potential_middle_indices,
    )

    middle_list = potential_middle_indices(theta_blocs_small.keys(), direction_right=1)
    nondeg, degenerate = degeneracy_in_theta(
        theta_blocs_small.keys(), middle_list, direction_right=1
    )
    newsubsize = []
    slices_degenerate_blocs(theta_blocs_small, degenerate, newsubsize)
    assert len(newsubsize) == 1


@pytest.mark.skip
def test_check_slices_degenerate_blocs_dimtwo(theta_blocs_large):
    from pyfhmdot.routine.indices import (
        degeneracy_in_theta,
        slices_degenerate_blocs,
        potential_middle_indices,
    )

    middle_list = potential_middle_indices(theta_blocs_large.keys())
    nondeg, degenerate = degeneracy_in_theta(
        theta_blocs_large.keys(), middle_list, direction_right=True
    )
    newsubsize = []
    slices_degenerate_blocs(theta_blocs_large, degenerate, newsubsize)
    assert len(newsubsize) == 2
