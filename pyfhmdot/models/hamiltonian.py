import numpy as _np
from scipy.linalg import expm as _expm
from numbers import Number as _ntype

import pyfhmdot.pymodels as _models


def _parameters2finalparameters(tupleMlist, parameters):
    """
    input (('M',7.,2),(Sz,1))
    output parameters[2]*7.,(Sz,1)

    input (('EXP',[1./2.,2.j],[0,1]),(SpoSm,1)
    output parameters[0]*1./2. np.exp(2.j*parameters[1]),(SpoSm,1)
    """
    if tupleMlist[0][0] == "M" and len(tupleMlist[0]) == 3:
        return (float(parameters[tupleMlist[0][2]])) * tupleMlist[0][1], tupleMlist[-1]
    # if tupleMlist[1][0]=='MR' and len(tupleMlist[1][-1])==1:
    #     if isinstance(parameters[tupleMlist[0]],list):
    #         return ([float(_)*tupleMlist[1][-1][0] for _ in parameters[tupleMlist[0]]], tupleMlist[-1]
    if tupleMlist[0][0] == "EXP" and len(tupleMlist[0]) == 3:
        return (
            float(parameters[tupleMlist[0][2][0]])
            * tupleMlist[0][1][0]
            * _np.exp(float(parameters[tupleMlist[0][2][1]]) * tupleMlist[0][1][1])
        ), tupleMlist[-1]
    raise (
        Exception("Error in _parameters2finalparameters when constructing hamiltonian")
    )


def _finalparameters2finalperiod(tupleMlistreturned, period):
    return (
        tupleMlistreturned[0],
        tupleMlistreturned[1][0],
        tupleMlistreturned[1][1],
        period,
    )


def _ham4expr2final(ham4expr, period, parameters, finalhamlistreturned):
    for i in xrange(4):
        # 1-ONSITE__2-NEAREST_NEIGHBOR__3-SECOND_NEARESTNEIGHBOR__4-SPECIAL-TERM(like-borders)
        for tupleMlist in ham4expr[i]:
            finalhamlistreturned[i].append(
                _finalparameters2finalperiod(
                    _parameters2finalparameters(tupleMlist, parameters), period
                )
            )
    pass  # returned in finalhamlistreturned


def _appendsubmodel(model, parameters, finalhamlistreturned):
    for submodeltuple in _models.hamiltonian[model]["submodel"]:
        _appendsubmodel(
            submodeltuple[0],
            [parameters[idx] for idx in submodeltuple[1]],
            finalhamlistreturned,
        )
    _ham4expr2final(
        _models.hamiltonian[model]["ham_expr"],
        _models.hamiltonian[model]["period"],
        parameters,
        finalhamlistreturned,
    )
    pass  # returned in finalhamlistreturned


def words_terms(model, parameters):
    #                       site, nearbond, special site, special nearbond,
    finalhamlistreturned = [[], [], [], []]

    # TODO
    # pop zero values (reducing a bit the model)

    _appendsubmodel(model, parameters, finalhamlistreturned)

    return finalhamlistreturned


def operator(name, quantum_name):
    if name in _models.operators.iterkeys():
        if _models.operators[name]["nb_site"] == 1:
            alpha = _models.operators[name]["coef"]
            mat = _models.operators[name]["qBasis"][quantum_name]
            return alpha, mat
        elif _models.operators[name]["nb_site"] == 2:
            alpha = _models.operators[_models.operators[name][0]]["coef"]
            mata = _models.operators[_models.operators[name][0]]["qBasis"][quantum_name]
            beta = _models.operators[_models.operators[name][1]]["coef"]
            matb = _models.operators[_models.operators[name][1]]["qBasis"][quantum_name]
            return (alpha, mata), (beta, matb)
    raise "Unknown in manybody.matrices.operator"


def onsite_fuse_for_mpo(tmpblocks):
    difflab = list(set([tmp[0] for tmp in tmpblocks]))
    outblocks = []
    for lab in difflab:
        for l in xrange(len(tmpblocks)):
            if tmpblocks[l][0] == lab:
                shortlist = [_[0] for _ in outblocks]
                if lab not in shortlist:
                    outblocks.append(tmpblocks[l])
                else:
                    # can only be last # shortlist.index(lab)
                    outblocks[-1][1] += tmpblocks[l][1]
    return outblocks


