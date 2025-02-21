import pytest

from pyfhmdot.routine.interface import mm_to_theta_with_gate


def get_theta():
    from numpy import array

    old_theta = {
        (0, 0, 0, 0): array([[[[0.99483226]]]]),
        (0, 0, 1, 1): array([[[[0.99226175, 0.0], [0.0, 1.00780536]]]]),
        (0, 0, 2, 2): array([[[[1.00520133]]]]),
        (0, 1, 0, 1): array([[[[-0.00257052, 0.0]], [[0.0, -0.00261078]]]]),
        (0, 1, 1, 2): array([[[[0.0], [-0.00260404]], [[-0.00260404], [0.0]]]]),
        (0, 2, 0, 2): array([[[[6.74591518e-06]]]]),
        (1, 0, 1, 0): array([[[[-0.00257052], [0.0]]], [[[0.0], [-0.00261078]]]]),
        (1, 0, 2, 1): array([[[[0.0, -0.00260404]]], [[[-0.00260404, 0.0]]]]),
        (1, 1, 0, 0): array([[[[0.99226175]], [[0.0]]], [[[0.0]], [[1.00780536]]]]),
        (1, 1, 1, 1): array(
            [
                [
                    [[9.79488739e-01, 0.00000000e00], [0.00000000e00, 1.00520133e00]],
                    [[0.00000000e00, 6.74591518e-06], [0.00000000e00, 0.00000000e00]],
                ],
                [
                    [[0.00000000e00, 0.00000000e00], [6.74591518e-06, 0.00000000e00]],
                    [[1.00520133e00, 0.00000000e00], [0.00000000e00, 1.01041614e00]],
                ],
            ]
        ),
        (1, 1, 2, 2): array([[[[0.99226175]], [[0.0]]], [[[0.0]], [[1.00780536]]]]),
        (1, 2, 0, 1): array([[[[0.0, -0.00260404]]], [[[-0.00260404, 0.0]]]]),
        (1, 2, 1, 2): array([[[[-0.00257052], [0.0]]], [[[0.0], [-0.00261078]]]]),
        (2, 0, 2, 0): array([[[[6.74591518e-06]]]]),
        (2, 1, 1, 0): array([[[[0.0], [-0.00260404]], [[-0.00260404], [0.0]]]]),
        (2, 1, 2, 1): array([[[[-0.00257052, 0.0]], [[0.0, -0.00261078]]]]),
        (2, 2, 0, 0): array([[[[1.00520133]]]]),
        (2, 2, 1, 1): array([[[[0.99226175, 0.0], [0.0, 1.00780536]]]]),
        (2, 2, 2, 2): array([[[[0.99483226]]]]),
    }

    new_theta = {
        (0, 0, 0, 0): array([[[[0.99483226]]]]),
        (0, 0, 1, 1): array([[[[1.00780536, 0.0], [0.0, 0.99226175]]]]),
        (0, 0, 2, 2): array([[[[1.00520133]]]]),
        (0, 1, 0, 1): array([[[[-0.00261078, 0.0]], [[0.0, -0.00257052]]]]),
        (0, 1, 1, 2): array([[[[0.0], [-0.00260404]], [[-0.00260404], [0.0]]]]),
        (0, 2, 0, 2): array([[[[6.74591518e-06]]]]),
        (1, 0, 1, 0): array([[[[-0.00261078], [0.0]]], [[[0.0], [-0.00257052]]]]),
        (1, 0, 2, 1): array([[[[0.0, -0.00260404]]], [[[-0.00260404, 0.0]]]]),
        (1, 1, 0, 0): array([[[[1.00780536]], [[0.0]]], [[[0.0]], [[0.99226175]]]]),
        (1, 1, 1, 1): array(
            [
                [
                    [[1.01041614e00, 0.00000000e00], [0.00000000e00, 1.00520133e00]],
                    [[0.00000000e00, 6.74591518e-06], [0.00000000e00, 0.00000000e00]],
                ],
                [
                    [[0.00000000e00, 0.00000000e00], [6.74591518e-06, 0.00000000e00]],
                    [[1.00520133e00, 0.00000000e00], [0.00000000e00, 9.79488739e-01]],
                ],
            ]
        ),
        (1, 1, 2, 2): array([[[[1.00780536]], [[0.0]]], [[[0.0]], [[0.99226175]]]]),
        (1, 2, 0, 1): array([[[[0.0, -0.00260404]]], [[[-0.00260404, 0.0]]]]),
        (1, 2, 1, 2): array([[[[-0.00261078], [0.0]]], [[[0.0], [-0.00257052]]]]),
        (2, 0, 2, 0): array([[[[6.74591518e-06]]]]),
        (2, 1, 1, 0): array([[[[0.0], [-0.00260404]], [[-0.00260404], [0.0]]]]),
        (2, 1, 2, 1): array([[[[-0.00261078, 0.0]], [[0.0, -0.00257052]]]]),
        (2, 2, 0, 0): array([[[[1.00520133]]]]),
        (2, 2, 1, 1): array([[[[1.00780536, 0.0], [0.0, 0.99226175]]]]),
        (2, 2, 2, 2): array([[[[0.99483226]]]]),
    }

    from pyfhmdot.create import create_hamiltonian_gates

    new_theta = create_hamiltonian_gates(
        "sh_xxz-hz_u1",
        {"Jxy": 0.25, "Jz": 0.5, "hz": 1.5},  # 1/4.*1, 1/4.*2, 1/2.*3
        3,
        dbeta=0.025,
        is_dgate=True,
        in_group=True,
    )[0][1]
    old_theta = {}
    for key in new_theta:
        old_theta[key] = new_theta[key][::-1, ::-1, ::-1, ::-1]

    return old_theta, new_theta


