import numpy as _np


def prepare_index_target_no_gate(lhs_indices, rhs_indices):
    # not sure it will work...
    target_key12 = []
    for it1 in lhs_indices:
        for it2 in rhs_indices:
            if it1[2] == it2[0]:
                target_key12.append(((it1[0], it1[1], it2[1], it2[2]), it1, it2))
    if len(target_key12) == 0:
        raise ("No targeted indices possible for contraction")
    target_key12_zipped = list(zip(*sorted(target_key12)))
    tmp = []
    for l in range(len(target_key12_zipped[0])):
        if target_key12_zipped[0].index(target_key12_zipped[0][l]) == l:
            tmp.append(
                (
                    True,
                    target_key12_zipped[0][l],
                    target_key12_zipped[1][l],
                    target_key12_zipped[2][l],
                )
            )
        else:
            tmp.append(
                (
                    False,
                    target_key12_zipped[0][l],
                    target_key12_zipped[1][l],
                    target_key12_zipped[2][l],
                )
            )
    return tmp


def prepare_index_target_with_gate(lhs_indices, rhs_indices, th_indices):
    index_target_tmp = prepare_index_target_no_gate(lhs_indices, rhs_indices)
    pass


def prepare_targets(old_blocks1, old_blocks2, index2contract):
    target_key12 = []
    for it1 in old_blocks1.keys():
        for it2 in old_blocks2.keys():
            if _np.all(
                [
                    (it1[index2contract[0][i]] == it2[index2contract[1][i]])
                    for i in range(len(index2contract[0]))
                ]
            ):
                target_key12.append(
                    (
                        tuple(
                            [
                                it1[i]
                                for i in xrange(len(it1))
                                if i not in index2contract[0]
                            ]
                            + [
                                it2[i]
                                for i in xrange(len(it2))
                                if i not in index2contract[1]
                            ]
                        ),
                        it1,
                        it2,
                    )
                )

    tmp = []
    if len(target_key12) != 0:
        target_key12 = zip(*sorted(target_key12))
        for l in range(len(target_key12[0])):
            if target_key12[0].index(target_key12[0][l]) == l:
                tmp.append(
                    (True, target_key12[0][l], target_key12[1][l], target_key12[2][l])
                )
            else:
                tmp.append(
                    (False, target_key12[0][l], target_key12[1][l], target_key12[2][l])
                )
    return tmp


def contract_arrays(new_blocks, old_blocks1, old_blocks2, index2contract, buildtarget):
    for new, target, it1, it2 in buildtarget:
        if new:
            new_blocks[target] = _np.tensordot(
                old_blocks1[it1],
                old_blocks2[it2],
                axes=[index2contract[0], index2contract[1]],
            )
        else:
            new_blocks[target] += _np.tensordot(
                old_blocks1[it1],
                old_blocks2[it2],
                axes=[index2contract[0], index2contract[1]],
            )


def multiply_blocs(new_blocks, lhs_blocks, rhs_blocks, index2contract, buildtarget):
    new_blocks = {}
    buildtarget = prepare_targets(lhs_blocks, rhs_blocks, index2contract)
    contract_arrays(new_blocks, lhs_blocks, rhs_blocks, index2contract, buildtarget)


def multiply_blocs():
    pass


def multiply_blocs_with_gate():
    pass
