import numpy as _np
from scipy.linalg import expm as _expm

from pyfhmdot.models.pyoperators import single_operator, two_sites_bond_operator
from pyfhmdot.intense.splitgroup import group_four_dgate as _group_four_dgate


def pyhamiltonian(name):
    models = {
        "skeleton": {
            "sub_model": "list_sub_ham_with_param",
            "on_site": "on_site_term",
            "nn_bond": "bond_term",
        },
        "sh_hx_no": {
            "sub_model": [],
            "on_site": [("hx", -1.0, "sh_sx_no")],
            "nn_bond": [],
        },
        "sh_hz_no": {
            "sub_model": [],
            "on_site": [("hz", -1.0, "sh_sz_no")],
            "nn_bond": [],
        },
        "sh_hz_u1": {
            "sub_model": [],
            "on_site": [("hz", -1.0, "sh_sz_u1")],
            "nn_bond": [],
        },
        "sh_xy_no": {
            "sub_model": [],
            "on_site": [],
            "nn_bond": [
                ("Jxy", 1.0 / 2.0, "sh_sp_no-sh_sm_no"),
                ("Jxy", 1.0 / 2.0, "sh_sm_no-sh_sp_no"),
            ],
        },
        "sh_xy_u1": {
            "sub_model": [],
            "on_site": [],
            "nn_bond": [
                ("Jxy", 1.0 / 2.0, "sh_sp_u1-sh_sm_u1"),
                ("Jxy", 1.0 / 2.0, "sh_sm_u1-sh_sp_u1"),
            ],
        },
        "sh_zz_no": {
            "sub_model": [],
            "on_site": [],
            "nn_bond": [("Jz", 1.0, "sh_sz_no-sh_sz_no")],
        },
        "sh_zz_u1": {
            "sub_model": [],
            "on_site": [],
            "nn_bond": [("Jz", 1.0, "sh_sz_u1-sh_sz_u1")],
        },
        "sh_xxz_no": {
            "sub_model": ["sh_xy_no", "sh_zz_no"],
            "on_site": [],
            "nn_bond": [],
        },
        "sh_xxz_u1": {
            "sub_model": ["sh_xy_u1", "sh_zz_u1"],
            "on_site": [],
            "nn_bond": [],
        },
        "sh_xxz-hz_no": {
            "sub_model": ["sh_xxz_no", "sh_hz_no"],
            "on_site": [],
            "nn_bond": [],
        },
        "sh_xxz-hz_u1": {
            "sub_model": ["sh_xxz_u1", "sh_hz_u1"],
            "on_site": [],
            "nn_bond": [],
        },
        "so_hx_no": {
            "sub_model": [],
            "on_site": [("hx", -1.0, "so_sx_no")],
            "nn_bond": [],
        },
        "so_hz_no": {
            "sub_model": [],
            "on_site": [("hz", -1.0, "so_sz_no")],
            "nn_bond": [],
        },
        "so_hz_u1": {
            "sub_model": [],
            "on_site": [("hz", -1.0, "so_sz_u1")],
            "nn_bond": [],
        },
        "so_sz^2_no": {
            "sub_model": [],
            "on_site": [("D", 1.0, "so_sz^2_no")],
            "nn_bond": [],
        },
        "so_sz^2_u1": {
            "sub_model": [],
            "on_site": [("D", 1.0, "so_sz^2_u1")],
            "nn_bond": [],
        },
        "so_xy_no": {
            "sub_model": [],
            "on_site": [],
            "nn_bond": [
                ("Jxy", 1.0 / 2.0, "so_sp_no-so_sm_no"),
                ("Jxy", 1.0 / 2.0, "so_sm_no-so_sp_no"),
            ],
        },
        "so_xy_u1": {
            "sub_model": [],
            "on_site": [],
            "nn_bond": [
                ("Jxy", 1.0 / 2.0, "so_sp_u1-so_sm_u1"),
                ("Jxy", 1.0 / 2.0, "so_sm_u1-so_sp_u1"),
            ],
        },
        "so_zz_no": {
            "sub_model": [],
            "on_site": [],
            "nn_bond": [("Jz", 1.0, "so_sz_no-so_sz_no")],
        },
        "so_zz_u1": {
            "sub_model": [],
            "on_site": [],
            "nn_bond": [("Jz", 1.0, "so_sz_u1-so_sz_u1")],
        },
        "so_xxz_no": {
            "sub_model": ["so_xy_no", "so_zz_no"],
            "on_site": [],
            "nn_bond": [],
        },
        "so_xxz_u1": {
            "sub_model": ["so_xy_u1", "so_zz_u1"],
            "on_site": [],
            "nn_bond": [],
        },
        "so_xxz-hz_no": {
            "sub_model": ["so_xxz_no", "so_hz_no"],
            "on_site": [],
            "nn_bond": [],
        },
        "so_xxz-hz_u1": {
            "sub_model": ["so_xxz_u1", "so_hz_u1"],
            "on_site": [],
            "nn_bond": [],
        },
        "ru_hzid_u1": {
            "sub_model": [],
            "on_site": [("hz", -1.0, "ru_hzid_u1")],
            "nn_bond": [],
        },
        "ru_idhz_u1": {
            "sub_model": [],
            "on_site": [("hz", -1.0, "ru_idhz_u1")],
            "nn_bond": [],
        },
        "ru_spsm_u1": {
            "sub_model": [],
            "on_site": [("Jxyperp", 1.0 / 2.0, "ru_spsm_u1")],
            "nn_bond": [],
        },
        "ru_smsp_u1": {
            "sub_model": [],
            "on_site": [("Jxyperp", 1.0 / 2.0, "ru_smsp_u1")],
            "nn_bond": [],
        },
        "ru_szsz_u1": {
            "sub_model": [],
            "on_site": [("Jzperp", 1.0, "ru_szsz_u1")],
            "nn_bond": [],
        },
        "ru_spid-smid_u1": {
            "sub_model": [],
            "on_site": [],
            "nn_bond": [("Jxypar", 1.0 / 2.0, "ru_spid-smid_u1")],
        },
        "ru_smid-spid_u1": {
            "sub_model": [],
            "on_site": [],
            "nn_bond": [("Jxypar", 1.0 / 2.0, "ru_smid-spid_u1")],
        },
        "ru_idsp-idsm_u1": {
            "sub_model": [],
            "on_site": [],
            "nn_bond": [("Jxypar", 1.0 / 2.0, "ru_idsp-idsm_u1")],
        },
        "ru_idsm-idsp_u1": {
            "sub_model": [],
            "on_site": [],
            "nn_bond": [("Jxypar", 1.0 / 2.0, "ru_idsm-idsp_u1")],
        },
        "ru_xypar_u1": {
            "sub_model": [
                "ru_smid-spid_u1",
                "ru_spid-smid_u1",
                "ru_idsm-idsp_u1",
                "ru_idsp-idsm_u1",
            ],
            "on_site": [],
            "nn_bond": [],
        },
        "ru_xyperp_u1": {
            "sub_model": ["ru_smsp_u1", "ru_spsm_u1"],
            "on_site": [],
            "nn_bond": [],
        },
        "ru_zzpar_u1": {
            "sub_model": ["ru_szid-szid_u1", "ru_idsz-idsz_u1"],
            "on_site": [],
            "nn_bond": [],
        },
        "ru_zzperp_u1": {
            "sub_model": ["ru_szsz_u1"],
            "on_site": [],
            "nn_bond": [],
        },
        "ru_xxzperp_xxzpar_u1": {
            "sub_model": ["ru_xyperp_u1", "ru_xypar_u1", "ru_zzperp_u1", "ru_zzpar_u1"],
            "on_site": [],
            "nn_bond": [],
        },
    }
    hamiltonian = {"on_site": [], "nn_bond": []}

    for on_site in models[name]["on_site"]:
        hamiltonian["on_site"].append(on_site)
    for bond in models[name]["nn_bond"]:
        hamiltonian["nn_bond"].append(bond)

    def append_sub_model(models, name, dst_hamiltonian):
        for sub_name in models[name]["sub_model"]:
            for on_site in models[sub_name]["on_site"]:
                dst_hamiltonian["on_site"].append(on_site)
            for bond in models[sub_name]["nn_bond"]:
                dst_hamiltonian["nn_bond"].append(bond)
            append_sub_model(models, sub_name, dst_hamiltonian)

    append_sub_model(models, name, hamiltonian)

    return hamiltonian


