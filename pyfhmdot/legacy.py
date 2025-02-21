"""project.py"""
# import shutil
# import shlex
from typing import Optional

import numpy as _np
from scipy.linalg import svd as _svd


def _svd_nondeg(block_dict, nondeg, nondeg_dims, array_of_U, array_of_S, array_of_V):
    for i in range(len(nondeg)):
        dims = nondeg_dims[i]
        # U,S,V = _np.linalg.svd(block_dict[nondeg[i][1]].reshape(dims[0]*dims[1],dims[2]*dims[3]), full_matrices=False, compute_uv=True)
        # U,S,V = _np.linalg.svd(block_dict[nondeg[i][1]].reshape(dims[0]*dims[1],dims[2]*dims[3]))
        # scipy
        # U,S,V = _svd(block_dict[nondeg[i][1]].reshape(dims[0]*dims[1],dims[2]*dims[3]) )
        try:
            U, S, V = _svd(
                block_dict[nondeg[i][1]].reshape(dims[0] * dims[1], dims[2] * dims[3]),
                full_matrices=False,
                compute_uv=True,
                overwrite_a=True,
            )
        except:
            # _np.save('/users/kestin0/MYBUGGY/matrix_{0}'.format(_np.random.randint(100000)),block_dict[nondeg[i][1]].reshape(dims[0]*dims[1],dims[2]*dims[3]))
            print("!!!!!!!!matrix badly conditioned!!!!!!!!!")
            U, S, V = _svd(
                block_dict[nondeg[i][1]].reshape(dims[0] * dims[1], dims[2] * dims[3]),
                full_matrices=False,
                compute_uv=True,
                overwrite_a=False,
                lapack_driver="gesvd",
            )
        # U,S,V = _svd(block_dict[nondeg[i][1]].reshape(dims[0]*dims[1],dims[2]*dims[3]), full_matrices=False, compute_uv=True, overwrite_a=True, lapack_driver='gesvd')
        array_of_U.append(U)
        array_of_S.append(S)
        array_of_V.append(V)
        # del U,S,V
    pass


def _sliceds(theta_blocs, deg, subnewsize):
    for i in range(len(deg)):  # for each deg global block
        # define a local basis
        left__loc_basis = sorted(set([(it[0], it[1]) for it in deg[i][1]]))
        right_loc_basis = sorted(set([(it[2], it[3]) for it in deg[i][1]]))
        # find the local dim corresponding to left_loc_basis and right_loc_basis
        left__loc_dim = len(left__loc_basis) * [(0, 0)]
        right_loc_dim = len(right_loc_basis) * [(0, 0)]
        # for each local_index
        for it in deg[i][1]:
            dims = theta_blocs._blocks[it].shape
            left__loc_dim[left__loc_basis.index((it[0], it[1]))] = (dims[0], dims[1])
            right_loc_dim[right_loc_basis.index((it[2], it[3]))] = (dims[2], dims[3])
        # find the totdim
        total_left__dim = sum([d[0] * d[1] for d in left__loc_dim])
        total_right_dim = sum([d[0] * d[1] for d in right_loc_dim])
        # offsets
        left__loc_off = [0] + [
            sum([d[0] * d[1] for d in left__loc_dim[:i]])
            for i in range(1, len(left__loc_dim))
        ]
        right_loc_off = [0] + [
            sum([d[0] * d[1] for d in right_loc_dim[:i]])
            for i in range(1, len(right_loc_dim))
        ]
        subnewsize.append(
            [
                total_left__dim,
                total_right_dim,
                left__loc_basis,
                left__loc_off,
                left__loc_dim,
                right_loc_basis,
                right_loc_off,
                right_loc_dim,
            ]
        )


