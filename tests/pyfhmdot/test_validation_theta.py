import pytest

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
    return old_theta, new_theta


def test_validation_theta_step_two_left():
    from numpy import array, all
    from copy import deepcopy

    mpsL = {}
    mpsL[(0, 1, 0)] = array(
        [[[-7.07106781e-01], [-7.07106781e-01]], [[-5.55111512e-17], [5.55111512e-17]]]
    )

    mpsR = {}
    mpsR[(0, 1, 0)] = array([[[0.70710678], [0.70710678]]])

    old_theta, new_theta = get_theta()

    assert len(old_theta) == 19 and len(new_theta) == 19

    for key in old_theta:
        assert all(old_theta[key] == new_theta[key][::-1, ::-1, ::-1, ::-1])

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
    for key in mps[0].keys():
        assert all(abs(mps[0][key] - old_results_mpsL[key]) < 1e-8)

    for key in mps[1].keys():
        assert all(abs(mps[1][key] - old_results_mpsR[key]) < 1e-8)


def test_validation_theta_step_one_right():
    from numpy import array, all

    mpsR = {(0, 1, 0): array([[[0.70710678], [0.70710678]]])}

    mpsL = {
        (2, 0, 0): array([[[-0.00260362]]]),
        (1, 1, 0): array(
            [[[-0.71250989], [-0.70163324]], [[-0.00363906], [0.00369547]]]
        ),
        (0, 2, 0): array([[[-0.00260362]]]),
    }
    pass
