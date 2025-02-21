import os
import toml
import json
import sys

from typing import List
import numpy as _np
from scipy.linalg import expm as _expm
from numbers import Number as _ntype

# example JSON<->BOOST compatible
# toml.dumps({"xy":{"a":1, "b_EXP":(2,3),"c_LIST":[1,2,3,4,5,6]},"zz": {"Jz":1}})


def check_filename_and_extension(filename: str) -> bool:
    ext = os.path.splitext(filename)[-1]
    valid_file = os.path.exists(filename) and (ext in [".json", ".toml"])
    return valid_file


def read_filename(filename: str) -> dict:
    if not check_filename_and_extension(filename):
        sys.exit(
            f"The file {filename} is not valid. Check extension (json or toml) and path."
        )
    with open(filename, "r") as file:
        if os.path.splitext(filename)[-1] == ".json":
            return json.loads(file.read())
        elif os.path.splitext(filename)[-1] == ".toml":
            return toml.loads(file.read())


def write_filename(filename: str, params: dict) -> dict:
    with open(filename, "w") as file:
        if os.path.splitext(filename)[-1] == ".json":
            file.write(json.dumps(params))
        elif os.path.splitext(filename)[-1] == ".toml":
            file.write(toml.dumps(params))


"""
def _ham4expr2final(ham4expr, period, parameters, finalhamlistreturned):
    for i in range(4):
        # 1-ONSITE__2-NEAREST_NEIGHBOR__3-SECOND_NEARESTNEIGHBOR__4-SPECIAL-TERM(like-borders)
        for tupleMlist in ham4expr[i]:
            finalhamlistreturned[i].append(
                _finalparameters2finalperiod(
                    _parameters2finalparameters(tupleMlist, parameters), period
                )
            )
    pass  # returned in finalhamlistreturned


def _appendsubmodel(model, parameters, finalhamlistreturned):
    for submodeltuple in models[model]["submodel"]:
        _appendsubmodel(
            submodeltuple[0],
            [parameters[idx] for idx in submodeltuple[1]],
            finalhamlistreturned,
        )
    _ham4expr2final(
        models[model]["ham_expr"],
        models[model]["period"],
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
"""
