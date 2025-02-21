import numpy as _np
from scipy.linalg import expm as _expm
from numbers import Number as _ntype


def read_parameters(line: str):
    param_name, param_value_str = line.split('=')
    if param_name[-4:] == "_EXP":
        rad, ang = param_value_str.split(',')
        return param_name, (float(rad),float(ang))
    elif param_name[-5:] == "_LIST":
        return param_name, [float(_) for _ in param_value_str.split(',')]
    else:
        return param_name, float(param_value_str)



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
    if tupleMlist[0][0] == "_EXP" and len(tupleMlist[0]) == 3:
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