def infinite_hamiltonian_terms(model, parameters):
    pass


def finite_hamiltonian_terms(qnmodel, parameters, L):
    # no quantum number at this level

    qn, model = _qn_model(qnmodel)
    qname = qn.split("-")[0]
    finalhamlistreturned = words_terms(model, parameters)

    onsiteHam = [[] for l in range(L)]
    onbondHam = [[] for l in range(L - 1)]

    for l in xrange(L):
        for siteOp in finalhamlistreturned[0]:
            if l % siteOp[-1] == siteOp[-2]:  # period modulo
                onsiteHam[l].append((siteOp[0], qname + "-" + siteOp[1]))
    for l in xrange(L - 1):
        for bondOp in finalhamlistreturned[1]:
            if l % bondOp[-1] == bondOp[-2]:  # period modulo
                onbondHam[l].append((bondOp[0], qname + "-" + bondOp[1]))

    for siteOp in finalhamlistreturned[2]:
        # siteOp=(factor,opera,0,period)
        if siteOp[-1] != -1:
            print("Why is there a special term with periodicity?")
        if siteOp[2][0] == "LEFT":
            from_l = 1
        elif siteOp[2][0] == "RIGHT":
            from_l = L
        elif siteOp[2][0] == "MIDDLE":
            from_l = L / 2
        else:
            raise (Exception("special should have word LEFT/RIGHT or MIDDLE"))
        l = from_l + siteOp[2][1] - 1
        onsiteHam[l].append((siteOp[0], qname + "-" + siteOp[1]))

    for bondOp in finalhamlistreturned[3]:
        # bondOp=(factor,opera,0,period)
        if bondOp[-1] != -1:
            print("Why is there a special term with periodicity?")
        if bondOp[2][0] == "LEFT":
            from_l = 1
        elif bondOp[2][0] == "RIGHT":
            from_l = L - 1
        elif bondOp[2][0] == "MIDDLE":
            from_l = (L - 1) / 2
        else:
            raise (Exception("special should have word LEFT/RIGHT or MIDDLE"))
        l = from_l + bondOp[2][1] - 1
        onbondHam[l].append((bondOp[0], qname + "-" + bondOp[1]))

    # print(onsiteHam,onbondHam)
    return onsiteHam, onbondHam


def _hamiltonian_mpo_period2(site_M, bond_L, bond_R, quantum_name):
    bl_dimL = len(bond_L) + 1
    bl_dimR = len(bond_R) + 1
    # bonds, sites, special, boundaries = _hamiltonian_terms(model, param)
    blocks = []

    # id
    alpha, idval = operator(quantum_name.split("-")[0] + "-Id", quantum_name)
    for idx, val in idval:
        blocks.append(
            [
                (0, idx[0], idx[1], 0),
                alpha * val.reshape(tuple([1] + list(val.shape) + [1])),
            ]
        )
        blocks.append(
            [
                (bl_dimL, idx[0], idx[1], bl_dimR),
                alpha * val.reshape(tuple([1] + list(val.shape) + [1])),
            ]
        )

    # on site
    tmpblocks = []
    for param, name in site_M:
        if isinstance(param, _ntype):
            alpha, idval = operator(name, quantum_name)
            for idx, val in idval:
                tmpblocks.append(
                    [
                        (bl_dimL, idx[0], idx[1], 0),
                        param * alpha * val.reshape(tuple([1] + list(val.shape) + [1])),
                    ]
                )
    addblocks = onsite_fuse_for_mpo(tmpblocks)
    for l in range(len(addblocks)):
        blocks.append(addblocks.pop())
    # Super important above, sum of on site operator

    # bond
    i = 0
    for param, name in bond_L:
        i += 1
        if isinstance(param, _ntype):
            (alpha, idvala), (beta, idvalb) = operator(name, quantum_name)
            for idxb, valb in idvalb:
                blocks.append(
                    [
                        (i, idxb[0], idxb[1], 0),
                        beta * valb.reshape(tuple([1] + list(valb.shape) + [1])),
                    ]
                )
    i = 0
    for param, name in bond_R:
        i += 1
        if isinstance(param, _ntype):
            (alpha, idvala), (beta, idvalb) = operator(name, quantum_name)
            for idxa, vala in idvala:
                blocks.append(
                    [
                        (bl_dimL, idxa[0], idxa[1], i),
                        param
                        * alpha
                        * vala.reshape(tuple([1] + list(vala.shape) + [1])),
                    ]
                )

    return blocks