def on_site_operators_from_hamiltonian(name, parameters):
    hamiltonian = pyhamiltonian(name)

    single_operators = []
    for on_site in hamiltonian["on_site"]:
        single_operators.append(
            single_operator(name=on_site[-1], coef=parameters[on_site[0]] * on_site[1])
        )

    return single_operators


def nn_bond_operators_from_hamiltonian(name, parameters, *, weight_on_left=None):
    hamiltonian = pyhamiltonian(name)

    two_sites_bond_operators = []
    for nn_bond in hamiltonian["nn_bond"]:
        two_sites_bond_operators.append(
            two_sites_bond_operator(
                name=nn_bond[-1],
                coef=parameters[nn_bond[0]] * nn_bond[1],
                weight_on_left=weight_on_left,
            )
        )

    return two_sites_bond_operators


def _mpo_from_operators(id_bloc, on_site, nn_bond_left, nn_bond_right):
    blocks = {}

    bl_dimL = len(nn_bond_left) + 1
    bl_dimR = len(nn_bond_right) + 1

    # id
    for idx, val in id_bloc.items():
        blocks[(0, idx[0], idx[1], 0)] = val.reshape(tuple([1] + list(val.shape) + [1]))
        blocks[(bl_dimL, idx[0], idx[1], bl_dimR)] = val.reshape(
            tuple([1] + list(val.shape) + [1])
        )
    # on_site
    for idx, val in on_site[0].items():
        if _np.all(val != 0):
            blocks[(bl_dimL, idx[0], idx[1], 0)] = val.reshape(
                tuple([1] + list(val.shape) + [1])
            )

    # nn_bond
    for i in range(1, bl_dimR, 1):
        for idxb, valb in nn_bond_right[i - 1].items():
            if _np.all(valb != 0):
                blocks[(i, idxb[0], idxb[1], 0)] = valb.reshape(
                    tuple([1] + list(valb.shape) + [1])
                )

    for i in range(1, bl_dimL, 1):
        for idxa, vala in nn_bond_left[i - 1].items():
            if _np.all(vala != 0):
                blocks[(bl_dimL, idxa[0], idxa[1], i)] = vala.reshape(
                    tuple([1] + list(vala.shape) + [1])
                )

    return blocks