def _svd_deg(theta_blocs, deg, subnewsize, array_of_U, array_of_S, array_of_V):
    if len(theta_blocs._blocks.keys()) == 0:
        pass
    else:
        datatype = theta_blocs._blocks.itervalues().next().dtype

    # print(subnewsize)
    for i in range(len(deg)):
        # construct the degenerated matrix
        thetaDeg = _np.zeros((subnewsize[i][0], subnewsize[i][1]), dtype=datatype)
        # fill it
        for it in deg[i][1]:
            posL = subnewsize[i][2].index((it[0], it[1]))
            offL = subnewsize[i][3][posL]
            dimL = subnewsize[i][4][posL]
            posR = subnewsize[i][5].index((it[2], it[3]))
            offR = subnewsize[i][6][posR]
            dimR = subnewsize[i][7][posR]
            sliceL = slice(offL, offL + dimL[0] * dimL[1])
            sliceR = slice(offR, offR + dimR[0] * dimR[1])
            thetaDeg[sliceL, sliceR] = theta_blocs._blocks[it].reshape(
                dimL[0] * dimL[1], dimR[0] * dimR[1]
            )
        # print("thetaDeg",thetaDeg)
        # now SVD
        # U,S,V = _np.linalg.svd(thetaDeg, full_matrices=False, compute_uv=True)
        # U,S,V = _np.linalg.svd(thetaDeg)
        # scipy
        # U,S,V = _svd(thetaDeg)
        try:
            U, S, V = _svd(
                thetaDeg, full_matrices=False, compute_uv=True, overwrite_a=False
            )
        except:
            # _np.save('/users/kestin0/MYBUGGY/matrix_{0}'.format(_np.random.randint(100000)),thetaDeg)
            print("!!!!!!!!matrix badly conditioned!!!!!!!!!")
            U, S, V = _svd(
                thetaDeg,
                full_matrices=False,
                compute_uv=True,
                overwrite_a=True,
                lapack_driver="gesvd",
            )

        # U,S,V = _svd(thetaDeg, full_matrices=False, compute_uv=True, overwrite_a=True, lapack_driver='gesvd')
        array_of_U.append(U)
        array_of_S.append(S)
        array_of_V.append(V)
        # del U, S, V
    pass


############################################################


def _mult_nondeg_MV(
    array_U, array_S, cut, array_V, nondeg, nondeg_dims, dst_lhs_blocs, dst_rhs_blocs
):
    i_Nb = len(nondeg)
    for i in range(i_Nb):  # reversed, and passed by pop.
        Dsi = cut.pop()
        if Dsi > 0:
            dims = nondeg_dims.pop()
            tmp_nondeg = nondeg.pop()
            dst_lhs_blocs[(tmp_nondeg[1][0], tmp_nondeg[1][1], tmp_nondeg[0])] = _np.dot(
                array_U.pop()[:, :Dsi], _np.diag(array_S.pop()[:Dsi])
            ).reshape(dims[0], dims[1], Dsi)
            dst_rhs_blocs[
                (tmp_nondeg[0], tmp_nondeg[1][2], tmp_nondeg[1][3])
            ] = array_V.pop()[:Dsi, :].reshape(Dsi, dims[2], dims[3])
        else:
            array_U.pop()
            array_V.pop()
            array_S.pop()
            nondeg_dims.pop()
            nondeg.pop()
            # print("REMOVED??????????????????????????????????????????????????!")
    pass


def _mult_deg_MV(
    array_U, array_S, cut, array_V, deg, subnewsize, dst_lhs_blocs, dst_rhs_blocs
):
    i_Nb = len(deg)  # index for deg and subnewsize.. we
    for i in range(i_Nb):  # reversed, and pop each value.
        # Dsi = cut[i]
        Dsi = cut.pop()
        if Dsi > 0:
            # M = _np.dot(array_U[i][:,:Dsi],_np.diag(array_S[i][:Dsi]))
            # V = array_V[i]#[Dsi:,:]
            M = _np.dot(array_U.pop()[:, :Dsi], _np.diag(array_S.pop()[:Dsi]))
            V = array_V.pop()  # [Dsi:,:]

            tmp = subnewsize.pop()
            tmp_deg = deg.pop()
            for it in tmp_deg[1]:
                posL = tmp[2].index((it[0], it[1]))
                offL = tmp[3][posL]
                dimL = tmp[4][posL]
                posR = tmp[5].index((it[2], it[3]))
                offR = tmp[6][posR]
                dimR = tmp[7][posR]

                # print('M[slice(offL,offL+dimL[0]*dimL[1]),:Dsi]=',M[slice(offL,offL+dimL[0]*dimL[1]),:Dsi])
                # print('dimL=',dimL)
                # print('Dsi=',Dsi)

                dst_lhs_blocs[(it[0], it[1], tmp_deg[0])] = M[
                    slice(offL, offL + dimL[0] * dimL[1]), :Dsi
                ].reshape(dimL[0], dimL[1], Dsi)
                dst_rhs_blocs[(tmp_deg[0], it[2], it[3])] = V[
                    :Dsi, slice(offR, offR + dimR[0] * dimR[1])
                ].reshape(Dsi, dimR[0], dimR[1])
        else:
            array_U.pop()
            array_V.pop()
            array_S.pop()
            subnewsize.pop()
            deg.pop()
            # print("REMOVED??????????????????????????????????????????????????!")

    pass


