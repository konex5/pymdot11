import numpy as _np

_real_t = "float64"
_cmpx_t = "complex128"


def single_operator_dense(name, coef):

    operators = (
        {
            "sh_id_no": [((0, 0), coef * _np.array([[1, 0], [0, 1]], dtype=_real_t))],
            "sh_id_u1": [
                ((1, 1), coef * _np.array([[1]], dtype=_real_t)),
                ((0, 0), coef * _np.array([[1]], dtype=_real_t)),
            ],
            "sh_sp_no": [[(0, 0), _np.array([[0, 1], [0, 0]], dtype=_real_t)]],
            "sh_sp_u1": [[(1, 0), _np.array([[1]], dtype=_real_t)]],
        },
    )
    """
    },
    "sh-Sm": {  # ok
        "nb_site": 1,
        "coef": float(1),
        "qBasis": {
            "sh-None": [[(0, 0), _np.array([[0, 1], [0, 0]], dtype=_real_t)]],
            "sh-U1": [[(0, 1), _np.array([[1]], dtype=_real_t)]],
            "sh-SU2": [[(0, 1), _np.array([[1]], dtype=_real_t)]],
        },
        "qchange": {"sh-None": [(0,)], "sh-U1": [(-1,)], "sh-SU2": [(0, -1)]},
    },
    "sh-Sz": {  # ok
        "nb_site": 1,
        "coef": (1 / _np.sqrt(2)),
        "qBasis": {
            "sh-None": [
                [
                    (0, 0),
                    _np.array(
                        [[-1 / _np.sqrt(2), 0], [0, +1 / _np.sqrt(2)]], dtype=_real_t
                    ),
                ]
            ],
            "sh-U1": [
                [(1, 1), _np.array([[+1 / _np.sqrt(2)]], dtype=_real_t)],
                [(0, 0), _np.array([[-1 / _np.sqrt(2)]], dtype=_real_t)],
            ],
            "sh-SU2": [
                [(1, 1), _np.array([[+1 / _np.sqrt(2)]], dtype=_real_t)],
                [(0, 0), _np.array([[-1 / _np.sqrt(2)]], dtype=_real_t)],
            ],
        },
        "qchange": {"sh-None": [(0,)], "sh-U1": [(0,)], "sh-SU2": [(0, 0)]},
    },
    ### the below is ill defined with QN conservation
    "sh-Sx": {
        "nb_site": 1,
        "qchange": [[0, (+1, -1)]],
        "coef": (1 / _np.sqrt(2)),
        "qBasis": {
            "sh-None": [
                [
                    (0, 0),
                    _np.array(
                        [[0, +1 / _np.sqrt(2)], [+1 / _np.sqrt(2), 0]], dtype=_real_t
                    ),
                ]
            ]
        },
    },
    "sh-Sy": {
        "nb_site": 1,
        "qchange": [[0, (+1, -1)]],
        "coef": (1 / _np.sqrt(2)),
        "qBasis": {
            "sh-None": [
                [
                    (0, 0),
                    _np.array(
                        [[0, +1j / _np.sqrt(2)], [-1j / _np.sqrt(2), 0]], dtype=_cmpx_t
                    ),
                ]
            ]
        },
    },
    ### the above is ill defined with QN conservation
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
    ### the following is ill defined with QN conservation
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
    ### the above is ill defined with QN conservation
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
                    * _np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=_real_t),
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
                    * _np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=_real_t),
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
                    * _np.array([[0, 1, 0], [0, 0, 1], [0, 0, 0]], dtype=_real_t),
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
                    * _np.array([[-1, 0, 0], [0, 0, 0], [0, 0, 1]], dtype=_real_t),
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
                    * _np.array([[+1, 0, 0], [0, 0, 0], [0, 0, +1]], dtype=_real_t),
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
    ### the following is ill defined with QN conservation
    "so-Sx": {  # ok
        "nb_site": 1,
        "qchange": [[0, 0]],
        "coef": _np.sqrt(2),
        "qBasis": {
            "so-None": [
                [
                    (0, 0),
                    (1 / 2.0)
                    * _np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=_real_t),
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
                    * _np.array([[0, 1j, 0], [-1j, 0, 1j], [0, -1j, 0]], dtype=_cmpx_t),
                ]
            ]
        },
    },
    ### the above is ill defined with QN conservation
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
    ### the following is ill defined with QN conservation
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
    ### the above is ill defined with QN conservation
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
                        [[-1, 0, 0, 0], [0, +1, 0, 0], [0, 0, -1, 0], [0, 0, 0, +1]],
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
                        [[+1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, +1]],
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
            [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
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
            [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
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


hamiltonian = {
    # ### SKELETON
    "skeleton": {
        "nb_param": "list_param",
        "qname_ideal": "qn_model_alone",
        "qname_allowed": "qname_allowed",
        "period": "ham_periodicity",
        "submodel": "list_of_submodel",
        "ham_expr": "expression_to_add__1-ONSITE__2-NEAREST_NEIGHBOR__3-SPECIAL-SITE__4-SPECIAL-BOND",
    },
    # ### sh-so CHAINS
    "hx": {
        "nb_param": 1,
        "qname_ideal": ["None", (1,)],
        "qname_allowed": ["None"],
        "period": 1,
        "submodel": [],
        "ham_expr": [[(("M", -1.0, 0), ("Sx", 0))], [], [], []],
    },
    "hz": {
        "nb_param": 1,
        "qname_ideal": ["U1", (1,)],
        "qname_allowed": ["None", "U1"],
        "period": 1,
        "submodel": [],
        "ham_expr": [[(("M", -1.0, 0), ("Sz", 0))], [], [], []],
    },
    # 'hzR' : {'nb_param' : 1, 'qname_ideal' : ['U1', (1,)],'qname_allowed' : ['None','U1'], 'period' : -1,
    #     'submodel' : [],
    #     'ham_expr' : [ [( 0, ('MR', [-1.] ), ('Sz', 0))], [], [], [] ] },
    "xy": {
        "nb_param": 1,
        "qname_ideal": ["SU2", (2,)],
        "qname_allowed": ["None", "U1", "SU2"],
        "period": 1,
        "submodel": [],
        "ham_expr": [
            [],
            [(("M", 1.0 / 2.0, 0), ("SpoSm", 0)), (("M", 1.0 / 2.0, 0), ("SmoSp", 0))],
            [],
            [],
        ],
    },
    # 'xy-2site' : {'nb_param' : 1, 'qname_ideal' : ['SU2', (2,)],'qname_allowed' : ['None','U1','SU2'], 'period' : 2,
    #     'submodel' : [],
    #     'ham_expr' : [ [], [], [( 0, ('M', [1./2.]), ('SpoSm', 0)),(0, ('M', 1./2.),('SmoSp', 0))], []] },
    "xydimer": {
        "nb_param": 2,
        "qname_ideal": ["SU2", (2,)],
        "qname_allowed": ["None", "U1", "SU2"],
        "period": 2,
        "submodel": [],
        "ham_expr": [
            [],
            [
                (("M", 1.0 / 2.0, 0), ("SpoSm", 0)),
                (("M", 1.0 / 2.0, 0), ("SmoSp", 0)),
                (("M", 1.0 / 2.0, 1), ("SpoSm", 1)),
                (("M", 1.0 / 2.0, 1), ("SmoSp", 1)),
            ],
            [],
            [],
        ],
    },
    "xyflux": {
        "nb_param": 1,
        "qname_ideal": ["SU2", (2,)],
        "qname_allowed": ["None", "U1", "SU2"],
        "period": 1,
        "submodel": [],
        "ham_expr": [
            [],
            [
                (("EXP", [1.0 / 2.0, +1.0j], [0, 1]), ("SpoSm", 0)),
                (("EXP", [1.0 / 2.0, -1.0j], [0, 1]), ("SmoSp", 0)),
            ],
            [],
            [],
        ],
    },
    "zz": {
        "nb_param": 1,
        "qname_ideal": ["SU2", (2,)],
        "qname_allowed": ["None", "U1", "SU2"],
        "period": 1,
        "submodel": [],
        "ham_expr": [[], [(("M", 1.0, 0), ("SzoSz", 0))], [], []],
    },
    "zz2sites": {
        "nb_param": 1,
        "qname_ideal": ["SU2", (2,)],
        "qname_allowed": ["None", "U1", "SU2"],
        "period": 1,
        "submodel": [],
        "ham_expr": [[], [(("M", 1.0, 0), ("SzoSz", 0))], [], []],
    },
    "zzdimer": {
        "nb_param": 2,
        "qname_ideal": ["SU2", (2,)],
        "qname_allowed": ["None", "U1", "SU2"],
        "period": 2,
        "submodel": [],
        "ham_expr": [
            [],
            [(("M", 1.0, 0), ("SzoSz", 0)), (("M", 1.0, 1), ("SzoSz", 1))],
            [],
            [],
        ],
    },
    "SxLEFT": {
        "nb_param": 1,
        "qname_ideal": ["SU2", (2,)],
        "qname_allowed": ["None", "U1", "SU2"],
        "period": -1,
        "submodel": [],
        "ham_expr": [
            [],
            [],
            [
                (("M", 1.0, 0), ("Sp", ("LEFT", 0))),
                (("M", 1.0, 0), ("Sm", ("LEFT", 0))),
            ],
            [],
        ],
    },
    "SxRIGHT": {
        "nb_param": 1,
        "qname_ideal": ["SU2", (2,)],
        "qname_allowed": ["None", "U1", "SU2"],
        "period": -1,
        "submodel": [],
        "ham_expr": [
            [],
            [],
            [
                (("M", 1.0, 0), ("Sp", ("RIGHT", 0))),
                (("M", 1.0, 0), ("Sm", ("RIGHT", 0))),
            ],
            [],
        ],
    },
    "SxMIDDLE": {
        "nb_param": 1,
        "qname_ideal": ["SU2", (2,)],
        "qname_allowed": ["None", "U1", "SU2"],
        "period": -1,
        "submodel": [],
        "ham_expr": [
            [],
            [],
            [
                (("M", 1.0, 0), ("Sp", ("MIDDLE", 0))),
                (("M", 1.0, 0), ("Sm", ("MIDDLE", 0))),
            ],
            [],
        ],
    },
    "ionanisotropy": {
        "nb_param": 1,
        "qname_ideal": ["U1", (1,)],
        "qname_allowed": ["None", "U1"],
        "period": 1,
        "submodel": [],
        "ham_expr": [[(("M", +1.0, 0), ("Sz^2", 0))], [], [], []],
    },
    # ### model
    # 'ising' : {'nb_param' : 2, 'qname_ideal' : ['U1', (1,)],'qname_allowed' : ['None','U1'], 'period' : 1,
    #     'submodel' : [('xx',[0]),('hz',[1])],
    #     'ham_expr' : [ [], [], [], [] ] },
    "xxx": {
        "nb_param": 1,
        "qname_ideal": ["SU2", (2,)],
        "qname_allowed": ["None", "U1"],
        "period": 1,
        "submodel": [("xy", [0]), ("zz", [0])],
        "ham_expr": [[], [], [], []],
    },
    "xxz": {
        "nb_param": 2,
        "qname_ideal": ["SU2", (2,)],
        "qname_allowed": ["None", "U1"],
        "period": 1,
        "submodel": [("xy", [0]), ("zz", [1])],
        "ham_expr": [[], [], [], []],
    },
    "xxz-hz": {
        "nb_param": 3,
        "qname_ideal": ["U1", (1,)],
        "qname_allowed": ["None", "U1"],
        "period": 1,
        "submodel": [("xxz", [0, 1]), ("hz", [2])],
        "ham_expr": [[], [], [], []],
    },
    # 'xxz-hzN' : {'nb_param' : 3, 'qname_ideal' : ['None', (1,)],'qname_allowed' : ['None','U1'], 'period' : 1,
    #     'submodel' : [('xxz',[0,1]),('hz',[2])],
    #     'ham_expr' : [ [], [], [], [] ] },
    "xxx-dimer": {
        "nb_param": 2,
        "qname_ideal": ["SU2", (2,)],
        "qname_allowed": ["None", "U1", "SU2"],
        "period": 1,
        "submodel": [("xydimer", [0, 1]), ("zzdimer", [0, 1])],
        "ham_expr": [[], [], [], []],
    },
    "xxx-dimer-hz": {
        "nb_param": 3,
        "qname_ideal": ["U1", (2,)],
        "qname_allowed": ["None", "U1"],
        "period": 1,
        "submodel": [("xydimer", [0, 1]), ("zzdimer", [0, 1]), ("hz", [2])],
        "ham_expr": [[], [], [], []],
    },
    "xxz-SxBord": {
        "nb_param": 3,
        "qname_ideal": ["SU2", (2,)],
        "qname_allowed": ["None", "U1"],
        "period": 1,
        "submodel": [("xy", [0]), ("zz", [1]), ("SxRIGHT", [2]), ("SxLEFT", [2])],
        "ham_expr": [[], [], [], []],
    },
    # ### so spin ONE
    "xxz-Dz-hz": {
        "nb_param": 4,
        "qname_ideal": ["U1", (2,)],
        "qname_allowed": ["None", "U1"],
        "period": 1,
        "submodel": [("xxz", [0, 1]), ("ionanisotropy", [2]), ("hz", [3])],
        "ham_expr": [[], [], [], []],
    },
    "xxx-Dz-hz": {
        "nb_param": 3,
        "qname_ideal": ["U1", (2,)],
        "qname_allowed": ["None", "U1"],
        "period": 1,
        "submodel": [("xxx", [0]), ("ionanisotropy", [1]), ("hz", [2])],
        "ham_expr": [[], [], [], []],
    },
    # ### ld LADDERS
    "ldhxId": {
        "nb_param": 1,
        "qname_ideal": ["None", (1,)],
        "qname_allowed": ["None"],
        "period": 1,
        "submodel": [],
        "ham_expr": [[(("M", -1.0, 0), ("SxId", 0))], [], [], []],
    },
    "ldIdhx": {
        "nb_param": 1,
        "qname_ideal": ["None", (1,)],
        "qname_allowed": ["None"],
        "period": 1,
        "submodel": [],
        "ham_expr": [[(("M", -1.0, 0), ("IdSx", 0))], [], [], []],
    },
    "ldhzId": {
        "nb_param": 1,
        "qname_ideal": ["U1", (1,)],
        "qname_allowed": ["None", "U1"],
        "period": 1,
        "submodel": [],
        "ham_expr": [[(("M", -1.0, 0), ("SzId", 0))], [], [], []],
    },
    "ldIdhz": {
        "nb_param": 1,
        "qname_ideal": ["U1", (1,)],
        "qname_allowed": ["None", "U1"],
        "period": 1,
        "submodel": [],
        "ham_expr": [[(("M", -1.0, 0), ("IdSz", 0))], [], [], []],
    },
    # 'ldhzTR' : {'nb_param' : 1, 'qname_ideal' : ['U1', (1,)],'qname_allowed' : ['None','U1'], 'period' : -1,
    #     'submodel' : [],
    #     'ham_expr' : [ [( 0, ('MR', [-1.] ), ('Sz', 0))], [], [], [] ] },
    "ldxy-rung": {
        "nb_param": 1,
        "qname_ideal": ["SU2detached", (2,)],
        "qname_allowed": ["None", "U1comb", "SU2detached"],
        "period": 1,
        "submodel": [],
        "ham_expr": [
            [(("M", 1.0 / 2.0, 0), ("SpSm", 0)), (("M", 1.0 / 2.0, 0), ("SmSp", 0))],
            [],
            [],
            [],
        ],
    },
    "ldxy-leg11": {
        "nb_param": 1,
        "qname_ideal": ["SU2detached", (2,)],
        "qname_allowed": ["None", "U1comb", "SU2detached"],
        "period": 1,
        "submodel": [],
        "ham_expr": [
            [],
            [
                (("M", 1.0 / 2.0, 0), ("SpIdoSmId", 0)),
                (("M", 1.0 / 2.0, 0), ("SmIdoSpId", 0)),
            ],
            [],
            [],
        ],
    },
    "ldxy-leg22": {
        "nb_param": 1,
        "qname_ideal": ["SU2detached", (2,)],
        "qname_allowed": ["None", "U1comb", "SU2detached"],
        "period": 1,
        "submodel": [],
        "ham_expr": [
            [],
            [
                (("M", 1.0 / 2.0, 0), ("IdSpoIdSm", 0)),
                (("M", 1.0 / 2.0, 0), ("IdSmoIdSp", 0)),
            ],
            [],
            [],
        ],
    },
    "ldxy-leg12": {
        "nb_param": 1,
        "qname_ideal": ["SU2detached", (2,)],
        "qname_allowed": ["None", "U1comb", "SU2detached"],
        "period": 1,
        "submodel": [],
        "ham_expr": [
            [],
            [
                (("M", 1.0 / 2.0, 0), ("SpIdoIdSm", 0)),
                (("M", 1.0 / 2.0, 0), ("SmIdoIdSp", 0)),
            ],
            [],
            [],
        ],
    },
    "ldxy-leg21": {
        "nb_param": 1,
        "qname_ideal": ["SU2detached", (2,)],
        "qname_allowed": ["None", "U1comb", "SU2detached"],
        "period": 1,
        "submodel": [],
        "ham_expr": [
            [],
            [
                (("M", 1.0 / 2.0, 0), ("IdSpoSmId", 0)),
                (("M", 1.0 / 2.0, 0), ("IdSmoSpId", 0)),
            ],
            [],
            [],
        ],
    },
    # # 'xyL-2site' : {'nb_param' : 1, 'qname_ideal' : ['SU2', (2,)],'qname_allowed' : ['None','U1','SU2'], 'period' : 2,
    # #     'submodel' : [],
    # #     'ham_expr' : [ [], [], [( 0, ('M', [1./2.]), ('SpSm', 0)),(0, ('M', 1./2.),('SmSp', 0))], []] },
    # 'xyleg11-dimer' : {'nb_param' : 2, 'qname_ideal' : ['SU2', (2,)],'qname_allowed' : ['None','U1','SU2'], 'period' : 2,
    #     'submodel' : [],
    #     'ham_expr' : [ [], [( 0, ('M', [1./2.]), ('SpIdoSmId', 0)),(0, ('M', [1./2.]),('SmIdoSpId', 0)),( 1, ('M', [1./2.]), ('SpIdoSmId', 1)),(1, ('M', [1./2.]),('SmIdoSpId', 1))], [], []] },
    # 'xyleg22-dimer' : {'nb_param' : 2, 'qname_ideal' : ['SU2', (2,)],'qname_allowed' : ['None','U1','SU2'], 'period' : 2,
    #     'submodel' : [],
    #     'ham_expr' : [ [], [( 0, ('M', [1./2.]), ('IdSpoIdSm', 0)),(0, ('M', [1./2.]),('IdSmoIdSp', 0)),( 1, ('M', [1./2.]), ('IdSpoIdSm', 1)),(1, ('M', [1./2.]),('IdSmoIdSp', 1))], [], []] },
    "ldxy-flux-rung": {
        "nb_param": 2,
        "qname_ideal": ["SU2detached", (2,)],
        "qname_allowed": ["None", "U1comb", "SU2detached"],
        "period": 1,
        "submodel": [],
        "ham_expr": [
            [
                (("EXP", [1.0 / 2.0, +1.0j], [0, 1]), ("SpSm", 0)),
                (("EXP", [1.0 / 2.0, -1.0j], [0, 1]), ("SmSp", 0)),
            ],
            [],
            [],
            [],
        ],
    },
    "ldxy-flux-leg11": {
        "nb_param": 1,
        "qname_ideal": ["SU2detached", (2,)],
        "qname_allowed": ["None", "U1comb", "SU2detached"],
        "period": 1,
        "submodel": [],
        "ham_expr": [
            [],
            [
                (("EXP", [1.0 / 2.0, +1.0j], [0, 1]), ("SpIdoSmId", 0)),
                (("EXP", [1.0 / 2.0, -1.0j], [0, 1]), ("SmIdoSpId", 0)),
            ],
            [],
            [],
        ],
    },
    "ldxy-flux-leg22": {
        "nb_param": 1,
        "qname_ideal": ["SU2detached", (2,)],
        "qname_allowed": ["None", "U1comb", "SU2detached"],
        "period": 1,
        "submodel": [],
        "ham_expr": [
            [],
            [
                (("EXP", [1.0 / 2.0, -1.0j], [0, 1]), ("IdSpoIdSm", 0)),
                (("EXP", [1.0 / 2.0, +1.0j], [0, 1]), ("IdSmoIdSp", 0)),
            ],
            [],
            [],
        ],
    },
    "ldxy-flux-border-rung": {
        "nb_param": 1,
        "qname_ideal": ["SU2detached", (2,)],
        "qname_allowed": ["None", "U1comb", "SU2detached"],
        "period": -1,
        "submodel": [],
        "ham_expr": [
            [],
            [],
            [
                (("EXP", [1.0 / 2.0, +1.0j], [0, 1]), ("SpSm", ("RIGHT", 0))),
                (("EXP", [1.0 / 2.0, -1.0j], [0, 1]), ("SmSp", ("RIGHT", 0))),
                (("EXP", [1.0 / 2.0, -1.0j], [0, 1]), ("SpSm", ("LEFT", 0))),
                (("EXP", [1.0 / 2.0, +1.0j], [0, 1]), ("SmSp", ("LEFT", 0))),
            ],
            [],
        ],
    },
    "ldzz-rung": {
        "nb_param": 1,
        "qname_ideal": ["SU2detached", (2,)],
        "qname_allowed": ["None", "U1comb", "SU2detached"],
        "period": 1,
        "submodel": [],
        "ham_expr": [[(("M", 1.0, 0), ("SzSz", 0))], [], [], []],
    },
    "ldzz-leg11": {
        "nb_param": 1,
        "qname_ideal": ["SU2detached", (2,)],
        "qname_allowed": ["None", "U1comb", "SU2detached"],
        "period": 1,
        "submodel": [],
        "ham_expr": [[], [(("M", 1.0, 0), ("SzIdoSzId", 0))], [], []],
    },
    "ldzz-leg22": {
        "nb_param": 1,
        "qname_ideal": ["SU2detached", (2,)],
        "qname_allowed": ["None", "U1comb", "SU2detached"],
        "period": 1,
        "submodel": [],
        "ham_expr": [[], [(("M", 1.0, 0), ("IdSzoIdSz", 0))], [], []],
    },
    "ldzz-leg12": {
        "nb_param": 1,
        "qname_ideal": ["SU2detached", (2,)],
        "qname_allowed": ["None", "U1comb", "SU2detached"],
        "period": 1,
        "submodel": [],
        "ham_expr": [[], [(("M", 1.0, 0), ("SzIdoIdSz", 0))], [], []],
    },
    "ldzz-leg21": {
        "nb_param": 1,
        "qname_ideal": ["SU2detached", (2,)],
        "qname_allowed": ["None", "U1comb", "SU2detached"],
        "period": 1,
        "submodel": [],
        "ham_expr": [[], [(("M", 1.0, 0), ("IdSzoSzId", 0))], [], []],
    },
    # # 'ldzzL2sites' : {'nb_param' : 1, 'qname_ideal' : ['SU2detached', (2,)],'qname_allowed' : ['None','U1comb','SU2detached'], 'period' : 1,
    # #     'submodel' : [],
    # #     'ham_expr' : [ [], [( 0, ('M', [1.]), ('SzSz', 0) )], [], [] ] },
    # 'ldzzIdleg11dimer' : {'nb_param' : 2, 'qname_ideal' : ['SU2detached', (2,)],'qname_allowed' : ['None','U1comb','SU2detached'], 'period' : 2,
    #     'submodel' : [],
    #     'ham_expr' : [ [], [( 0, ('M', [1.]), ('SzIdoSzId', 0) ),( 1, ('M', [1.]), ('SzIdoSzId', 1) )], [], [] ] },
    # 'ldIdzzleg22dimer' : {'nb_param' : 2, 'qname_ideal' : ['SU2detached', (2,)],'qname_allowed' : ['None','U1comb','SU2detached'], 'period' : 2,
    #     'submodel' : [],
    #     'ham_expr' : [ [], [( 0, ('M', [1.]), ('IdSzoIdSz', 0) ),( 1, ('M', [1.]), ('IdSzoIdSz', 1) )], [], [] ] },
    "ldxxz-rung": {
        "nb_param": 2,
        "qname_ideal": ["SU2detached", (2,)],
        "qname_allowed": ["None", "SU2detached", "U1comb"],
        "period": 1,
        "submodel": [("ldxy-rung", [0]), ("ldzz-rung", [1])],
        "ham_expr": [[], [], [], []],
    },
    "ldxxz-legs": {
        "nb_param": 2,
        "qname_ideal": ["SU2detached", (2,)],
        "qname_allowed": ["None", "SU2detached", "U1comb"],
        "period": 1,
        "submodel": [
            ("ldxy-leg11", [0]),
            ("ldxy-leg22", [0]),
            ("ldzz-leg11", [1]),
            ("ldzz-leg22", [1]),
        ],
        "ham_expr": [[], [], [], []],
    },
    # model !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    "ldsnake0": {
        "nb_param": 2,
        "qname_ideal": ["U1comb", (1,)],
        "qname_allowed": ["None", "U1comb"],
        "period": 1,
        "submodel": [
            ("ldxy-rung", [0]),
            ("ldzz-rung", [0]),
            ("ldxy-leg12", [1]),
            ("ldzz-leg12", [1]),
        ],
        "ham_expr": [[], [], [], []],
    },
    "ldsnake1": {
        "nb_param": 2,
        "qname_ideal": ["U1comb", (1,)],
        "qname_allowed": ["None", "U1comb"],
        "period": 1,
        "submodel": [
            ("ldxy-rung", [0]),
            ("ldzz-rung", [0]),
            ("ldxy-leg21", [1]),
            ("ldzz-leg21", [1]),
        ],
        "ham_expr": [[], [], [], []],
    },
    # 'ldsnake0-dimer-hz' : {'nb_param' : 2, 'qname_ideal' : ['U1comb', (1,)],'qname_allowed' : ['None','U1comb'], 'period' : 1,
    #     'submodel' : [('ldxy-rung',[0]),('ldzz-rung',[0]),('ldhzId',[2]),('ldIdhz',[2])],
    #     'ham_expr' : [ [], [ ( 1, ('M', [1./2.]), ('SpIdoIdSm', 0)),(1, ('M', [1./2.]),('SmIdoIdSp', 0)),(1, ('M', [1.]),('SzIdoIdSz', 0)) ], [], [] ] },
    # 'ldsnake1-dimer-hz' : {'nb_param' : 2, 'qname_ideal' : ['U1comb', (2,)],'qname_allowed' : ['None','U1comb'], 'period' : 2,
    #     'submodel' : [('ldxy-rung',[0]),('ldzz-rung',[0]),('ldhzId',[2]),('ldIdhz',[2])],
    #     'ham_expr' : [ [], [ ( 1, ('M', [1./2.]), ('IdSpoIdSm', 0)),(1, ('M', [1./2.]),('IdSmoIdSp', 0)),(1, ('M', [1.]),('IdSzoIdSz', 0)),
    #                          ( 1, ('M', [1./2.]), ('SpIdoSmId', 1)),(1, ('M', [1./2.]),('SmIdoSpId', 1)),(1, ('M', [1.]),('SzIdoSzId', 1)) ], [], [] ] },
    "lr-xxz": {
        "nb_param": 4,
        "qname_ideal": ["SU2detached", (2,)],
        "qname_allowed": ["None", "U1comb", "SU2detached"],
        "period": 1,
        "submodel": [("ldxxz-rung", [2, 3]), ("ldxxz-legs", [0, 1])],
        "ham_expr": [[], [], [], []],
    },
    "lr-xxz-hz": {
        "nb_param": 5,
        "qname_ideal": ["U1comb", (2,)],
        "qname_allowed": ["None", "U1comb"],
        "period": 1,
        "submodel": [("lr-xxz", [0, 1, 2, 3]), ("ldhzId", [4]), ("ldIdhz", [4])],
        "ham_expr": [[], [], [], []],
    },
    # 'ldxxz-hzN' : {'nb_param' : 3, 'qname_ideal' : ['None', (1,)],'qname_allowed' : ['None','U1comb'], 'period' : 1,
    #     'submodel' : [('ldxxz',[0,1]),('ldhzId',[2]),('ldIdhz',[2])],
    #     'ham_expr' : [ [], [], [], [] ] },
    # ###
    #
    #   /|\    /|\
    #  / | \  / | \
    # /__|  \/__|  \
    #
    "ldcoupled_triangle": {
        "nb_param": 5,
        "qname_ideal": ["U1comb", (1,)],
        "qname_allowed": ["None", "U1comb"],
        "period": 2,
        "submodel": [("ldhzId", [4])],
        "ham_expr": [
            [
                (("M", 1.0 / 2.0, 0), ("SpSm", 1)),
                (("M", 1.0 / 2.0, 0), ("SmSp", 1)),
                (("M", 1.0, 1), ("SzSz", 1)),
                (("M", -1.0, 4), ("IdSz", 1)),
            ],
            [
                (("M", 1.0 / 2.0, 0), ("SpIdoSmId", 0)),
                (("M", 1.0 / 2.0, 0), ("SmIdoSpId", 0)),
                (("M", 1.0, 1), ("SzIdoSzId", 0)),
                (("M", 1.0 / 2.0, 0), ("SpIdoIdSm", 0)),
                (("M", 1.0 / 2.0, 0), ("SmIdoIdSp", 0)),
                (("M", 1.0, 1), ("SzIdoIdSz", 1)),
                (("M", 1.0 / 2.0, 2), ("IdSpoSmId", 1)),
                (("M", 1.0 / 2.0, 2), ("IdSmoSpId", 1)),
                (("M", 1.0, 3), ("IdSzoSzId", 1)),
            ],
            [],
            [],
        ],
    },
    # 'ldcoupled_triangle_flux' : {'nb_param' : 5, 'qname_ideal' : ['U1comb', (1,)],'qname_allowed' : ['None','U1comb'], 'period' : 2,
    #     'submodel' : [('ldhzId',[4])],
    #     'ham_expr' : [ [( ('M', 1./2., 0), ('SpSm', 1)), ( ('M', 1./2., 0), ('SmSp', 1)), ( ('M', 1., 1), ('SzSz', 1)), ( ('M', -1., 4), ('IdSz', 1)) ], [( ('M', 1./2., 0), ('SpIdoSmId', 0)),( ('M', 1./2., 0),('SmIdoSpId', 0)),( ('M', 1., 1),('SzIdoSzId', 0)), ( ('M', 1./2., 0), ('SpIdoIdSm', 0)), ( ('M', 1./2., 0),('SmIdoIdSp', 0)),( ('M', 1., 1),('SzIdoIdSz', 1)), ( ('M', 1./2., 2), ('IdSpoSmId', 1)),(('M', 1./2., 2),('IdSmoSpId', 1)),( ('M', 1., 3),('IdSzoSzId', 1)) ], [], [] ] },
    # 'ldcoupled_triangle_neel_flux' : {'nb_param' : 5, 'qname_ideal' : ['U1comb', (1,)],'qname_allowed' : ['None','U1comb'], 'period' : 4,
    #     'submodel' : [('ldhzId',[4])],
    #     'ham_expr' : [ [( ('M', 1./2., 0), ('SpSm', 1)), ( ('M', 1./2., 0), ('SmSp', 1)), ( ('M', 1., 1), ('SzSz', 1)), ( ('M', -1., 4), ('IdSz', 1)) ], [( ('M', 1./2., 0), ('SpIdoSmId', 0)),( ('M', 1./2., 0),('SmIdoSpId', 0)),( ('M', 1., 1),('SzIdoSzId', 0)), ( ('M', 1./2., 0), ('SpIdoIdSm', 0)), ( ('M', 1./2., 0),('SmIdoIdSp', 0)),( ('M', 1., 1),('SzIdoIdSz', 1)), ( ('M', 1./2., 2), ('IdSpoSmId', 1)),(('M', 1./2., 2),('IdSmoSpId', 1)),( ('M', 1., 3),('IdSzoSzId', 1)) ], [], [] ] },
    # 'ldcoupled_square' : {'nb_param' : 3, 'qname_ideal' : ['SU2', (2,)],'qname_allowed' : ['None','U1'], 'period' : 2,
    #     'submodel' : [('xyrung',[0]),('zzrung',[0]),('hzId',[2]),('Idhz',[2])],
    #     'ham_expr' : [ [ ], [( 0, ('M', [1./2.]), ('SpIdoSmId', 0)),(0, ('M', [1./2.]),('SmIdoSpId', 0)),(0, ('M', [1./2.]),('SzIdoSzId', 0)), ( 0, ('M', [1./2.]), ('IdSpoIdSm', 0)),(0, ('M', [1./2.]),('IdSmoIdSp', 0)),(0, ('M', [1./2.]),('IdSzoIdSz', 0)), ( 1, ('M', [1./2.]), ('SpIdoSmId', 1)),(1, ('M', [1./2.]),('SmIdoSpId', 1)),(1, ('M', [1./2.]),('SzIdoSzId', 1)), ( 1, ('M', [1./2.]), ('IdSpoIdSm', 1)),(1, ('M', [1./2.]),('IdSmoIdSp', 1)),(1, ('M', [1./2.]),('IdSzoIdSz', 1)) ], [], [] ] },
    "ldspincurrent": {
        "nb_param": 1,
        "qname_ideal": ["SU2detached", (2,)],
        "qname_allowed": ["None", "U1comb", "SU2detached"],
        "period": 1,
        "submodel": [
            ("ldxy-flux-leg11", [0]),
            ("ldxy-flux-leg22", [0]),
            ("ldxy-flux-border-rung", [0]),
        ],
        "ham_expr": [[], [], [], []],
    },
    # 'ldsh-xxx-hz-dimJ1J2' :
    #     {'nb_param' : 3, 'qname' : ['ldsh-U1comb', (2,)], 'period' : 2,
    #      'ham_expr' : [ [(1, 1/2.,'ldsh-SmIdIdSp'),(1, 1/2.,'ldsh-SpIdIdSm'),(1, 1/2.,'ldsh-IdSmSpId'),(1, 1/2.,'ldsh-IdSpSmId'),(1, 1.,'ldsh-SzIdIdSz'),(1, 1.,'ldsh-IdSzSzId')],
    #                     [(0, 1/2.,'ldsh-SpSm'),(0, 1/2.,'ldsh-SmSp'),(0, 1.,'ldsh-SzSz'),(2, -1.,'ldsh-SzId'),(2, -1.,'ldsh-IdSz')],
    #                     [],
    #                     [] ],
    #      'ham_expr0' : [ [(0, 1/2.,'ldsh-SmIdSpId'),(0, 1/2.,'ldsh-SpIdSmId'),(0, 1.,'ldsh-SzIdSzId')],
    #                     [],
    #                     [],
    #                     [] ],
    #      'ham_expr1' : [ [(0, 1/2.,'ldsh-IdSmIdSp'),(0, 1/2.,'ldsh-IdSpIdSm'),(0, 1.,'ldsh-IdSzIdSz')],
    #                     [],
    #                     [],
    #                     [] ]
    #  },
    # 'ldsh-xxz-hz-dimJ1J2' :
    #     {'nb_param' : 5, 'qname' : ['ldsh-U1comb', (2,)], 'period' : 2,
    #      'ham_expr' : [ [(2, 1/2.,'ldsh-SmIdIdSp'),(2, 1/2.,'ldsh-SpIdIdSm'),(2, 1/2.,'ldsh-IdSmSpId'),(2, 1/2.,'ldsh-IdSpSmId'),(3, 1.,'ldsh-SzIdIdSz'),(3, 1.,'ldsh-IdSzSzId')],
    #                     [(0, 1/2.,'ldsh-SpSm'),(0, 1/2.,'ldsh-SmSp'),(1, 1.,'ldsh-SzSz'),(4, -1.,'ldsh-SzId'),(4, -1.,'ldsh-IdSz')],
    #                     [],
    #                     [] ],
    #      'ham_expr0' : [ [(0, 1/2.,'ldsh-SmIdSpId'),(0, 1/2.,'ldsh-SpIdSmId'),(1, 1.,'ldsh-SzIdSzId')],
    #                     [],
    #                     [],
    #                     [] ],
    #      'ham_expr1' : [ [(0, 1/2.,'ldsh-IdSmIdSp'),(0, 1/2.,'ldsh-IdSpIdSm'),(1, 1.,'ldsh-IdSzIdSz')],
    #                     [],
    #                     [],
    #                     [] ]
    # }
}

################################################################################
################################################################################
################################################################################

"""