def _mpo_from_operators_left_border(id_bloc, on_site, nn_bond_right):
    blocks = {}
    bl_dimR = len(nn_bond_right) + 1

    # id
    for idx, val in id_bloc.items():
        blocks[(0, idx[0], idx[1], bl_dimR)] = val.reshape(
            tuple([1] + list(val.shape) + [1])
        )

    # on site
    for idx, val in on_site[0].items():
        if _np.all(val != 0):
            blocks[(0, idx[0], idx[1], 0)] = val.reshape(
                tuple([1] + list(val.shape) + [1])
            )

    # nn_bond
    for i in range(1, bl_dimR, 1):
        for idxa, vala in nn_bond_right[i - 1].items():
            if _np.all(vala != 0):
                blocks[(0, idxa[0], idxa[1], i)] = vala.reshape(
                    tuple([1] + list(vala.shape) + [1])
                )

    return blocks


def _mpo_from_operators_right_border(id_bloc, on_site, nn_bond_left):
    blocks = {}
    bl_dimL = len(nn_bond_left) + 1

    # id
    for idx, val in id_bloc.items():
        blocks[(0, idx[0], idx[1], 0)] = val.reshape(tuple([1] + list(val.shape) + [1]))

    # on site
    for idx, val in on_site[0].items():
        if _np.all(val != 0):
            blocks[(bl_dimL, idx[0], idx[1], 0)] = val.reshape(
                tuple([1] + list(val.shape) + [1])
            )

    # nn_bond
    for i in range(1, bl_dimL, 1):
        for idxb, valb in nn_bond_left[i - 1].items():
            if _np.all(valb != 0):
                blocks[(i, idxb[0], idxb[1], 0)] = valb.reshape(
                    tuple([1] + list(valb.shape) + [1])
                )

    return blocks