############################################################


def _mult_nondeg_UM(
    array_U, array_S, cut, array_V, nondeg, nondeg_dims, dst_lhs_blocs, dst_rhs_blocs
):
    for i in range(len(nondeg)):  # reversed, and passed by pop.
        Dsi = cut[i]
        if Dsi != 0:
            dims = nondeg_dims[i]
            dst_lhs_blocs[(nondeg[i][1][0], nondeg[i][1][1], nondeg[i][0])] = array_U[i][
                :, :Dsi
            ].reshape(dims[0], dims[1], Dsi)
            dst_rhs_blocs[(nondeg[i][0], nondeg[i][1][2], nondeg[i][1][3])] = _np.dot(
                _np.diag(array_S[i][:Dsi]), array_V[i][:Dsi, :]
            ).reshape(Dsi, dims[2], dims[3])
        else:
            # print("REMOVED??????????????????????????????????????????????????!")
            pass
    pass


def _mult_deg_UM(
    array_U, array_S, cut, array_V, deg, subnewsize, dst_lhs_blocs, dst_rhs_blocs
):
    i_Nb = len(deg)
    for i in range(i_Nb):
        Dsi = cut.pop()
        if Dsi > 0:
            M = _np.dot(_np.diag(array_S.pop()[:Dsi]), array_V.pop()[:Dsi, :])
            U = array_U.pop()  # [:,:Dsi]

            tmp = subnewsize.pop()
            tmp_deg = deg.pop()
            for it in tmp_deg[1]:
                posL = tmp[2].index((it[0], it[1]))
                offL = tmp[3][posL]
                dimL = tmp[4][posL]
                posR = tmp[5].index((it[2], it[3]))
                offR = tmp[6][posR]
                dimR = tmp[7][posR]

                dst_lhs_blocs[(it[0], it[1], tmp_deg[0])] = U[
                    slice(offL, offL + dimL[0] * dimL[1]), :Dsi
                ].reshape(dimL[0], dimL[1], Dsi)
                dst_rhs_blocs[(tmp_deg[0], it[2], it[3])] = M[
                    :Dsi, slice(offR, offR + dimR[0] * dimR[1])
                ].reshape(Dsi, dimR[0], dimR[1])
        else:
            array_U.pop()
            array_V.pop()
            array_S.pop()
            subnewsize.pop()
            deg.pop()
            # print("REMOVED??????????????????????????????????????????????????!")

    pass


############################################################


def theta_to_um(theta_blocs, lhs_blocs, rhs_blocs, simdict):
    lab = theta_blocs.get_labels()
    if len(lab) != 4:
        raise (Exception("To svd, you should have a theta matrix form."))

    bas = theta_blocs._lbasis
    keys = list(theta_blocs._blocks.iterkeys())
    middle = retained_QN(bas, keys, direction_right=True)

    # # froebenius norm !
    # norm_before = 0.
    # for _ in theta_blocs._blocks.itervalues():
    #     norm_before += _np.linalg.norm(_)**2
    # norm_before = _np.sqrt(norm_before)
    # print('norm_before=',norm_before)

    ### HERE
    # lhs_blocs = _QTensor([bas[0],bas[1],middle],[lab[0],lab[1],(lab[0][0],lab[0][1]+1)])
    # rhs_blocs = _QTensor([middle,bas[2],bas[3]],[(lab[0][0],lab[0][1]+1),lab[2],lab[3]])
    lhs_blocs._lbasis[-1] = middle
    rhs_blocs._lbasis[+0] = middle
    lhs_blocs._blocks = dict()
    rhs_blocs._blocks = dict()

    nondeg, deg = degeneracy_in_QN(bas, keys, middle, True)

    subnewsize_deg = []
    _sliceds(theta_blocs, deg, subnewsize_deg)
    nondeg_dims = [theta_blocs._blocks[_[1]].shape for _ in nondeg]

    array_of_U = []
    array_of_S = []
    array_of_V = []

    _svd_nondeg(
        theta_blocs._blocks, nondeg, nondeg_dims, array_of_U, array_of_S, array_of_V
    )
    _svd_deg(theta_blocs, deg, subnewsize_deg, array_of_U, array_of_S, array_of_V)
    # print('SSSSSSSSSSSSSSSSSSSSSS')
    # print(array_of_S)

    eps_truncation_error = simdict["eps_truncation_error"]
    chi_max = simdict["dw_Dmax"]
    chi_max_total = simdict["dw_Dmax_tot"]

    cut, dw = strategyQ_truncation(
        array_of_S, eps_truncation_error, chi_max, chi_max_total, False
    )
    # print('dw',dw)
    # print('SSSSSSSSSSSSSSSSSSSSSS')
    if simdict["normalize"] == True:
        normalize_the_array(array_of_S, cut)

    simdict["dw_one_serie"] += dw
    # simdict['dw_max'] = max(dw,simdict['dw_max'])
    # prettyprint(array_of_S)
    cut_nondeg = [cut[i] for i in range(len(nondeg))]
    cut_deg = [cut[i] for i in range(len(nondeg), len(nondeg) + len(deg))]
    # print("cut_nondeg",cut_nondeg)
    _mult_deg_UM(
        array_of_U,
        array_of_S,
        cut_deg,
        array_of_V,
        deg,
        subnewsize_deg,
        lhs_blocs._blocks,
        rhs_blocs._blocks,
    )
    _mult_nondeg_UM(
        array_of_U,
        array_of_S,
        cut_nondeg,
        array_of_V,
        nondeg,
        nondeg_dims,
        lhs_blocs._blocks,
        rhs_blocs._blocks,
    )

    # return lhs_blocs, rhs_blocs
    pass


