import numpy as _np

_real_t = "float64"
_cplx_t = "complex128"


def single_operator(name, coef):  # -> one bloc

    operators = {
        "sh_id_no": {(0, 0): coef * _np.array([[1, 0], [0, 1]], dtype=_real_t)},
        "sh_id_u1": {
            (1, 1): coef * _np.array([[1]], dtype=_real_t),
            (0, 0): coef * _np.array([[1]], dtype=_real_t),
        },
        "sh_sp_no": {(0, 0): coef * _np.array([[0, 1], [0, 0]], dtype=_real_t)},
        "sh_sp_u1": {(1, 0): coef * _np.array([[1]], dtype=_real_t)},
        "sh_sm_no": {(0, 0): coef * _np.array([[0, 0], [1, 0]], dtype=_real_t)},
        "sh_sm_u1": {(0, 1): coef * _np.array([[1]], dtype=_real_t)},
        "sh_sx_no": {(0, 0): coef * _np.array([[0, 1], [1, 0]], dtype=_real_t)},
        "sh_sx_u1": {
            (1, 0): coef * _np.array([[1]], dtype=_real_t),
            (0, 1): coef * _np.array([[1]], dtype=_real_t),
        },
        "sh_sz_no": {(0, 0): coef * _np.array([[1, 0], [0, -1]], dtype=_real_t)},
        "sh_sz_u1": {
            (0, 0): coef * _np.array([[1]], dtype=_real_t),
            (1, 1): coef * _np.array([[-1]], dtype=_real_t),
        },
        "sh_id_cplx_no": {(0, 0): coef * _np.array([[1, 0], [0, 1]], dtype=_cplx_t)},
        "sh_id_cplx_u1": {
            (1, 1): coef * _np.array([[1]], dtype=_cplx_t),
            (0, 0): coef * _np.array([[1]], dtype=_cplx_t),
        },
        "sh_sy_no": {(0, 0): coef * _np.array([[0, -1j], [1j, 0]], dtype=_cplx_t)},
        "sh_sy_u1": {
            (1, 0): coef * _np.array([[-1]], dtype=_cplx_t),
            (0, 1): coef * _np.array([[1j]], dtype=_cplx_t),
        },
    }

    return operators[name]