# def _hamiltonian_mpo_period3(onsite_M,bond_L,bond_R,quantum_name):
#     pass
# def _hamiltonian_mpo_period4(onsite_M,bond_L,bond_R,quantum_name):
#     pass


def _hamiltonian_mpo_leftborder(site_M, bond_R, quantum_name):
    bl_dimR = len(bond_R) + 1

    blocks = []
    # id
    alpha, val = operator(quantum_name.split("-")[0] + "-Id", quantum_name)
    for idx, val in val:
        blocks.append(
            [
                (0, idx[0], idx[1], bl_dimR),
                alpha * val.reshape(tuple([1] + list(val.shape) + [1])),
            ]
        )

    # on site
    tmpblocks = []
    for param, name in site_M:
        if isinstance(param, _ntype):
            alpha, idval = operator(name, quantum_name)
            for idx, val in idval:
                tmpblocks.append(
                    [
                        (0, idx[0], idx[1], 0),
                        param * alpha * val.reshape(tuple([1] + list(val.shape) + [1])),
                    ]
                )
    addblocks = onsite_fuse_for_mpo(tmpblocks)
    for l in range(len(addblocks)):
        blocks.append(addblocks.pop())

    # bond
    i = 0
    for param, name in bond_R:
        i += 1
        (alpha, idvala), (beta, idvalb) = operator(name, quantum_name)
        for idxa, vala in idvala:
            blocks.append(
                [
                    (0, idxa[0], idxa[1], i),
                    param * alpha * vala.reshape(tuple([1] + list(vala.shape) + [1])),
                ]
            )

    return blocks


def _hamiltonian_mpo_rightborder(site_M, bond_L, quantum_name):
    bl_dimL = len(bond_L) + 1

    blocks = []
    # id
    alpha, val = operator(quantum_name.split("-")[0] + "-Id", quantum_name)
    for idx, val in val:
        blocks.append(
            [
                (0, idx[0], idx[1], 0),
                alpha * val.reshape(tuple([1] + list(val.shape) + [1])),
            ]
        )

    # on site
    tmpblocks = []
    for param, name in site_M:
        if isinstance(param, _ntype):
            alpha, idval = operator(name, quantum_name)
            for idx, val in idval:
                tmpblocks.append(
                    [
                        (bl_dimL, idx[0], idx[1], 0),
                        param * alpha * val.reshape(tuple([1] + list(val.shape) + [1])),
                    ]
                )
    addblocks = onsite_fuse_for_mpo(tmpblocks)
    for l in range(len(addblocks)):
        blocks.append(addblocks.pop())

    # bond
    i = 0
    for param, name in bond_L:
        i += 1
        (alpha, idvala), (beta, idvalb) = operator(name, quantum_name)
        for idxb, valb in idvalb:
            blocks.append(
                [
                    (i, idxb[0], idxb[1], 0),
                    beta * valb.reshape(tuple([1] + list(valb.shape) + [1])),
                ]
            )

    return blocks


def hamiltonian_obc(qnmodel, param, L):
    """
    qnmodel='sh-xxz-hz' or 'ldsh-ldxxz-hz'
    """
    qn, model = _qn_model(qnmodel)

    mpo = []
    onsite, onbond = finite_hamiltonian_terms(qnmodel, param, L)

    for l in xrange(L):
        if l == 0:
            mpo.append(_hamiltonian_mpo_leftborder(onsite[0], onbond[0], qn))
        elif l == L - 1:
            mpo.append(_hamiltonian_mpo_rightborder(onsite[L - 1], onbond[L - 2], qn))
        else:
            mpo.append(
                _hamiltonian_mpo_period2(onsite[l], onbond[l - 1], onbond[l], qn)
            )
    return mpo


############################################################
############################################################
############################################################


############################################################
############################################################
############################################################