def theta_to_mv(theta_blocs, lhs_blocs, rhs_blocs, simdict):
    lab = theta_blocs.get_labels()
    if len(lab) != 4:
        raise (Exception("To svd, you should have a theta matrix form."))

    bas = theta_blocs._lbasis
    keys = list(theta_blocs._blocks.iterkeys())
    middle = retained_QN(bas, keys, direction_right=False)

    # # froebenius norm
    # norm_before = 0.
    # for _ in theta_blocs._blocks.itervalues():
    #     norm_before += _np.linalg.norm(_)**2
    # norm_before = _np.sqrt(norm_before)
    # print('norm_before=',norm_before)

    ### HERE
    # lhs_blocs = _QTensor([bas[0],bas[1],middle],[lab[0],lab[1],(lab[0][0],lab[0][1]+1)])
    # rhs_blocs = _QTensor([middle,bas[2],bas[3]],[(lab[0][0],lab[0][1]+1),lab[2],lab[3]])
    lhs_blocs._lbasis[-1] = middle
    rhs_blocs._lbasis[+0] = middle
    lhs_blocs._blocks = dict()
    rhs_blocs._blocks = dict()

    nondeg, deg = degeneracy_in_QN(bas, keys, middle, False)
    # print("nondeg, deg",nondeg, deg)

    subnewsize_deg = []
    _sliceds(theta_blocs, deg, subnewsize_deg)
    nondeg_dims = [theta_blocs._blocks[_[1]].shape for _ in nondeg]

    array_of_U = []
    array_of_S = []
    array_of_V = []

    _svd_nondeg(
        theta_blocs._blocks, nondeg, nondeg_dims, array_of_U, array_of_S, array_of_V
    )
    _svd_deg(theta_blocs, deg, subnewsize_deg, array_of_U, array_of_S, array_of_V)
    # print('SSSSSSSSSSSSSSSSSSSSS')
    # print(array_of_S)

    eps_truncation_error = simdict["eps_truncation_error"]
    chi_max = simdict["dw_Dmax"]
    chi_max_total = simdict["dw_Dmax_tot"]
    cut, dw = strategyQ_truncation(
        array_of_S, eps_truncation_error, chi_max, chi_max_total, False
    )
    # print('dw',dw)
    # print('SSSSSSSSSSSSSSSSSSSSS')
    if simdict["normalize"] == True:
        normalize_the_array(array_of_S, cut)

    simdict["dw_one_serie"] += dw
    # simdict['dw_max'] = max(dw,simdict['dw_max'])
    # print(array_of_S,deg,nondeg)
    cut_nondeg = [cut[i] for i in range(len(nondeg))]
    cut_deg = [cut[i] for i in range(len(nondeg), len(nondeg) + len(deg))]

    # print("cut_nondeg,cut_deg",cut_nondeg,cut_deg)

    _mult_deg_MV(
        array_of_U,
        array_of_S,
        cut_deg,
        array_of_V,
        deg,
        subnewsize_deg,
        lhs_blocs._blocks,
        rhs_blocs._blocks,
    )
    _mult_nondeg_MV(
        array_of_U,
        array_of_S,
        cut_nondeg,
        array_of_V,
        nondeg,
        nondeg_dims,
        lhs_blocs._blocks,
        rhs_blocs._blocks,
    )

    # return lhs_blocs, rhs_blocs
    pass