def test_validation_theta_step_two_left():
    from numpy import array, all
    from copy import deepcopy

    mpsL = {}
    mpsL[(0, 1, 0)] = array(
        [
            [[-7.071067811865476e-01], [-7.071067811865475e-01]],
            [[-5.551115123125784e-17], [5.551115123125784e-17]],
        ]
    )

    mpsR = {}
    mpsR[(0, 1, 0)] = array([[[0.7071067811865475], [0.7071067811865475]]])

    mpsNextR = {}
    mpsNextR[(0, 1, 0)] = array([[[0.7071067811865475], [0.7071067811865475]]])

    old_theta, new_theta = get_theta()

    assert len(old_theta) == 19 and len(new_theta) == 19

    for key in old_theta:
        assert all(old_theta[key] == new_theta[key][::-1, ::-1, ::-1, ::-1])

    from pyfhmdot.algorithm import apply_gate_on_mm_at

    mps = [deepcopy(mpsL), deepcopy(mpsR), deepcopy(mpsNextR)]
    gate = [deepcopy(old_theta), deepcopy(old_theta)]

    tmp_blocs = {}
    mm_to_theta_with_gate(
        dst_blocs=tmp_blocs,
        lhs_blocs=mps[0],
        rhs_blocs=mps[1],
        gate_blocs=gate[0],
        conserve_left_right_before=False,
        conserve_left_right_after=False,
    )

    old_results_theta_blocs = {
        (0, 0, 2, 0): array([[[[2.60403588e-03]]], [[[-2.40741243e-35]]]]),
        (0, 1, 1, 0): array(
            [
                [
                    [[-4.89744369e-01], [-5.02604036e-01]],
                    [[-5.02604036e-01], [-5.05208072e-01]],
                ],
                [
                    [[-3.84471971e-17], [-3.94562107e-17]],
                    [[3.94562107e-17], [3.96611692e-17]],
                ],
            ]
        ),
        (0, 2, 0, 0): array([[[[2.60403588e-03]]], [[[-2.40741243e-35]]]]),
    }

    for key in tmp_blocs.keys():
        assert all(abs((tmp_blocs[key] - old_results_theta_blocs[key])) < 1e-8)

    apply_gate_on_mm_at(
        mps,
        gate,
        1,
        {"dw_one_serie": 0},
        100,
        1,
        1e-62,
        is_um=True,
        conserve_left_right_after_gate=False,
        direction_right=1,
    )

    old_results_mpsL = {
        (0, 0, 0): array([[[1.00000000e00]], [[-9.24492802e-33]]]),
        (0, 1, 1): array(
            [
                [[-7.01647432e-01, 7.12524303e-01], [-7.12524303e-01, -7.01647432e-01]],
                [[-5.50821898e-17, 5.58648184e-17], [5.59360802e-17, 5.50098233e-17]],
            ]
        ),
        (0, 2, 2): array([[[1.00000000e00]], [[-9.24492802e-33]]]),
    }

    old_results_mpsR = {
        (0, 2, 0): array([[[0.00260362]]]),
        (1, 1, 0): array([[[0.70163324], [0.71250989]], [[0.00369547], [-0.00363906]]]),
        (2, 0, 0): array([[[0.00260362]]]),
    }

    for key in mps[0].keys():
        assert all(abs((mps[0][key] - old_results_mpsL[key])) < 1e-8)

    for key in mps[1].keys():
        assert all(abs(mps[1][key] - old_results_mpsR[key]) < 1e-8)

    from pyfhmdot.algorithm import apply_mm_at

    apply_mm_at(
        mps,
        2,
        {"dw_one_serie": 0},
        100,
        1,
        1e-62,
        is_um=True,
        conserve_left_right_before=False,
        direction_right=1,
    )

    old_next_results_mpsR = {
        (0, 2, 0): array([[[-0.00260362, 0.9999662]]]),
        (1, 1, 0): array(
            [
                [[-0.70163324, -0.00731115], [-0.71250989, 0.00353689]],
                [[-0.00369547, 0.00092365], [0.00363906, -0.00086739]],
            ]
        ),
        (2, 0, 0): array([[[-0.00260362, -0.00016533]]]),
    }
    old_next_results_mpsNextR = {
        (0, 1, 0): array(
            [
                [[-7.07106781e-01], [-7.07106781e-01]],
                [[-7.85055213e-17], [7.85055213e-17]],
            ]
        )
    }

    for key in mps[1].keys():
        assert all(abs(mps[1][key] - old_next_results_mpsR[key]) < 1e-8)

    for key in mps[2].keys():
        assert all(abs(mps[2][key] - old_next_results_mpsNextR[key]) < 1e-8)


def test_validation_theta_step_one_right():
    from numpy import array, all
    from copy import deepcopy

    mpsR = {(0, 1, 0): array([[[0.70710678], [0.70710678]]])}

    mpsL = {
        (2, 0, 0): array([[[-0.00260362]]]),
        (1, 1, 0): array(
            [[[-0.71250989], [-0.70163324]], [[-0.00363906], [0.00369547]]]
        ),
        (0, 2, 0): array([[[-0.00260362]]]),
    }

    old_theta, new_theta = get_theta()

    from pyfhmdot.algorithm import apply_gate_on_mm_at

    mps = [deepcopy(mpsL), deepcopy(mpsR)]
    gate = [deepcopy(old_theta)]
    apply_gate_on_mm_at(
        mps,
        gate,
        1,
        {"dw_one_serie": 0},
        100,
        1,
        1e-62,
        is_um=True,
        conserve_left_right_after_gate=False,
        direction_right=1,
    )
    # found the problem, the gate is wrong at border in the new code!!
    pass
