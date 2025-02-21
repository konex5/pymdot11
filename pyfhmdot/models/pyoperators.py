import numpy as _np

_real_t = "float64"
_cplx_t = "complex128"


def single_operator(name, coef):  # -> one bloc

    operators = {
        # spin half
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
            (0, 1): coef * _np.array([[-1j]], dtype=_cplx_t),
            (1, 0): coef * _np.array([[1j]], dtype=_cplx_t),
        },
        # spin one
        "so_id_no": {
            (0, 0): coef * _np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=_real_t)
        },
        "so_id_u1": {
            (0, 0): coef * _np.array([[1]], dtype=_real_t),
            (1, 1): coef * _np.array([[1]], dtype=_real_t),
            (2, 2): coef * _np.array([[1]], dtype=_real_t),
        },
        "so_sp_no": {
            (0, 0): coef * _np.array([[0, 1, 0], [0, 0, 1], [0, 0, 0]], dtype=_real_t)
        },
        "so_sp_u1": {
            (0, 1): coef * _np.array([[1]], dtype=_real_t),
            (1, 2): coef * _np.array([[1]], dtype=_real_t),
        },
        "so_sm_no": {
            (0, 0): coef * _np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=_real_t)
        },
        "so_sm_u1": {
            (1, 0): coef * _np.array([[1]], dtype=_real_t),
            (2, 1): coef * _np.array([[1]], dtype=_real_t),
        },
        "so_sz_no": {
            (0, 0): coef * _np.array([[1, 0, 0], [0, 0, 0], [0, 0, -1]], dtype=_real_t)
        },
        "so_sz_u1": {
            (0, 0): coef * _np.array([[1]], dtype=_real_t),
            (2, 2): coef * _np.array([[-1]], dtype=_real_t),
        },
        "so_sz^2_no": {
            (0, 0): coef * _np.array([[1, 0, 0], [0, 0, 0], [0, 0, 1]], dtype=_real_t)
        },
        "so_sz^2_u1": {
            (0, 0): coef * _np.array([[1]], dtype=_real_t),
            (2, 2): coef * _np.array([[1]], dtype=_real_t),
        },
        "so_sx_no": {
            (0, 0): coef * _np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=_real_t)
        },
        "so_id_cplx_no": {
            (0, 0): coef * _np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=_cplx_t)
        },
        "so_id_cplx_u1": {
            (0, 0): coef * _np.array([[1]], dtype=_cplx_t),
            (1, 1): coef * _np.array([[1]], dtype=_cplx_t),
            (2, 2): coef * _np.array([[1]], dtype=_cplx_t),
        },
        "so_sy_no": {
            (0, 0): coef
            * _np.array([[0, -1j, 0], [1j, 0, -1j], [0, 1j, 0]], dtype=_cplx_t)
        },
    }

    return operators[name]


def two_sites_bond_operator(name, coef, *, weight_on_left=None):  # -> two blocs
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
        "so_id_no-so_id_no",
        "so_sm_no-so_sp_no",
        "so_sp_no-so_sm_no",
        "so_sx_no-so_sx_no",
        "so_sy_no-so_sy_no",
        "so_sz_no-so_sz_no",
        "so_id_u1-so_id_u1",
        "so_sm_u1-so_sp_u1",
        "so_sp_u1-so_sm_u1",
        "so_sz_u1-so_sz_u1",
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

    return operators


"""