def two_sites_bond_operator(name, coef, weight_on_left=None):  # -> two blocs
    bonds = [
        "sh_id_no-sh_id_no",
        "sh_sm_no-sh_sp_no",
        "sh_sp_no-sh_sm_no",
        "sh_sx_no-sh_sx_no",
        "sh_sy_no-sh_sy_no",
        "sh_sz_no-sh_sz_no",
        "sh_id_u1-sh_id_u1",
        "sh_sm_u1-sh_sp_u1",
        "sh_sp_u1-sh_sm_u1",
        "sh_sz_u1-sh_sz_u1",
    ]
    if name in bonds:
        left_name, right_name = name.split("-")

        if weight_on_left is None:
            return single_operator(left_name, _np.sqrt(coef)), single_operator(
                right_name, _np.sqrt(coef)
            )
        elif weight_on_left:
            return single_operator(left_name, coef), single_operator(right_name, 1.0)
        else:
            return single_operator(left_name, 1.0), single_operator(right_name, coef)

    """
    # the above is ill defined with QN conservation
    "sh-SzoSz": {  # ok
        "nb_site": 2,
        0: "sh-Sz",
        1: "sh-Sz",
        "qchange": {
            "sh-None": [(0,), (0,)],
            "sh-U1": [(0,), (0,)],
            "sh-SU2": [(0, 0), (0, 0)],
        },
    },
    "sh-SpoSm": {  # ok
        "nb_site": 2,
        0: "sh-Sp",
        1: "sh-Sm",
        "qchange": {
            "sh-None": [(0,), (0,)],
            "sh-U1": [(+1,), (-1,)],
            "sh-SU2": [(0, +1), (0, -1)],
        },
    },
    "sh-SmoSp": {  # ok
        "nb_site": 2,
        0: "sh-Sm",
        1: "sh-Sp",
        "qchange": {
            "sh-None": [(0,), (0,)],
            "sh-U1": [(-1,), (+1,)],
            "sh-SU2": [(0, -1), (0, +1)],
        },
    },
    # the following is ill defined with QN conservation
    "sh-SxoSx": {
        "nb_site": 2,
        0: "sh-Sx",
        1: "sh-Sx",
        "qchange": {"sh-None": [(0,), (0,)]},
    },
    "sh-SyoSy": {
        "nb_site": 2,
        0: "sh-Sy",
        1: "sh-Sy",
        "qchange": {"sh-None": [(0,), (0,)]},
    },
    # the above is ill defined with QN conservation
    # -----------------------------------------------------------
    # ### so
    # ### PLEASE CHECK VERY CAREFULLY SINCE
    # # index [0] is |s=1,mz=-1> down
    # # index [1] is |s=1,mz=+0> "|0>"
    # # index [2] is |s=1,mz=+1> up
    # ##########################################
    "so-Id": {  # ok
        "nb_site": 1,
        "coef": _np.sqrt(3),
        "qBasis": {
            "so-None": [
                [
                    (0, 0),
                    (1 / _np.sqrt(3))
                    * _np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                                dtype=_real_t),
                ]
            ],
            "so-U1": [
                [(0, 0), _np.array([[1 / _np.sqrt(3)]], dtype=_real_t)],
                [(1, 1), _np.array([[1 / _np.sqrt(3)]], dtype=_real_t)],
                [(2, 2), _np.array([[1 / _np.sqrt(3)]], dtype=_real_t)],
            ],
            "so-SO3": [],
        },
        "qchange": {"so-None": [(0,)], "so-U1": [(0,)], "sh-SO3": [(0, 0)]},
    },
    "so-Sp": {  # ok
        "nb_site": 1,
        "coef": _np.sqrt(2),
        "qBasis": {
            "so-None": [
                [
                    (0, 0),
                    (1 / _np.sqrt(2))
                    * _np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]],
                                dtype=_real_t),
                ]
            ],
            "so-U1": [
                [(0, 1), _np.array([[(1 / (_np.sqrt(2)))]], dtype=_real_t)],
                [(1, 2), _np.array([[(1 / (_np.sqrt(2)))]], dtype=_real_t)],
            ],
            "so-SO3": [],
        },
        "qchange": {"so-None": [(0,)], "so-U1": [(+2,)], "sh-SO3": [(+2,)]},
    },
    "so-Sm": {  # ok
        "nb_site": 1,
        "coef": _np.sqrt(2),
        "qBasis": {
            "so-None": [
                [
                    (0, 0),
                    (1 / _np.sqrt(2))
                    * _np.array([[0, 1, 0], [0, 0, 1], [0, 0, 0]],
                                dtype=_real_t),
                ]
            ],
            "so-U1": [
                [(1, 0), _np.array([[(1 / (_np.sqrt(2)))]], dtype=_real_t)],
                [(2, 1), _np.array([[(1 / (_np.sqrt(2)))]], dtype=_real_t)],
            ],
            "so-SO3": [],
        },
        "qchange": {"so-None": [(0,)], "so-U1": [(-2,)], "sh-SO3": [(-2,)]},
    },
    "so-Sz": {  # ok
        "nb_site": 1,
        "coef": _np.sqrt(2),
        "qBasis": {
            "so-None": [
                [
                    (0, 0),
                    (1 / _np.sqrt(2))
                    * _np.array([[-1, 0, 0], [0, 0, 0],
                                [0, 0, 1]], dtype=_real_t),
                ]
            ],
            "so-U1": [
                [(0, 0), _np.array([[-1 / _np.sqrt(2)]], dtype=_real_t)],
                [(2, 2), _np.array([[1 / _np.sqrt(2)]], dtype=_real_t)],
            ],
            "so-SO3": [],
        },
        "qchange": {"so-None": [(0,)], "so-U1": [(0,)], "sh-SO3": [(0,)]},
    },
    "so-Sz^2": {  # ok (for single Ion anisotropy)
        "nb_site": 1,
        "coef": _np.sqrt(2),
        "qBasis": {
            "so-None": [
                [
                    (0, 0),
                    (1 / _np.sqrt(2))
                    * _np.array([[+1, 0, 0], [0, 0, 0],
                                [0, 0, +1]], dtype=_real_t),
                ]
            ],
            "so-U1": [
                [(0, 0), _np.array([[+1 / _np.sqrt(2)]], dtype=_real_t)],
                [(2, 2), _np.array([[+1 / _np.sqrt(2)]], dtype=_real_t)],
            ],
            "so-SO3": [],
        },
        "qchange": {"so-None": [(0,)], "so-U1": [(0,)], "sh-SO3": [(0,)]},
    },
    # the following is ill defined with QN conservation
    "so-Sx": {  # ok
        "nb_site": 1,
        "qchange": [[0, 0]],
        "coef": _np.sqrt(2),
        "qBasis": {
            "so-None": [
                [
                    (0, 0),
                    (1 / 2.0)
                    * _np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]],
                                dtype=_real_t),
                ]
            ]
        },
    },
    "so-Sy": {  # ok
        "nb_site": 1,
        "qchange": [[0, 0]],
        "coef": _np.sqrt(2),
        "qBasis": {
            "so-None": [
                [
                    (0, 0),
                    (1 / 2.0)
                    * _np.array([[0, 1j, 0], [-1j, 0, 1j],
                                [0, -1j, 0]], dtype=_cmpx_t),
                ]
            ]
        },
    },
    # the above is ill defined with QN conservation
    "so-IdoId": {
        "nb_site": 2,
        0: "so-Id",
        1: "so-Id",
        "qchange": {
            "so-None": [(0,), (0,)],
            "so-U1": [(0,), (0,)],
            "so-SO3": [(0,), (0,)],
        },
    },
    "so-SzoSz": {
        "nb_site": 2,
        0: "so-Sz",
        1: "so-Sz",
        "qchange": {
            "so-None": [(0,), (0,)],
            "so-U1": [(0,), (0,)],
            "so-SO3": [(0,), (0,)],
        },
    },
    "so-SpoSm": {
        "nb_site": 2,
        0: "so-Sp",
        1: "so-Sm",
        "qchange": {
            "so-None": [(0,), (0,)],
            "so-U1": [(+2,), (-2,)],
            "so-SO3": [(+2,), (-2,)],
        },
    },
    "so-SmoSp": {
        "nb_site": 2,
        0: "so-Sm",
        1: "so-Sp",
        "qchange": {
            "so-None": [(0,), (0,)],
            "so-U1": [(-2,), (+2,)],
            "so-SO3": [(-1,), (+1,)],
        },
    },
    # the following is ill defined with QN conservation
    "so-SxSx": {
        "nb_site": 2,
        0: "so-Sx",
        1: "so-Sx",
        "qchange": {"sh-None": [(0,), (0,)]},
    },
    "so-SySy": {
        "nb_site": 2,
        0: "so-Sy",
        1: "so-Sy",
        "qchange": {"sh-None": [(0,), (0,)]},
    },
    # the above is ill defined with QN conservation
    # -----------------------------------------------------------
    # ### ldsh=ladder spin half
    # # the numbers correspond to legs
    # ## ldsh-U1detached <<<<<<<<<<< PROBLEM! Sz_tot cons impossible
    # # 0 is |s1=1/2,mz1=-1/2>x|s2=1/2,mz2=-1/2>
    # # 1 is |s1=1/2,mz1=-1/2>x|s2=1/2,mz2=+1/2>
    # # 2 is |s1=1/2,mz1=+1/2>x|s2=1/2,mz2=-1/2>
    # # 3 is |s1=1/2,mz1=+1/2>x|s2=1/2,mz2=+1/2>
    # ## ldsh-U1comb => WORK!
    # # 0 is |s1=1/2,mz1=-1/2>x|s2=1/2,mz2=-1/2>
    # # 1 is |s1=1/2,mz1=-1/2>x|s2=1/2,mz2=+1/2>, |s1=1/2,mz1=+1/2>x|s2=1/2,mz2=-1/2>
    # # 2 is |s1=1/2,mz1=+1/2>x|s2=1/2,mz2=+1/2>
    ############################################
    # ### PLEASE CHECK VERY CAREFULLY SINCE
    "ldsh-Id": {  # ok
        "nb_site": 1,
        "coef": 2.0,
        "qBasis": {
            "ldsh-None": [
                [
                    (0, 0),
                    (1 / 2.0)
                    * _np.array(
                        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
                        dtype=_real_t,
                    ),
                ]
            ],
            "ldsh-U1detached": [
                [(0, 0), _np.array([[+1 / 2.0]], dtype=_real_t)],
                [(1, 1), _np.array([[+1 / 2.0]], dtype=_real_t)],
                [(2, 2), _np.array([[+1 / 2.0]], dtype=_real_t)],
                [(3, 3), _np.array([[+1 / 2.0]], dtype=_real_t)],
            ],
            "ldsh-U1comb": [
                [(0, 0), _np.array([[+1 / 2.0]], dtype=_real_t)],
                [(1, 1), _np.array([[+1 / 2.0, 0], [0, +1 / 2.0]], dtype=_real_t)],
                [(2, 2), _np.array([[+1 / 2.0]], dtype=_real_t)],
            ],
        },
        "qchange": {
            "ldsh-None": [(0,)],
            "ldsh-U1detached": [(0,)],
            "ldsh-U1comb": [(0,)],
        },
    },
    "ldsh-SzId": {  # ok
        "nb_site": 1,
        "coef": 1.0,
        "qBasis": {
            "ldsh-None": [
                [
                    (0, 0),
                    (1 / 2.0)
                    * _np.array(
                        [[-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
                        dtype=_real_t,
                    ),
                ]
            ],
            "ldsh-U1detached": [
                [(0, 0), _np.array([[-1 / 2.0]], dtype=_real_t)],
                [(1, 1), _np.array([[-1 / 2.0]], dtype=_real_t)],
                [(2, 2), _np.array([[+1 / 2.0]], dtype=_real_t)],
                [(3, 3), _np.array([[+1 / 2.0]], dtype=_real_t)],
            ],
            "ldsh-U1comb": [
                [(0, 0), _np.array([[-1 / 2.0]], dtype=_real_t)],
                [(1, 1), _np.array([[-1 / 2.0, 0], [0, +1 / 2.0]], dtype=_real_t)],
                [(2, 2), _np.array([[+1 / 2.0]], dtype=_real_t)],
            ],
        },
        "qchange": {
            "ldsh-None": [(0,)],
            "ldsh-U1detached": [(0,)],
            "ldsh-U1comb": [(0,)],
        },
    },
    "ldsh-IdSz": {  # ok
        "nb_site": 1,
        "coef": 1.0,
        "qBasis": {
            "ldsh-None": [
                [
                    (0, 0),
                    (1 / 2.0)
                    * _np.array(
                        [[-1, 0, 0, 0], [0, +1, 0, 0],
                            [0, 0, -1, 0], [0, 0, 0, +1]],
                        dtype=_real_t,
                    ),
                ]
            ],
            "ldsh-U1detached": [
                [(0, 0), _np.array([[-1 / 2.0]], dtype=_real_t)],
                [(1, 1), _np.array([[+1 / 2.0]], dtype=_real_t)],
                [(2, 2), _np.array([[-1 / 2.0]], dtype=_real_t)],
                [(3, 3), _np.array([[+1 / 2.0]], dtype=_real_t)],
            ],
            "ldsh-U1comb": [
                [(0, 0), _np.array([[-1 / 2.0]], dtype=_real_t)],
                [(1, 1), _np.array([[+1 / 2.0, 0], [0, -1 / 2.0]], dtype=_real_t)],
                [(2, 2), _np.array([[+1 / 2.0]], dtype=_real_t)],
            ],
        },
        "qchange": {
            "ldsh-None": [(0,)],
            "ldsh-U1detached": [(0,)],
            "ldsh-U1comb": [(0,)],
        },
    },
    "ldsh-SzSz": {  # ok
        "nb_site": 1,
        "coef": 1 / 2.0,
        "qBasis": {
            "ldsh-None": [
                [
                    (0, 0),
                    (1 / 2.0)
                    * _np.array(
                        [[+1, 0, 0, 0], [0, -1, 0, 0],
                            [0, 0, -1, 0], [0, 0, 0, +1]],
                        dtype=_real_t,
                    ),
                ]
            ],
            "ldsh-U1detached": [
                [(0, 0), _np.array([[+1 / 2.0]], dtype=_real_t)],
                [(1, 1), _np.array([[-1 / 2.0]], dtype=_real_t)],
                [(2, 2), _np.array([[-1 / 2.0]], dtype=_real_t)],
                [(3, 3), _np.array([[+1 / 2.0]], dtype=_real_t)],
            ],
            "ldsh-U1comb": [
                [(0, 0), _np.array([[+1 / 2.0]], dtype=_real_t)],
                [(1, 1), _np.array([[-1 / 2.0, 0], [0, -1 / 2.0]], dtype=_real_t)],
                [(2, 2), _np.array([[+1 / 2.0]], dtype=_real_t)],
            ],
        },
        "qchange": {
            "ldsh-None": [(0,)],
            "ldsh-U1detached": [(0,)],
            "ldsh-U1comb": [(0,)],
        },
    },
    "ldsh-SpId": {  # ok
        "nb_site": 1,
        "coef": _np.sqrt(2),
        "qBasis": {
            "ldsh-None": [
                [
                    (0, 0),
                    (1 / _np.sqrt(2))
                    * _np.array(
                        [[0, 0, 0, 0], [0, 0, 0, 0], [+1, 0, 0, 0], [0, +1, 0, 0]],
                        dtype=_real_t,
                    ),
                ]
            ],
            "ldsh-U1detached": [
                [(2, 0), _np.array([[+1 / _np.sqrt(2)]], dtype=_real_t)],
                [(3, 1), _np.array([[+1 / _np.sqrt(2)]], dtype=_real_t)],
            ],
            "ldsh-U1comb": [
                [(1, 0), _np.array([[0], [+1 / _np.sqrt(2)]], dtype=_real_t)],
                [(2, 1), _np.array([[+1 / _np.sqrt(2), 0]], dtype=_real_t)],
            ],
        },
        "qchange": {
            "ldsh-None": [(0,)],
            "ldsh-U1detached": [(2,)],
            "ldsh-U1comb": [(2,)],
        },
    },
    "ldsh-IdSp": {  # ok
        "nb_site": 1,
        "coef": _np.sqrt(2),
        "qBasis": {
            "ldsh-None": [
                [
                    (0, 0),
                    (1 / _np.sqrt(2))
                    * _np.array(
                        [[0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 0]],
                        dtype=_real_t,
                    ),
                ]
            ],
            "ldsh-U1detached": [
                [(1, 0), _np.array([[+1 / _np.sqrt(2)]], dtype=_real_t)],
                [(3, 2), _np.array([[+1 / _np.sqrt(2)]], dtype=_real_t)],
            ],
            "ldsh-U1comb": [
                [(1, 0), _np.array([[+1 / _np.sqrt(2)], [0]], dtype=_real_t)],
                [(2, 1), _np.array([[0, +1 / _np.sqrt(2)]], dtype=_real_t)],
            ],
        },
        "qchange": {
            "ldsh-None": [(0,)],
            "ldsh-U1detached": [(2,)],
            "ldsh-U1comb": [(2,)],
        },
    },
    "ldsh-SmId": {  # ok
        "nb_site": 1,
        "coef": _np.sqrt(2),
        "qBasis": {
            "ldsh-None": [
                [
                    (0, 0),
                    (1 / _np.sqrt(2))
                    * _np.array(
                        [[0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
                        dtype=_real_t,
                    ),
                ]
            ],
            "ldsh-U1detached": [
                [(0, 2), _np.array([[+1 / _np.sqrt(2)]], dtype=_real_t)],
                [(1, 3), _np.array([[+1 / _np.sqrt(2)]], dtype=_real_t)],
            ],
            "ldsh-U1comb": [
                [(0, 1), _np.array([[0, +1 / _np.sqrt(2)]], dtype=_real_t)],
                [(1, 2), _np.array([[+1 / _np.sqrt(2)], [0]], dtype=_real_t)],
            ],
        },
        "qchange": {
            "ldsh-None": [(0,)],
            "ldsh-U1detached": [(-2,)],
            "ldsh-U1comb": [(-2,)],
        },
    },
    "ldsh-IdSm": {  # ok
        "nb_site": 1,
        "coef": _np.sqrt(2),
        "qBasis": {
            "ldsh-None": [
                [
                    (0, 0),
                    (1 / _np.sqrt(2))
                    * _np.array(
                        [[0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 0]],
                        dtype=_real_t,
                    ),
                ]
            ],
            "ldsh-U1detached": [
                [(0, 1), _np.array([[+1 / _np.sqrt(2)]], dtype=_real_t)],
                [(2, 3), _np.array([[+1 / _np.sqrt(2)]], dtype=_real_t)],
            ],
            "ldsh-U1comb": [
                [(0, 1), _np.array([[+1 / _np.sqrt(2), 0]], dtype=_real_t)],
                [(1, 2), _np.array([[0], [+1 / _np.sqrt(2)]], dtype=_real_t)],
            ],
        },
        "qchange": {
            "ldsh-None": [(0,)],
            "ldsh-U1detached": [(-2,)],
            "ldsh-U1comb": [(-2,)],
        },
    },
    "ldsh-SpSp": {  # ok
        "nb_site": 1,
        "coef": 1,
        "qBasis": {
            "ldsh-None": [
                [
                    (0, 0),
                    _np.array(
                        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0]],
                        dtype=_real_t,
                    ),
                ]
            ],
            "ldsh-U1detached": [[(3, 0), _np.array([[+1]], dtype=_real_t)]],
            "ldsh-U1comb": [[(2, 0), _np.array([[+1]], dtype=_real_t)]],
        },
        "qchange": {
            "ldsh-None": [(0,)],
            "ldsh-U1detached": [(+4,)],
            "ldsh-U1comb": [(+4,)],
        },
    },
    "ldsh-SmSm": {  # ok
        "nb_site": 1,
        "coef": 1,
        "qBasis": {
            "ldsh-None": [
                [
                    (0, 0),
                    _np.array(
                        [[0, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                        dtype=_real_t,
                    ),
                ]
            ],
            "ldsh-U1detached": [[(0, 3), _np.array([[+1]], dtype=_real_t)]],
            "ldsh-U1comb": [[(0, 2), _np.array([[+1]], dtype=_real_t)]],
        },
        "qchange": {
            "ldsh-None": [(0,)],
            "ldsh-U1detached": [(-4,)],
            "ldsh-U1comb": [(-4,)],
        },
    },
    "ldsh-SpSm": {  # ok
        "nb_site": 1,
        "qchange": [[0, 0]],
        "coef": 1,
        "qBasis": {
            "ldsh-None": [
                [
                    (0, 0),
                    _np.array(
                        [[0, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                        dtype=_real_t,
                    ),
                ]
            ],
            "ldsh-U1detached": [[(1, 2), _np.array([[+1]], dtype=_real_t)]],
            "ldsh-U1comb": [[(1, 1), _np.array([[0, +1], [0, 0]], dtype=_real_t)]],
        },
        "qchange": {
            "ldsh-None": [(0,)],
            "ldsh-U1detached": [(0,)],
            "ldsh-U1comb": [(0,)],
        },
    },
    "ldsh-SmSp": {  # ok
        "nb_site": 1,
        "coef": 1,
        "qBasis": {
            "ldsh-None": [
                [
                    (0, 0),
                    _np.array(
                        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]],
                        dtype=_real_t,
                    ),
                ]
            ],
            "ldsh-U1detached": [[(2, 1), _np.array([[+1]], dtype=_real_t)]],
            "ldsh-U1comb": [[(1, 1), _np.array([[0, 0], [+1, 0]], dtype=_real_t)]],
        },
        "qchange": {
            "ldsh-None": [(0,)],
            "ldsh-U1detached": [(0,)],
            "ldsh-U1comb": [(0,)],
        },
    },
    "ldsh-SzIdoSzId": {  # ok
        "nb_site": 2,
        0: "ldsh-SzId",
        1: "ldsh-SzId",
        "qchange": {
            "ldsh-None": [(0,), (0,)],
            "ldsh-U1detached": [(0,), (0,)],
            "ldsh-U1comb": [(0,), (0,)],
        },
    },
    "ldsh-IdSzoIdSz": {  # ok
        "nb_site": 2,
        0: "ldsh-IdSz",
        1: "ldsh-IdSz",
        "qchange": {
            "ldsh-None": [(0,), (0,)],
            "ldsh-U1detached": [(0,), (0,)],
            "ldsh-U1comb": [(0,), (0,)],
        },
    },
    "ldsh-SzIdoIdSz": {  # ok
        "nb_site": 2,
        0: "ldsh-SzId",
        1: "ldsh-IdSz",
        "qchange": {
            "ldsh-None": [(0,), (0,)],
            "ldsh-U1detached": [(0,), (0,)],
            "ldsh-U1comb": [(0,), (0,)],
        },
    },
    "ldsh-IdSzoSzId": {  # ok
        "nb_site": 2,
        0: "ldsh-IdSz",
        1: "ldsh-SzId",
        "qchange": {
            "ldsh-None": [(0,), (0,)],
            "ldsh-U1detached": [(0,), (0,)],
            "ldsh-U1comb": [(0,), (0,)],
        },
    },
    "ldsh-SpIdoSmId": {
        "nb_site": 2,
        0: "ldsh-SpId",
        1: "ldsh-SmId",
        "qchange": {
            "ldsh-None": [(0,), (0,)],
            "ldsh-U1detached": [(+2,), (-2,)],
            "ldsh-U1comb": [(+2,), (-2,)],
        },
    },
    "ldsh-IdSpoIdSm": {
        "nb_site": 2,
        0: "ldsh-IdSp",
        1: "ldsh-IdSm",
        "qchange": {
            "ldsh-None": [(0,), (0,)],
            "ldsh-U1detached": [(+2,), (-2,)],
            "ldsh-U1comb": [(+2,), (-2,)],
        },
    },
    "ldsh-SpIdoIdSm": {
        "nb_site": 2,
        0: "ldsh-SpId",
        1: "ldsh-IdSm",
        "qchange": {
            "ldsh-None": [(0,), (0,)],
            "ldsh-U1detached": [(+2,), (-2,)],
            "ldsh-U1comb": [(+2,), (-2,)],
        },
    },
    "ldsh-IdSpoSmId": {
        "nb_site": 2,
        0: "ldsh-IdSp",
        1: "ldsh-SmId",
        "qchange": {
            "ldsh-None": [(0,), (0,)],
            "ldsh-U1detached": [(+2,), (-2,)],
            "ldsh-U1comb": [(+2,), (-2,)],
        },
    },
    "ldsh-SmIdoSpId": {
        "nb_site": 2,
        0: "ldsh-SmId",
        1: "ldsh-SpId",
        "qchange": {
            "ldsh-None": [(0,), (0,)],
            "ldsh-U1detached": [(-2,), (+2,)],
            "ldsh-U1comb": [(-2,), (+2,)],
        },
    },
    "ldsh-IdSmoIdSp": {
        "nb_site": 2,
        0: "ldsh-IdSm",
        1: "ldsh-IdSp",
        "qchange": {
            "ldsh-None": [(0,), (0,)],
            "ldsh-U1detached": [(-2,), (+2,)],
            "ldsh-U1comb": [(-2,), (+2,)],
        },
    },
    "ldsh-SmIdoIdSp": {
        "nb_site": 2,
        0: "ldsh-SmId",
        1: "ldsh-IdSp",
        "qchange": {
            "ldsh-None": [(0,), (0,)],
            "ldsh-U1detached": [(-2,), (+2,)],
            "ldsh-U1comb": [(-2,), (+2,)],
        },
    },
    "ldsh-IdSmoSpId": {
        "nb_site": 2,
        0: "ldsh-IdSm",
        1: "ldsh-SpId",
        "qchange": {
            "ldsh-None": [(0,), (0,)],
            "ldsh-U1detached": [(-2,), (+2,)],
            "ldsh-U1comb": [(-2,), (+2,)],
        },
    },
    # ### the following is ill defined with QN conservation
    # 'ldsh-SxSx' :
    #     {'nb_site' : 2, 'qchange' : [[0,(+1,-1)],[(+1,-1),(+2,0,-2)]],
    #      0 : 'ldsh-Sx', 1 : 'ldsh-Sx' },
    # 'ldsh-SySy' :
    #     {'nb_site' : 2, 'qchange' : [[0,(+1,-1)],[(+1,-1),(+2,0,-2)]],
    #      0 : 'ldsh-Sy', 1 : 'ldsh-Sy' },
    # # ### ldsc=ladder spin half STRONG COUPLING
    # # # 0 is ld singlet s0=|s=+1,mz=+0>
    # # # 1 is ld triplet t-=|s=+1,mz=-1>
    # # # 2 is ld triplet t0=|s=+1,mz=+0>
    # # # 3 is ld triplet t+=|s=+1,mz=+1>
    #     'ldshSC-Id' :
    #         {'nb_site' : 1, 'qchange' : [[0,0]], 'coef' : 2. ,
    #          'qBasis' :
    #            { 'ldsh-None' : [[(0,0), (1/2.)*_np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],dtype=_real_t)]] ,
    #              'ldsh-U1detached' : [[(0,0), _np.array([[+1/2.]],dtype=_real_t)],
    #                         [(1,1), _np.array([[+1/2.]],dtype=_real_t)],
    #                         [(2,2), _np.array([[+1/2.]],dtype=_real_t)],
    #                         [(3,3), _np.array([[+1/2.]],dtype=_real_t)]]
    #            }
    #      },
    "skeleton": {"qcons_compatibility": ["None"], "nb_site": 0, "qchange": []},

    """
    return operators


