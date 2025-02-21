import pytest


def test_fhmdot_operators():
    from automation import is_mdot_available

    if is_mdot_available():
        from mdot_operators import single_operator_real, single_operator_cplx
        from pyfhmdot.models.pymodels import single_operator
        from numpy import all

        for op_name in [
            "sh_id_no",
            "sh_sm_no",
            "sh_sp_no",
            "sh_sx_no",
            "sh_sy_no",
            "sh_sz_no",
            "sh_id_u1",
            "sh_sm_u1",
            "sh_sp_u1",
            "sh_sz_u1",
            # "so_id_no",
            # "so_sm_no",
            # "so_sp_no",
            # "so_sx_no",
            # "so_sy_no",
            # "so_sz_no",
            # "so_id_u1",
            # "so_sm_u1",
            # "so_sp_u1",
            # "so_sz_u1",
            # "ru_idid_no",
            # "ru_idsz_no",
            # "ru_szid_no",
            # "ru_idsp_no",
            # "ru_spid_no",
            # "ru_idsm_no",
            # "ru_smid_no",
            # "ru_idsp_no",
            # "ru_spid_no",
            # "ru_idsm_no",
            # "ru_smid_no",
            # "ru_idid_u1",
            # "ru_idsz_u1",
            # "ru_szid_u1",
            # "ru_idsp_u1",
            # "ru_spid_u1",
            # "ru_idsm_u1",
            # "ru_smid_u1",
            # "ru_idsp_u1",
            # "ru_spid_u1",
            # "ru_idsm_u1",
            # "ru_smid_u1",
        ]:
            op_python = single_operator(op_name)
            if "sy" in op_name:    
                op_mdot = single_operator_cplx(op_name)
            else:
                op_mdot = single_operator_real(op_name)
            
            if "sp" not in op_name and "sm" not in op_name: # need to fix
                for key in op_python.keys():
                    assert all(op_python[key] == op_mdot[key])
