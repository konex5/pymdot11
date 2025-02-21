import numpy as _np


def prepare_index_target_no_gate(
    lhs_indices, rhs_indices, left_conservation=False, right_conservation=False
):
    target_key12 = []
    for it1 in lhs_indices:
        for it2 in rhs_indices:
            if not left_conservation:
                keep_it_left = True
            elif left_conservation and it1[0] + it1[1] == it1[2]:  # simple qnum
                keep_it_left = True
            else:
                keep_it_left = False
            if not right_conservation:
                keep_it_right = True
            elif right_conservation and it2[0] == it2[1] + it2[2]:  # simple qnum
                keep_it_right = True
            else:
                keep_it_right = False
            if it1[2] == it2[0] and keep_it_left and keep_it_right:
                target_key12.append(((it1[0], it1[1], it2[1], it2[2]), it1, it2))

    if len(target_key12) == 0:
        raise ("No targeted indices possible for contraction")
    target_key12_zipped = list(zip(*sorted(target_key12)))
    tmp = []
    for l in range(len(target_key12_zipped[0])):
        if target_key12_zipped[0].index(target_key12_zipped[0][l]) == l:
            is_degenerate = True
        else:
            is_degenerate = False
        tmp.append(
            (
                is_degenerate,
                target_key12_zipped[0][l],
                target_key12_zipped[1][l],
                target_key12_zipped[2][l],
            )
        )
    return tmp


def prepare_index_target_with_gate(
    index_target_no_gate, theta_indices, left_right_conservation=False
):
    target_key12_with_theta = []
    for before_theta_indices in index_target_no_gate:
        for th_indices in theta_indices:
            if not left_right_conservation:
                keep_it_left_right = True
            elif (
                left_right_conservation
                and before_theta_indices[0] + th_indices[0]
                == th_indices[1] + before_theta_indices[3]
            ):  # simple qnum
                keep_it_left_right = True
            else:
                keep_it_left_right = False
            if (
                before_theta_indices[1] == th_indices[2]
                and before_theta_indices[2] == th_indices[3]
            ) and keep_it_left_right:
                target_key12_with_theta.append(
                    (
                        (
                            before_theta_indices[0],
                            th_indices[0],
                            th_indices[1],
                            before_theta_indices[3],
                        ),
                        th_indices,
                        before_theta_indices,
                    )
                )
    if len(target_key12_with_theta) == 0:
        raise ("No targeted indices possible for contraction")
    target_key12_with_theta_zipped = list(zip(*sorted(target_key12_with_theta)))
    tmp = []
    for l in range(len(target_key12_with_theta_zipped[0])):
        if (
            target_key12_with_theta_zipped[0].index(
                target_key12_with_theta_zipped[0][l]
            )
            == l
        ):
            is_degenerate = True
        else:
            is_degenerate = False
        tmp.append(
            (
                is_degenerate,
                target_key12_with_theta_zipped[0][l],
                target_key12_with_theta_zipped[1][l],
                target_key12_with_theta_zipped[2][l],
            )
        )
    return tmp


def multiply_blocs_no_gate(lhs_blocs, rhs_blocs):
    dest_blocs = {}
    index_target_no_gate = prepare_index_target_no_gate(
        lhs_blocs.keys(), rhs_blocs.keys()
    )
    for new, target, it1, it2 in index_target_no_gate:
        if new:
            dest_blocs[target] = _np.tensordot(
                lhs_blocs[it1],
                rhs_blocs[it2],
                axes=[2, 0],
            )
        else:
            dest_blocs[target] += _np.tensordot(
                lhs_blocs[it1],
                rhs_blocs[it2],
                axes=[2, 0],
            )
    return dest_blocs


def multiply_blocs_with_gate(lhs_blocs, rhs_blocs, theta_blocs):
    tmp_blocs = multiply_blocs_no_gate(lhs_blocs, rhs_blocs)
    dest_blocs = {}
    index_target_with_gate = prepare_index_target_with_gate(
        tmp_blocs.keys(), theta_blocs.keys()
    )
    for new, target, it1, it2 in index_target_with_gate:
        if new:
            dest_blocs[target] = _np.tensordot(
                theta_blocs[it1],
                tmp_blocs[it2],
                axes=([2, 3], [1, 2]),
            ).transpose([2, 0, 1, 3])
        else:
            dest_blocs[target] += _np.tensordot(
                theta_blocs[it1],
                tmp_blocs[it2],
                axes=([2, 3], [1, 2]),
            ).transpose([2, 0, 1, 3])
    return dest_blocs


def indices_prepare_destination_without_gate(
    left_indices, right_indices, *, conserve_left_right=False
):
    about_indices_to_contract = []

    for left_index in left_indices:
        for right_index in right_indices:
            if left_index[2] == right_index[0]:
                if (not conserve_left_right) or (
                    conserve_left_right
                    and (
                        left_index[0] + left_index[1] == right_index[1] + right_index[2]
                    )
                ):
                    about_indices_to_contract.append(
                        (
                            (
                                left_index[0],
                                left_index[1],
                                right_index[1],
                                right_index[2],
                            ),
                            left_index,
                            right_index,
                        )
                    )

    return sorted(set(about_indices_to_contract))


def indices_theta_prepare_conservation_for_gate(
    theta_indices, gate_indices, *, conserve_left_right=False
):
    destination_indices = []
    for theta_index in theta_indices:
        for gate_index in gate_indices:
            if gate_index[2] == theta_index[1] and gate_index[3] == theta_index[2]:
                if (not conserve_left_right) or (
                    conserve_left_right
                    and (
                        theta_index[0] + gate_index[0] == gate_index[1] + theta_index[3]
                    )
                ):
                    destination_indices.append(
                        (
                            (
                                theta_index[0],
                                gate_index[0],
                                gate_index[1],
                                theta_index[3],
                            ),
                            theta_index,
                            gate_index,
                        )
                    )

    return sorted(set(destination_indices))


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
    buildtarget = prepare_targets(lhs_blocks, rhs_blocks, index2contract)
    contract_arrays(new_blocks, lhs_blocks, rhs_blocks, index2contract, buildtarget)
