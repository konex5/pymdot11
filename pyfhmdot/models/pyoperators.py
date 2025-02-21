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
        # # rung: two spin half
        # 0 is |s1=1/2,mz1=+1/2>x|s2=1/2,mz2=+1/2>
        # 1 is |s1=1/2,mz1=+1/2>x|s2=1/2,mz2=-1/2>, |s1=1/2,mz1=-1/2>x|s2=1/2,mz2=+1/2>
        # 2 is |s1=1/2,mz1=-1/2>x|s2=1/2,mz2=-1/2>
        # works well for singlets and triplets
        "ru_idid_no": {
            (0, 0): coef
            * _np.array(
                [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=_real_t
            )
        },
        "ru_idid_u1": {
            (0, 0): coef * _np.array([[1]], dtype=_real_t),
            (1, 1): coef * _np.array([[1, 0], [0, 1]], dtype=_real_t),
            (2, 2): coef * _np.array([[1]], dtype=_real_t),
        },
        "ru_szid_no": {
            (0, 0): coef
            * _np.array(
                [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1]],
                dtype=_real_t,
            )
        },
        "ru_szid_u1": {
            (0, 0): coef * _np.array([[1]], dtype=_real_t),
            (1, 1): coef * _np.array([[1, 0], [0, -1]], dtype=_real_t),
            (2, 2): coef * _np.array([[-1]], dtype=_real_t),
        },
        "ru_idsz_no": {
            (0, 0): coef
            * _np.array(
                [[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]],
                dtype=_real_t,
            )
        },
        "ru_idsz_u1": {
            (0, 0): coef * _np.array([[1]], dtype=_real_t),
            (1, 1): coef * _np.array([[-1, 0], [0, 1]], dtype=_real_t),
            (2, 2): coef * _np.array([[-1]], dtype=_real_t),
        },
        "ru_szsz_no": {
            (0, 0): coef
            * _np.array(
                [[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]],
                dtype=_real_t,
            )
        },
        "ru_szsz_u1": {
            (0, 0): coef * _np.array([[1]], dtype=_real_t),
            (1, 1): coef * _np.array([[-1, 0], [0, -1]], dtype=_real_t),
            (2, 2): coef * _np.array([[1]], dtype=_real_t),
        },
        "ru_spid_no": {
            (0, 0): coef
            * _np.array(
                [[0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0]], dtype=_real_t
            )
        },
        "ru_spid_u1": {
            (0, 1): coef * _np.array([[0, 1]], dtype=_real_t),
            (1, 2): coef * _np.array([[1], [0]], dtype=_real_t),
        },
        "ru_idsp_no": {
            (0, 0): coef
            * _np.array(
                [[0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 0]], dtype=_real_t
            )
        },
        "ru_idsp_u1": {
            (0, 1): coef * _np.array([[1, 0]], dtype=_real_t),
            (1, 2): coef * _np.array([[0], [1]], dtype=_real_t),
        },
        "ru_smid_no": {
            (0, 0): coef
            * _np.array(
                [[0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0]], dtype=_real_t
            )
        },
        "ru_smid_u1": {
            (1, 0): coef * _np.array([[0], [1]], dtype=_real_t),
            (2, 1): coef * _np.array([[1, 0]], dtype=_real_t),
        },
        "ru_idsm_no": {
            (0, 0): coef
            * _np.array(
                [[0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 0]], dtype=_real_t
            )
        },
        "ru_idsm_u1": {
            (1, 0): coef * _np.array([[1], [0]], dtype=_real_t),
            (2, 1): coef * _np.array([[0, 1]], dtype=_real_t),
        },
        "ru_spsp_no": {
            (0, 0): coef
            * _np.array(
                [[0, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], dtype=_real_t
            )
        },
        "ru_spsp_u1": {
            (0, 2): coef * _np.array([[1]], dtype=_real_t),
        },
        "ru_smsm_no": {
            (0, 0): coef
            * _np.array(
                [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0]], dtype=_real_t
            )
        },
        "ru_smsm_u1": {
            (2, 0): coef * _np.array([[1]], dtype=_real_t),
        },
        "ru_spsm_no": {
            (0, 0): coef
            * _np.array(
                [[0, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]], dtype=_real_t
            )
        },
        "ru_spsm_u1": {
            (1, 1): coef * _np.array([[0, 1], [0, 0]], dtype=_real_t),
        },
        "ru_smsp_no": {
            (0, 0): coef
            * _np.array(
                [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]], dtype=_real_t
            )
        },
        "ru_smsp_u1": {
            (1, 1): coef * _np.array([[0, 0], [1, 0]], dtype=_real_t),
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
        "ru_idid_no-ru_idid_no",
        "ru_idsz_no-ru_idsz_no",
        "ru_szid_no-ru_idsz_no",
        "ru_idsz_no-ru_szid_no",
        "ru_szid_no-ru_szid_no",
        "ru_idsp_no-ru_idsp_no",
        "ru_spid_no-ru_idsp_no",
        "ru_idsp_no-ru_spid_no",
        "ru_spid_no-ru_spid_no",
        "ru_idsm_no-ru_idsm_no",
        "ru_smid_no-ru_idsm_no",
        "ru_idsm_no-ru_smid_no",
        "ru_smid_no-ru_smid_no",
        "ru_idsp_no-ru_idsm_no",
        "ru_spid_no-ru_idsm_no",
        "ru_idsp_no-ru_smid_no",
        "ru_spid_no-ru_smid_no",
        "ru_idsm_no-ru_idsp_no",
        "ru_smid_no-ru_idsp_no",
        "ru_idsm_no-ru_spid_no",
        "ru_smid_no-ru_spid_no",
        "ru_idid_u1-ru_idid_u1",
        "ru_idsz_u1-ru_idsz_u1",
        "ru_szid_u1-ru_idsz_u1",
        "ru_idsz_u1-ru_szid_u1",
        "ru_szid_u1-ru_szid_u1",
        "ru_idsp_u1-ru_idsp_u1",
        "ru_spid_u1-ru_idsp_u1",
        "ru_idsp_u1-ru_spid_u1",
        "ru_spid_u1-ru_spid_u1",
        "ru_idsm_u1-ru_idsm_u1",
        "ru_smid_u1-ru_idsm_u1",
        "ru_idsm_u1-ru_smid_u1",
        "ru_smid_u1-ru_smid_u1",
        "ru_idsp_u1-ru_idsm_u1",
        "ru_spid_u1-ru_idsm_u1",
        "ru_idsp_u1-ru_smid_u1",
        "ru_spid_u1-ru_smid_u1",
        "ru_idsm_u1-ru_idsp_u1",
        "ru_smid_u1-ru_idsp_u1",
        "ru_idsm_u1-ru_spid_u1",
        "ru_smid_u1-ru_spid_u1",
    ]

    if name in bonds:
        left_name, right_name = name.split("-")

        if weight_on_left is None:
            return single_operator(left_name, _np.sign(coef)*_np.sqrt(_np.abs(coef))), single_operator(
                right_name, _np.sign(coef)*_np.sqrt(_np.abs(coef))
            )
        elif weight_on_left:
            return single_operator(left_name, coef), single_operator(right_name, 1.0)
        else:
            return single_operator(left_name, 1.0), single_operator(right_name, coef)