def _gate_ham_period2_numpy(site_L, site_R, bond_M, quantum_name):
    quantum_name_NONE = quantum_name.split("-")[0] + "-None"
    d = _models.basis[quantum_name_NONE]["deg"][0]

    if (
        _np.any([isinstance(x[0], complex) for x in site_L])
        or _np.any([isinstance(x[0], complex) for x in site_R])
        or _np.any([isinstance(x[0], complex) for x in bond_M])
    ):
        t = _np.ndarray((d, d, d, d), dtype="complex128")
        t.fill(0)
    else:
        t = _np.ndarray((d, d, d, d))
        t.fill(0)

    # id
    alphaId, Id = operator(quantum_name.split("-")[0] + "-Id", quantum_name_NONE)

    # on site_L
    for param, name in site_L:
        if isinstance(param, _ntype):

            alpha, mat = operator(name, quantum_name_NONE)
            t[:, :, :, :] += (
                param * _np.outer(alpha * mat[0][-1], alphaId * Id[0][-1])
            ).reshape(d, d, d, d)

    # on site_R
    for param, name in site_R:
        if isinstance(param, _ntype):
            alpha, mat = operator(name, quantum_name_NONE)
            t[:, :, :, :] += (
                param * _np.outer(alphaId * Id[0][-1], alpha * mat[0][-1])
            ).reshape(d, d, d, d)

    # bond
    for param, name in bond_M:
        if isinstance(param, _ntype):
            (alpha, mata), (beta, matb) = operator(name, quantum_name_NONE)
            t[:, :, :, :] += (
                param * _np.outer(alpha * mata[0][-1], beta * matb[0][-1])
            ).reshape(d, d, d, d)

    return t


# def _gate_ham_period3_numpy(site_L,site_R,bond_M,quantum_name):
#     pass
# def _gate_ham_period4_numpy(site_L,site_R,bond_M,quantum_name):
#     pass

############################################################
############################################################
############################################################


def _exp_gate(arg, dH, d):
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


def _exp_dgate(arg, dH, d):
    ### TMP correspond to exp(+arg dH)
    tmp = _exp_gate(arg, dH, d)
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

    # REMARK ABOUT TIME EVOLUTION WITH COMPLEX HAMILTONIAN !
    #
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
    #
    # REMARK ENDED HERE !

    ###
    # # CORRECT BUT ALONE!
    # dU1 = _np.outer(tmp.reshape(d**4),_np.eye(d**2,d**2).reshape(d**4)).reshape(d,d,d,d,d,d,d,d)
    # dU1 = _np.outer(_np.eye(d**2,d**2).reshape(d**4),tmp.reshape(d**4)).reshape(d,d,d,d,d,d,d,d)
    # # CORRECT BUT ALONE!

    # dU2b = _np.outer(_np.conjugate(tmp).reshape(d**4),tmp.reshape(d**4)).reshape(d,d,d,d,d,d,d,d)
    # #dU2b=>[('s',-(l+1)),('s',-(l+2)),('W',-(l+1)),('W',-(l+2)),('W',+(l+1)),('W',+(l+2)),('s',+(l+1)),('s',+(l+2))]

    dU2 = _np.outer(_np.conjugate(tmp).reshape(d ** 4), tmp.reshape(d ** 4)).reshape(
        d, d, d, d, d, d, d, d
    )
    # dU2=>[('s',-(l+1)),('s',-(l+2)),('W',-(l+1)),('W',-(l+2)),('W',+(l+1)),('W',+(l+2)),('s',+(l+1)),('s',+(l+2))]
    # dU.setflags(write=0)
    return dU2


############################################################
############################################################
############################################################


def _suzu_trotter_period2_exp_numpy(arg, site_L, site_R, bond_M, quantum_name, dgate):
    quantum_name_NONE = quantum_name.split("-")[0] + "-None"
    d = _models.basis[quantum_name_NONE]["deg"][0]

    dH = _gate_ham_period2_numpy(site_L, site_R, bond_M, quantum_name)
    if dgate == False:
        return _exp_gate(arg, dH, d)
    else:
        return _exp_dgate(arg, dH, d)


# def gate_periodicity_two_suzu_trotter_exp_numpy(arg,model,param,numtype):
#     pass
# def gate_periodicity_ofL_suzu_trotter_exp_numpy(arg,L,model,param,numtype):
#     pass

############################################################
############################################################
############################################################

# below, cut from dense to quantum number (index + matrix)
def _generate_slices(d, deg):
    offi = 0
    for i in xrange(d):
        offj = 0
        for j in xrange(d):
            offk = 0
            for k in xrange(d):
                offl = 0
                for l in xrange(d):
                    yield i, j, k, l, slice(offi, (offi + deg[i])), slice(
                        offj, (offj + deg[j])
                    ), slice(offk, (offk + deg[k])), slice(offl, (offl + deg[l]))
                    offl += deg[l]
                offk += deg[k]
            offj += deg[j]
        offi += deg[i]


