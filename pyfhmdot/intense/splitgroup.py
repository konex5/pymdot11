import numpy as _np
from pyfhmdot.intense.mul_mp import (
    permute_blocs,
)


def splitgroup_mapping(model_name, *, section):
    head, _, tail = model_name.split("_")
    mapping_name = head + "_" + tail
    mapping = {
        "sh_no": {"deg": [2], "2deg": [4], "map": [[(0, 0)], [0], [slice(0, 4)]]},
        "sh_u1": {
            "deg": [1, 1],
            "2deg": [1, 2, 1],
            "map": [
                [(0, 0), (0, 1), (1, 0), (1, 1)],
                [1, 0, 2, 1],
                [slice(0, 1), slice(0, 1), slice(0, 1), slice(1, 2)],
            ],
        },
        "so_no": {"deg": [3], "2deg": [9], "map": [[(0, 0)], [0], [slice(0, 9)]]},
        "so_u1": {
            "deg": [1, 1, 1],
            "2deg": [1, 2, 3, 2, 1],
            "map": [
                [
                    (0, 0),
                    (0, 1),
                    (0, 2),
                    (1, 0),
                    (1, 1),
                    (1, 2),
                    (2, 0),
                    (2, 1),
                    (2, 2),
                ],
                [2, 1, 0, 3, 2, 1, 4, 3, 2],
                [
                    slice(0, 1),
                    slice(0, 1),
                    slice(0, 1),
                    slice(0, 1),
                    slice(1, 2),
                    slice(1, 2),
                    slice(0, 1),
                    slice(1, 2),
                    slice(2, 3),
                ],
            ],
        },
        "ru_no": {"deg": [4], "2deg": [16], "map": [[(0, 0)], [0], [slice(0, 16)]]},
        "ru_u1": {
            "deg": [1, 2, 1],
            "2deg": [1, 4, 6, 4, 1],
            "map": [
                [
                    (0, 0),
                    (0, 1),
                    (0, 2),
                    (1, 0),
                    (1, 1),
                    (1, 2),
                    (2, 0),
                    (2, 1),
                    (2, 2),
                ],
                [2, 1, 0, 3, 2, 1, 4, 3, 2],
                [
                    slice(0, 1),
                    slice(0, 2),
                    slice(0, 1),
                    slice(0, 2),
                    slice(1, 5),
                    slice(2, 4),
                    slice(0, 1),
                    slice(2, 4),
                    slice(5, 6),
                ],
            ],
        },
    }
    return mapping[mapping_name][section]


def reshape_and_group(model_name, newblocks, oldblocks, indices):
    mapping = splitgroup_mapping(model_name, section="map")
    target_constructed = []
    for it in oldblocks.keys():
        tup2group = (it[indices[0]], it[indices[1]])
        idmap = mapping[0].index(tup2group)
        valuegrouped = mapping[1][idmap]
        dest_key = tuple(
            [it[i] for i in range(indices[0])]
            + [valuegrouped]
            + [it[i] for i in range(indices[1] + 1, len(it))]
        )
        oldshape = oldblocks[it].shape
        if dest_key not in target_constructed:
            totalshape = tuple(
                [oldshape[i] for i in range(indices[0])]
                + [splitgroup_mapping(model_name,
                                      section="2deg")[valuegrouped]]
                + [oldshape[i] for i in range(indices[1] + 1, len(it))]
            )
            newblocks[dest_key] = _np.ndarray(
                (totalshape), oldblocks[it].dtype)
            newblocks[dest_key].fill(0)
            target_constructed.append(dest_key)

        newshape = tuple(
            [oldshape[i] for i in range(indices[0])]
            + [oldshape[indices[0]] * oldshape[indices[1]]]
            + [oldshape[i] for i in range(indices[1] + 1, len(oldshape))]
        )
        newsliced = tuple(
            [slice(0, oldshape[i]) for i in range(indices[0])]
            + [mapping[2][idmap]]
            + [slice(0, oldshape[i])
               for i in range(indices[1] + 1, len(oldshape))]
        )

        newblocks[dest_key][newsliced] = oldblocks[it].reshape(newshape)