def on_site_fuse_for_mpo(tmpblocks, coef=1.0):
    all_keys = []
    for tmp in tmpblocks:
        for key in tmp.keys():
            all_keys.append(key)
    all_keys = sorted(set(all_keys))

    outblocks = {}
    for key in all_keys:
        for l in range(len(tmpblocks)):
            if key in tmpblocks[l].keys():
                if key not in outblocks.keys():
                    outblocks[key] = coef * tmpblocks[l][key]
                else:
                    outblocks[key] = coef * (
                        outblocks[key] + tmpblocks[l][key]
                    )  # for cmplx
    return [outblocks]


def hamiltonian_obc(model_name, parameters, size):
    """
    qnmodel='sh_xxz-hz_no' or 'ru_ldxxz-hz_u1'
    """
    mpo = []
    head, _, tail = model_name.split("_")
    id_bloc = single_operator(name=head + "_id_" + tail, coef=1.0)
    on_site = on_site_operators_from_hamiltonian(model_name, parameters)
    on_site = on_site_fuse_for_mpo(on_site)
    # fuse
    nn_bond = nn_bond_operators_from_hamiltonian(model_name, parameters)
    nn_bond_left = [_[0] for _ in nn_bond]
    nn_bond_right = [_[1] for _ in nn_bond]

    for site_i in range(size):
        if site_i == 0:
            mpo.append(_mpo_from_operators_left_border(id_bloc, on_site, nn_bond_right))
        elif site_i == size - 1:
            mpo.append(_mpo_from_operators_right_border(id_bloc, on_site, nn_bond_left))
        else:
            mpo.append(
                _mpo_from_operators(id_bloc, on_site, nn_bond_left, nn_bond_right)
            )
    return mpo


def _hamiltonian_gate_from_dense(id_dense, on_site_left, on_site_right, nn_bond, *, d):

    if (
        _np.any([isinstance(x, complex) for x in on_site_left])
        or _np.any([isinstance(x, complex) for x in on_site_right])
        or _np.any([isinstance(x, complex) for x in nn_bond])
    ):
        t = _np.ndarray((d, d, d, d), dtype="complex128")
        t.fill(0)
    else:
        t = _np.ndarray((d, d, d, d))
        t.fill(0)

    # on_site_left
    t[:, :, :, :] += (_np.outer(on_site_left[0][(0, 0)], id_dense[(0, 0)])).reshape(
        d, d, d, d
    )

    # on_site_right
    t[:, :, :, :] += (_np.outer(id_dense[(0, 0)], on_site_right[0][(0, 0)])).reshape(
        d, d, d, d
    )

    # nn_bond
    for bond in nn_bond:
        t[:, :, :, :] += (_np.outer(bond[0][(0, 0)], bond[1][(0, 0)])).reshape(
            d, d, d, d
        )

    return t


def _exp_gate(arg, dH, *, d):
    #####
    # REMARK : exp(+arg dH) is before contracted with s..
    #  _|_|_  Wu,l Wu,l+1
    #  |___|
    #   | |   Wd,l Wd,l+1
    # ------- => exp(+arg dH)
    dU = _expm(+arg * (dH.transpose([0, 2, 1, 3])).reshape(d * d, d * d)).reshape(
        d, d, d, d
    )
    # dU.setflags(write=0)
    # [('Wd',(l+1)),('Wd',(l+2)),('Wu',(l+1)),('Wu',(l+2))])
    return dU