def _generate_slices_dgate(d, deg):
    offi = 0
    for i in xrange(d):
        offj = 0
        for j in xrange(d):
            offk = 0
            for k in xrange(d):
                offl = 0
                for l in xrange(d):
                    offm = 0
                    for m in xrange(d):
                        offn = 0
                        for n in xrange(d):
                            offo = 0
                            for o in xrange(d):
                                offp = 0
                                for p in xrange(d):
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

############################################################
############################################################
############################################################


def suzu_trotter_period2_exp(arg, site_L, site_R, bond_M, quantum_name, dgate):
    # for gate : GOES OUT IN SSWW order
    # # [('s',(l+1)),('s',(l+2)),('W',(l+1)),('W',(l+2))])
    #
    # for dgate : GOES OUT IN SSWW-SSWW order
    # # [('s',(l+1)),('s',(l+2)),('W',(l+1)),('W',(l+2)),('W',-(l+1)),('W',-(l+2)),('s',-(l+1)),('s',-(l+2))])
    #
    deg = _models.basis[quantum_name]["deg"]
    d = len(deg)
    t = _suzu_trotter_period2_exp_numpy(
        arg, site_L, site_R, bond_M, quantum_name, dgate
    )

    blocks = []
    if dgate == False:
        for i, j, k, l, si, sj, sk, sl in _generate_slices(d, deg):
            tmp = t[si, sj, sk, sl]
            if not _np.all(tmp == 0):
                tmp.setflags(write=0)
                blocks.append([[i, j, k, l], tmp])
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
        ) in _generate_slices_dgate(d, deg):
            tmp = t[si, sj, sk, sl, sm, sn, so, sp]
            if not _np.all(tmp == 0):
                tmp.setflags(write=0)
                blocks.append([[i, j, k, l, m, n, o, p], tmp])
    return blocks


############################################################


def suzu_trotter_obc_exp(arg, qnmodel, param, L, dgate):
    # for gate : GOES OUT IN SSWW order
    # # [('s',(l+1)),('s',(l+2)),('W',(l+1)),('W',(l+2))])
    #
    # for dgate : GOES OUT IN SSWW-SSWW order
    # # [('s',(l+1)),('s',(l+2)),('W',(l+1)),('W',(l+2)),('W',-(l+1)),('W',-(l+2)),('s',-(l+1)),('s',-(l+2))])
    #
    qname = qnmodel.split("-")[0]
    # if qname[0:2]=='ld':
    #     model = 'ld-'+qnmodel.split(qname+'-')[-1]
    # else:
    #     model = qnmodel.split(qname+'-')[-1]

    quantum_name = (
        qname
        + "-"
        + _models.hamiltonian[qnmodel.split(qname + "-")[-1]]["qname_ideal"][0]
    )

    mpo = []
    onsite, onbond = finite_hamiltonian_terms(qnmodel, param, L)

    for l in xrange(L - 1):
        if l == 0:
            effectif_onsite_L = onsite[l]
        else:
            effectif_onsite_L = [(param / 2.0, name) for param, name in onsite[l]]

        if l == L - 2:
            effectif_onsite_R = onsite[L - 1]
        else:
            effectif_onsite_R = [(param / 2.0, name) for param, name in onsite[l + 1]]

        effectif_onbond = onbond[l]
        mpo.append(
            suzu_trotter_period2_exp(
                arg,
                effectif_onsite_L,
                effectif_onsite_R,
                effectif_onbond,
                quantum_name,
                dgate,
            )
        )

    return mpo


############################################################
# MATRICES ARE CORRECT!
# manybody.models.quantum_name = 'sh-None'
# A = manybody.matrices.suzu_trotter_obc_exp(-0.02,'sh-xxz-hz',[1,1,2],10,True)[0]
# manybody.models.quantum_name = 'sh-U1'
# B = manybody.matrices.suzu_trotter_obc_exp(-0.02,'sh-xxz-hz',[1,1,2],10,True)[0]
# for i in xrange(len(B)):
#     print(B[i][1][0,0,0,0] == A[0][1][tuple(B[i][0])])