def reshape_and_split(model_name, newblocks, oldblocks, index):
    mapping = splitgroup_mapping(model_name, section="map")
    for it in oldblocks.keys():
        int2split = it[index]
        if mapping[1].count(int2split) == 1:
            idmap = mapping[1].index(int2split)
            valuesplited = mapping[0][idmap]
            dest_key = tuple(
                [it[i] for i in range(index)]
                + list(valuesplited)
                + [it[i] for i in range(index + 1, len(it))]
            )
            oldshape = oldblocks[it].shape
            newshape = tuple(
                [oldshape[i] for i in range(index)]
                + [int(_np.sqrt(oldshape[index])),
                   int(_np.sqrt(oldshape[index]))]
                + [oldshape[i] for i in range(index + 1, len(it))]
            )
            newblocks[dest_key] = oldblocks[it].reshape(newshape)
        else:
            for idmap in [i for i, x in enumerate(mapping[1]) if x == int2split]:
                valuesplited = mapping[0][idmap]
                dest_key = tuple(
                    [it[i] for i in range(index)]
                    + list(valuesplited)
                    + [it[i] for i in range(index + 1, len(it))]
                )
                oldshape = oldblocks[it].shape

                newsliced = tuple(
                    [slice(0, oldshape[i]) for i in range(index)]
                    + [mapping[2][idmap]]
                    + [slice(0, oldshape[i])
                       for i in range(index + 1, len(oldshape))]
                )
                tmp = oldblocks[it][newsliced]

                deg_map = splitgroup_mapping(model_name, section="deg")
                dimL = deg_map[mapping[0][idmap][0]]
                dimR = deg_map[mapping[0][idmap][1]]
                lastshape = tuple(
                    [oldshape[i] for i in range(index)]
                    + [dimL, dimR]
                    + [oldshape[i] for i in range(index + 1, len(oldshape))]
                )

                newblocks[dest_key] = tmp.reshape(lastshape)


def group_four_dgate(model_name, dst_dgate, dgate):
    # for dgate : GOES OUT IN SSWW-SSWW order
    # # [('s',(l+1)),('s',(l+2)),('W',(l+1)),('W',(l+2)),('W',-(l+1)),('W',-(l+2)),('s',-(l+1)),('s',-(l+2))])
    tmp_four = {}
    for key, values in dgate.items():
        tmp_four[
            (key[4], key[0], key[6], key[2], key[7], key[3], key[5], key[1])
        ] = values.transpose(4, 0, 6, 2, 7, 3, 5, 1)
    tmp_fou = {}
    reshape_and_group(model_name, tmp_fou, tmp_four, [0, 1])
    tmp_fo = {}
    reshape_and_group(model_name, tmp_fo, tmp_fou, [1, 2])
    tmp_f = {}
    reshape_and_group(model_name, tmp_f, tmp_fo, [2, 3])
    reshape_and_group(model_name, dst_dgate, tmp_f, [3, 4])


def split_four_dgate(model_name, dst_dgate, dgate):
    tmp_f = {}
    reshape_and_split(model_name, tmp_f, dgate, 3)
    tmp_fo = {}
    reshape_and_split(model_name, tmp_fo, tmp_f, 2)
    tmp_fou = {}
    reshape_and_split(model_name, tmp_fou, tmp_fo, 1)
    tmp_four = {}
    reshape_and_split(model_name, tmp_four, tmp_fou, 0)
    for key, values in tmp_four.items():
        if _np.any(values != 0):
            dst_dgate[
                (key[1], key[7], key[3], key[5], key[0], key[6], key[2], key[4])
            ] = values.transpose(1, 7, 3, 5, 0, 6, 2, 4)


def group_dmps(model_name, dst_dmp, mp):
    reshape_and_group(model_name, dst_dmp, mp, [1, 2])


def split_dmps(model_name, dst_mp, dmp):
    reshape_and_split(model_name, dst_mp, dmp, 1)


def group_mpos(model_name,dst_mp,mpos):
    # mpos
    #    2| |4
    # 0 -|___|- 5
    #    1| |3
    tmp = {}
    permute_blocs(tmp,mpos,[(0,1,2,3,4,5),(0,1,4,2,4,5)])
    # mpos
    #    3| |4
    # 0 -|___|- 5
    #    1| |2
    tmp_tmp = {}
    reshape_and_group(model_name, tmp_tmp, tmp, [1, 2])
    reshape_and_group(model_name, dst_mp, tmp_tmp, [2, 3])
    #    2||
    # 0 -|___|- 3
    #    1||
    


def group_all(model_name, dmps):
    dmps_out = []
    for i, tmp in enumerate(dmps):
        _ = {}
        group_dmps(model_name, _, tmp)
        dmps_out.append(_)
    return dmps_out


def split_all(model_name, dmps):
    dmps_out = []
    for i, tmp in enumerate(dmps):
        _ = {}
        split_dmps(model_name, _, tmp)
        dmps_out.append(_)
    return dmps_out