def _exp_dgate(arg, dH, *, d):
    # TMP correspond to exp(+arg dH)
    tmp = _exp_gate(arg, dH, d=d)
    #####
    # REMARK : exp(+arg dH) is before contracted with s..
    # ------- => dU = exp(+arg dH) et dU | ket >
    #  _|_|_  Wp,l Wp,l+1
    #  |_dU_|
    #   | |   sp,l sp,l+1
    # |||A||| => obs A     >
    #  _|_|_  sm,-l sm,-(l+1)
    #  |___|
    #   | |   Wm,-l Wm,-(l+1)
    # ------- => exp(+conj(arg) dH)

    # REMARK ABOUT TIME EVOLUTION WITH COMPLEX HAMILTONIAN!
    # let's call dU = exp(-i dt dH)     (where arg=-i*dt for time)
    # of course dU^\dagger = exp(+i dt dH)
    #
    # so we have
    # A(t) = dU^\dagger A dU
    #
    # dU^\dagger = transpose(conj(dU))
    #
    # thus one should permute the label in the correct way after one
    # conjugate
    # REMARK ENDED HERE !
    dU = _np.outer(_np.conjugate(tmp).reshape(d**4), tmp.reshape(d**4)).reshape(
        d, d, d, d, d, d, d, d
    )
    # dU=>[('s',-(l+1)),('s',-(l+2)),('W',-(l+1)),('W',-(l+2)),('W',+(l+1)),('W',+(l+2)),('s',+(l+1)),('s',+(l+2))]
    # dU.setflags(write=0)
    return dU


def _suzu_trotter_exp_numpy(
    arg, id_dense, on_site_left, on_site_right, nn_bond, is_dgate, *, d
):

    dH = _hamiltonian_gate_from_dense(
        id_dense, on_site_left, on_site_right, nn_bond, d=d
    )
    if is_dgate == False:
        return _exp_gate(arg, dH, d=d)
    else:
        return _exp_dgate(arg, dH, d=d)


# below, cut from dense to quantum number (index + matrix)


def _generate_slices(d, deg):
    offi = 0
    for i in range(d):
        offj = 0
        for j in range(d):
            offk = 0
            for k in range(d):
                offl = 0
                for l in range(d):
                    yield i, j, k, l, slice(offi, (offi + deg[i])), slice(
                        offj, (offj + deg[j])
                    ), slice(offk, (offk + deg[k])), slice(offl, (offl + deg[l]))
                    offl += deg[l]
                offk += deg[k]
            offj += deg[j]
        offi += deg[i]


def _generate_slices_dgate(d, deg):
    offi = 0
    for i in range(d):
        offj = 0
        for j in range(d):
            offk = 0
            for k in range(d):
                offl = 0
                for l in range(d):
                    offm = 0
                    for m in range(d):
                        offn = 0
                        for n in range(d):
                            offo = 0
                            for o in range(d):
                                offp = 0
                                for p in range(d):
                                    yield i, j, k, l, m, n, o, p, slice(
                                        offi, (offi + deg[i])
                                    ), slice(offj, (offj + deg[j])), slice(
                                        offk, (offk + deg[k])
                                    ), slice(
                                        offl, (offl + deg[l])
                                    ), slice(
                                        offm, (offm + deg[m])
                                    ), slice(
                                        offn, (offn + deg[n])
                                    ), slice(
                                        offo, (offo + deg[o])
                                    ), slice(
                                        offp, (offp + deg[p])
                                    )
                                    offp += deg[p]
                                offo += deg[o]
                            offn += deg[n]
                        offm += deg[m]
                    offl += deg[l]
                offk += deg[k]
            offj += deg[j]
        offi += deg[i]


# above, cut from dense to quantum number (index + matrix)