"""


# the doubled system is always the difference of the two qns (not the sum!!)
basis = {  #
    "sh-None": {
        "zero": [(0,)],
        "qn": [(0,)],
        "deg": [2],
        "2qn": [(0,)],
        "2deg": [4],
        "map": [[(0, 0)], [0], [slice(0, 4)]],
    },  # Nothing
    "sh-U1": {
        "zero": [(0,)],
        "qn": [(-1,), (1,)],
        "deg": [1, 1],
        "2qn": [(-2,), (0,), (2,)],
        "2deg": [1, 2, 1],
        "map": [
            [(0, 0), (0, 1), (1, 0), (1, 1)],
            [1, 0, 2, 1],
            [slice(0, 1), slice(0, 1), slice(0, 1), slice(1, 2)],
        ],
    },  # S^z_tot
    "sh-SU2": {
        "zero": [(0, 0)],
        "qn": [(1, -1), (1, 1)],
        "deg": [1, 1],
        "2qn": [(2, -2), ((2, 0), 0), (2, 2)],
        "2deg": [1, 2, 1],
        "map": [((0, 0), 1), ((1, 1), 1), ((0, 1), 0), ((1, 0), 2)],
        "slices": [
            [(0, slice(0, 1)), (1, slice(1, 2))],
            [(0, slice(0, 1)), (1, slice(1, 2))],
        ],
    },  # S^2, S^z_tot
    #
    #
    #
    "so-None": {
        "zero": [(0,)],
        "qn": [(0,)],
        "deg": [3],
        "2qn": [(0,)],
        "2deg": [9],
        "map": [[(0, 0)], [0], [slice(0, 9)]],
    },
    "so-U1": {
        "zero": [(0,)],
        "qn": [(-2,), (0,), (2,)],
        "deg": [1, 1, 1],
        "2qn": [(-4,), (-2,), (0,), (+2,), (+4,)],
        "2deg": [1, 2, 3, 2, 1],
        "map": [
            [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1),
              (1, 2), (2, 0), (2, 1), (2, 2)],
            [2, 1, 0, 3, 2, 1, 4, 3, 2],
            [
                slice(0, 1),
                slice(0, 1),
                slice(0, 1),
                slice(0, 1),
                slice(1, 2),
                slice(1, 2),
                slice(0, 1),
                slice(1, 2),
                slice(2, 3),
            ],
        ],
    },  # S^z_tot
    # 'so-SO3'  : {'zero' : [(0,)], 'qn' : [(0,)], 'deg' : [3], '2qn' : [(0,)], '2deg' : [9] , 'map' : [[(0,0)],[0],[slice(0,9)]] },
    #
    #
    #
    "ldsh-None": {
        "zero": [(0,)],
        "qn": [(0,)],
        "deg": [4],
        "2qn": [(0,)],
        "2deg": [16],
        "map": [[(0, 0)], [0], [slice(0, 16)]],
    },
    # the one working is ============================
    "ldsh-U1comb": {
        "zero": [(0,)],
        "qn": [(-2,), (0,), (+2,)],
        "deg": [1, 2, 1],
        "2qn": [(-4,), (-2,), (0,), (+2,), (+4,)],
        "2deg": [1, 4, 6, 4, 1],
        "map": [
            [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1),
              (1, 2), (2, 0), (2, 1), (2, 2)],
            [2, 1, 0, 3, 2, 1, 4, 3, 2],
            [
                slice(0, 1),
                slice(0, 2),
                slice(0, 1),
                slice(0, 2),
                slice(1, 5),
                slice(2, 4),
                slice(0, 1),
                slice(2, 4),
                slice(5, 6),
            ],
        ],
    },
    # attempt detached do not work =========================
    "ldsh-SU2detached": {
        "zero": [(0, 0)],
        "qn": [(-1, -1), (-1, +1), (+1, -1), (+1, +1)],
        "deg": [1, 1, 1, 1],
        "2qn": [
            (-2, -2),
            (-2, 0),
            (-2, 2),
            (0, -2),
            (0, 0),
            (0, 2),
            (2, -2),
            (2, 0),
            (2, 2),
        ],
        "2deg": [1, 2, 1, 2, 4, 2, 1, 2, 1],
        "map": [
            [
                (0, 0),
                (0, 1),
                (0, 2),
                (0, 3),
                (1, 0),
                (1, 1),
                (1, 2),
                (1, 3),
                (2, 0),
                (2, 1),
                (2, 2),
                (2, 3),
                (3, 0),
                (3, 1),
                (3, 2),
                (3, 3),
            ],
            [0, 1, 1, 2, 3, 4, 4, 5, 3, 4, 4, 5, 6, 7, 7, 8],
            [
                slice(0, 1),
                slice(0, 1),
                slice(1, 2),
                slice(0, 1),
                slice(0, 1),
                slice(0, 1),
                slice(1, 2),
                slice(0, 1),
                slice(1, 2),
                slice(2, 3),
                slice(3, 4),
                slice(1, 2),
                slice(0, 1),
                slice(0, 1),
                slice(1, 2),
                slice(0, 1),
            ],
        ],
    },
    # 'b2-None' : {},
    # 'fls-None' : {},
    # 'ffs-None' : {},
    # 'ldso-None' : {'zero' : [(0,)], 'qn' : [(0,)], 'deg' : [9], '2qn' : [(0,)], '2deg' : [81] , 'map' : [[(0,0)],[0],[slice(0,81)]] },
    "skeleton": {
        "zero": ["neutral QN"],
        "qn": ["pure state QN"],
        "deg": ["int"],
        "2qn": ["mixed state QN"],
        "2deg": ["int**2"],
        "map": [["pair of pure QN"], ["mixed QN"], ["slice"]],
    },
}


_real_t = "float64"
_cmpx_t = "complex128"

global quantum_name

# 0, ('M', 1./2.), (Sz,0)   => param[0]/2.*Sz    for all sites
# ### 3, ('MR', 1./2.)   => [_/2. for param[3] is list]
# 1, ('EXP', 1./2.,2.j) => np.exp(2.j*param[1])/2.



################################################################################
################################################################################
################################################################################

"""