def suzu_trotter_exp_to_blocs(
    arg,
    id_dense,
    on_site_left,
    on_site_right,
    nn_bond,
    is_dgate,
    *,
    degenerate_list,
    dense_d
):
    # for gate : GOES OUT IN SSWW order
    # # [('s',(l+1)),('s',(l+2)),('W',(l+1)),('W',(l+2))])
    #
    # for dgate : GOES OUT IN SSWW-SSWW order
    # # [('s',(l+1)),('s',(l+2)),('W',(l+1)),('W',(l+2)),('W',-(l+1)),('W',-(l+2)),('s',-(l+1)),('s',-(l+2))])
    #
    # deg = _models.basis[quantum_name]["deg"]
    fake_d = len(degenerate_list)
    t = _suzu_trotter_exp_numpy(
        arg, id_dense, on_site_left, on_site_right, nn_bond, is_dgate, d=dense_d
    )

    blocks = {}
    if is_dgate == False:
        for i, j, k, l, si, sj, sk, sl in _generate_slices(fake_d, degenerate_list):
            tmp = t[si, sj, sk, sl]
            if not _np.all(tmp == 0):
                tmp.setflags(write=0)
                blocks[(i, j, k, l)] = tmp
    else:
        for (
            i,
            j,
            k,
            l,
            m,
            n,
            o,
            p,
            si,
            sj,
            sk,
            sl,
            sm,
            sn,
            so,
            sp,
        ) in _generate_slices_dgate(fake_d, degenerate_list):
            tmp = t[si, sj, sk, sl, sm, sn, so, sp]
            if not _np.all(tmp == 0):
                tmp.setflags(write=0)
                blocks[(i, j, k, l, m, n, o, p)] = tmp
    return blocks


def suzu_trotter_obc_exp(arg, model_name, parameters, size, is_dgate, in_group):
    # for gate : GOES OUT IN SSWW order
    # # [('s',(l+1)),('s',(l+2)),('W',(l+1)),('W',(l+2))])
    #
    # for dgate : GOES OUT IN SSWW-SSWW order
    # # [('s',(l+1)),('s',(l+2)),('W',(l+1)),('W',(l+2)),('W',-(l+1)),('W',-(l+2)),('s',-(l+1)),('s',-(l+2))])
    #
    mpo = []

    head, mod, tail = model_name.split("_")
    if head == "sh" and tail == "no":
        degenerate_list = [2]
        dense_d = 2
    elif head == "sh" and tail == "u1":
        degenerate_list = [1, 1]
        dense_d = 2
    elif head == "so" and tail == "no":
        degenerate_list = [3]
        dense_d = 3
    elif head == "so" and tail == "u1":
        degenerate_list = [1, 1, 1]
        dense_d = 3
    elif head == "ru" and tail == "u1":
        degenerate_list = [1, 2, 1]
        dense_d = 4
    else:
        degenerate_list = [4]
        dense_d = 4

    id_dense = single_operator(name=head + "_id_no", coef=1.0)
    on_site = on_site_operators_from_hamiltonian(head + "_" + mod + "_no", parameters)
    on_site_left_border = on_site_fuse_for_mpo(on_site)
    on_site_right_border = on_site_fuse_for_mpo(on_site)
    on_site = on_site_fuse_for_mpo(on_site, coef=1.0 / 2.0)

    # fuse
    nn_bond = nn_bond_operators_from_hamiltonian(head + "_" + mod + "_no", parameters)

    for l in range(size - 1):
        if l == 0:
            eff_on_site_left = on_site_left_border
        else:
            eff_on_site_left = on_site

        if l == size - 2:
            eff_on_site_right = on_site_right_border
        else:
            eff_on_site_right = on_site

        if is_dgate and in_group:
            tmporary = suzu_trotter_exp_to_blocs(
                arg,
                id_dense,
                eff_on_site_left,
                eff_on_site_right,
                nn_bond,
                is_dgate,
                degenerate_list=degenerate_list,
                dense_d=dense_d,
            )
            tmp = {}
            _group_four_dgate(model_name, tmp, tmporary)
        else:
            tmp = suzu_trotter_exp_to_blocs(
                arg,
                id_dense,
                eff_on_site_left,
                eff_on_site_right,
                nn_bond,
                is_dgate,
                degenerate_list=degenerate_list,
                dense_d=dense_d,
            )
        mpo.append(tmp)

    return mpo
