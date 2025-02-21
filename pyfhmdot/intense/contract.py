from pyfhmdot.intense.mul_mp import (
    multiply_mp,
    fuse_mp,
    permute_blocs,
    rm_border_mpo,
    trace_mp,
)


def contract_left_right_mpo_mpo_permute(dst, left_bloc, mpo_one, mpo_two, right_bloc):
    # mpo
    #    2|
    # 0 -|_|-3
    #    1|
    mpos = {}
    multiply_mp(mpos, mpo_one, mpo_two, [3], [0])
    # mpos
    #    2| |4
    # 0 -|___|- 5
    #    1| |3
    tmp = {}
    multiply_mp(tmp, left_bloc, mpos, [1], [0])
    mpos.clear()
    # tmp
    # 1   | |_|3, 5|_
    #     |  _  __  _|- 6
    # 0   |_| |2, 4|
    tmp_tmp = {}
    multiply_mp(tmp_tmp, tmp, right_bloc, [6], [1])
    tmp.clear()
    # tmp_tmp
    # 1   | |_|3, 5|_| |   7
    #     |  _  __  _| |
    # 0   |_| |2, 4| | |   6
    permute_blocs(dst, tmp_tmp, [(0, 1, 2, 3, 4, 5, 6, 7), (1, 3, 5, 7, 0, 2, 4, 6)])
    # dst
    # 4   | |_|5, 6|_| |   7
    #     |  _  __  _| |
    # 0   |_| |1, 2| | |   3


def contract_dmps_left_border(dst, dmps):
    # dmps
    #    2|
    # 0 -|_|-3
    #    1|
    trace_mp(dst, dmps, 1, 2)
    # dst
    # 0   |_|-1


def contract_dmps_right_border(dst, dmps):
    # mps_down
    #    2|
    # 0 -|_|-3
    #    1|
    trace_mp(dst, dmps, 1, 2)
    # dst
    # 0-|_|   1


def contract_left_very_small_bloc_dmps(dst, left_bloc, dmps):
    # dmps
    #    2|
    # 0 -|_|-3
    #    1|
    tmp = {}
    multiply_mp(tmp, left_bloc, dmps, [1], [0])
    trace_mp(dst, tmp, 1, 2)
    # dst
    # 0   |_|-1


def contract_right_very_small_bloc_dmps(dst, right_bloc, dmps):
    # dmps
    #    2|
    # 0 -|_|-3
    #    1|
    tmp = {}
    multiply_mp(tmp, dmps, right_bloc, [3], [0])
    trace_mp(dst, tmp, 1, 2)
    # dst
    #  0-|_|    1


def contract_left_right_very_small_bloc(dst, left_blocs, right_blocs):
    # left
    # 0   |_|-1
    # right
    #  0-|_|    1
    multiply_mp(dst, left_blocs, right_blocs, [0, 1], [1, 0])


def contract_dmps_dmps_left_border(dst, mps_down, mps_up):
    # mps_down
    #    2|
    # 0 -|_|-3
    #    1|
    multiply_mp(dst, mps_down, mps_up, [0, 1, 2], [0, 2, 1])
    # dst
    #    | |-1
    #    |_|-0


def contract_dmps_dmps_right_border(dst, mps_down, mps_up):
    # mps_down
    #    2|
    # 0 -|_|-3
    #    1|
    multiply_mp(dst, mps_down, mps_up, [1, 2, 3], [2, 1, 3])
    # dst
    #  1-| |
    #  0-|_|


def contract_left_small_bloc_dmps(dst, left_bloc, mps_down, mps_up):
    tmp = {}
    # mps_down
    #    2|
    # 0 -|_|-3
    #    1|
    multiply_mp(tmp, left_bloc, mps_down, [0], [0])
    multiply_mp(dst, tmp, mps_up, [0, 1, 2], [0, 2, 1])
    # dst
    #    | |-1
    #    |_|-0


def contract_right_small_bloc_dmps(dst, right_bloc, mps_down, mps_up):
    tmp = {}
    # mps_down
    #    2|
    # 0 -|_|-3
    #    1|
    multiply_mp(tmp, mps_up, right_bloc, [3], [1])
    multiply_mp(dst, mps_down, tmp, [1, 2, 3], [2, 1, 3])
    # dst
    #  1-| |
    #  0-|_|


def contract_left_right_small_bloc(dst, left_blocs, right_blocs):
    multiply_mp(dst, left_blocs, right_blocs, [0, 1], [0, 1])


def contract_mps_mps_left_border(dst, mps_down, mps_up):
    # mps_down
    #    1|
    # 0 -|_|-2
    multiply_mp(dst, mps_down, mps_up, [0, 1], [0, 1])
    # dst
    #    | |-1
    #    |_|-0


def contract_mps_mps_right_border(dst, mps_down, mps_up):
    # mps_down
    #    1|
    # 0 -|_|-2
    multiply_mp(dst, mps_down, mps_up, [1, 2], [1, 2])
    # dst
    #  1-| |
    #  0-|_|


def contract_left_small_bloc_mps(dst, left_bloc, mps_down, mps_up):
    tmp = {}
    # mps_down
    #    1|
    # 0 -|_|-2
    multiply_mp(tmp, left_bloc, mps_down, [0], [0])
    multiply_mp(dst, tmp, mps_up, [0, 1], [0, 1])
    # dst
    #    | |-1
    #    |_|-0


def contract_right_small_bloc_mps(dst, right_bloc, mps_down, mps_up):
    tmp = {}
    # mps_down
    #    1|
    # 0 -|_|-2
    multiply_mp(tmp, right_bloc, mps_down, [0], [2])
    multiply_mp(dst, tmp, mps_up, [0, 2], [2, 1])
    # dst
    #  1-| |
    #  0-|_|


def contract_dmps_mpo_dmps_left_border(dst, mps_down, mpo, mps_up):
    mpo_left = {}
    fuse_mp(mpo_left, mpo, 0)
    tmp = {}
    # mps_down
    #    2|
    # 0 -|_|-3
    #    1|
    multiply_mp(tmp, mps_down, mpo_left, [2], [0])
    # tmp
    #    3|
    #    | |-4
    #    | |
    # 0 -|_|-2
    #    1|
    multiply_mp(dst, tmp, mps_up, [0, 1, 3], [0, 2, 1])
    # dst
    #    | |-2
    #    | |-1
    #    |_|-0


def contract_dmps_mpo_dmps_right_border(dst, mps_down, mpo, mps_up):
    mpo_left = {}
    fuse_mp(mpo_left, mpo, 2)
    tmp = {}
    # mps_down
    #    2|
    # 0 -|_|-3
    #    1|
    multiply_mp(tmp, mps_down, mpo_left, [2], [1])
    # tmp
    #    4|
    # 3 -| |
    #    | |
    # 0 -|_|-2
    #    1|
    # tmp_left_bloc = {}
    multiply_mp(dst, tmp, mps_up, [1, 2, 4], [2, 3, 1])
    # dst
    # 2 -| |
    # 1 -| |
    # 0 -|_|


def contract_left_bloc_dmps(dst, left_bloc, mps_down, mpo, mps_up):
    tmp = {}
    # mps_down
    #    2|
    # 0 -|_|-3
    #    1|
    multiply_mp(tmp, left_bloc, mps_down, [0], [0])
    # tmp
    # 1 -| |
    # 0 -| ||3
    #    |___|-4
    #      2|
    tmp_tmp = {}
    multiply_mp(tmp_tmp, tmp, mpo, [0, 3], [0, 1])
    # tmp
    # 0 -| ||3
    #    |   |-4
    #    |___|-2
    #      1|
    multiply_mp(dst, tmp_tmp, mps_up, [0, 1, 3], [0, 2, 1])
    # dst
    #    | |- 2
    #    | |- 1
    #    |_|- 0


def contract_right_bloc_dmps(dst, right_bloc, mps_down, mpo, mps_up):
    tmp = {}
    # mps_down
    #    2|
    # 0 -|_|-3
    #    1|
    multiply_mp(tmp, right_bloc, mps_down, [0], [3])
    # tmp
    #      | |-1
    #    4|| |-0
    #  2-|___|
    #     3|
    tmp_tmp = {}
    multiply_mp(tmp_tmp, tmp, mpo, [0, 4], [3, 1])
    # tmp
    #     4| |-0
    #  3-|   |
    #  1-|___|
    #     2|
    multiply_mp(dst, tmp_tmp, mps_up, [0, 2, 4], [3, 2, 1])
    # dst
    # 2 -| |
    # 1 -| |
    # 0 -|_|


def contract_left_right_bloc(dst, left_blocs, right_blocs):
    multiply_mp(dst, left_blocs, right_blocs, [0, 1, 2], [0, 1, 2])


def contract_left_right_bloc_with_mpo(dst, left_blocs, mpo, right_blocs):
    tmp = {}
    # mpo
    #    2|
    # 0 -|_|-3
    #    1|
    multiply_mp(tmp, left_blocs, mpo, [1], [0])
    # tmp
    #  1-| ||3
    #    |   |-4
    #  0-|_||2
    tmp_tmp = {}
    multiply_mp(tmp_tmp, tmp, right_blocs, [4], [1])
    # tmp_tmp
    #  1-| |_ |3_| |-5
    #    |  _   _  |
    #  0-|_|  |2 | |-4
    permute_blocs(dst, tmp_tmp, [(0, 1, 2, 3, 4, 5), (0, 2, 4, 1, 3, 5)])
    # dst
    #  3-| |_ |4_| |-5
    #    |  _   _  |
    #  0-|_|  |1 | |-2


def contract_mps_mpo_mps_left_border(dst, mps_down, mpo, mps_up):
    mpo_left = {}
    rm_border_mpo(mpo_left, mpo, is_left=True)
    tmp = {}
    # mps_down
    #    1|
    # 0 -|_|-2
    multiply_mp(tmp, mps_down, mpo_left, [1], [1])
    # tmp
    #     |2
    #    | |-3
    # 0 -|_|-1

    multiply_mp(dst, tmp, mps_down, [0, 2], [0, 1])
    # dst
    #    | |-2
    #    | |-1
    #    |_|-0


def contract_mps_mpo_mps_right_border(dst, mps_down, mpo, mps_up):
    mpo_right = {}
    rm_border_mpo(mpo_right, mpo, is_left=False)
    tmp = {}
    # mps_down
    #    1|
    # 0 -|_|-2
    multiply_mp(tmp, mps_down, mpo_right, [1], [1])
    # tmp
    #    3|
    # 2 -| |
    # 0 -| |-1
    # tmp_left_bloc = {}
    multiply_mp(dst, tmp, mps_up, [1, 3], [2, 1])
    # dst
    # 2 -| |
    # 1 -| |
    # 0 -|_|


def contract_left_bloc_mps(dst, left_bloc, mps_down, mpo, mps_up):
    tmp = {}
    # mps_down
    #    1|
    # 0 -|_|-2
    multiply_mp(tmp, left_bloc, mps_down, [0], [0])
    # tmp
    # 1 -| |
    # 0 -| ||2
    #    |___|-3
    tmp_tmp = {}
    multiply_mp(tmp_tmp, tmp, mpo, [0, 2], [0, 1])
    # tmp_tmp
    # 0 -| ||2
    #    |   |-3
    #    |___|-1
    multiply_mp(dst, tmp_tmp, mps_up, [0, 2], [0, 1])
    # dst
    #    | |- 2
    #    | |- 1
    #    |_|- 0


def contract_right_bloc_mps(dst, right_bloc, mps_down, mpo, mps_up):
    tmp = {}
    # mps_down
    #    1|
    # 0 -|_|-2
    multiply_mp(tmp, right_bloc, mps_down, [0], [2])
    # tmp
    #      | |-1
    #    3|| |-0
    #  2-|___|
    tmp_tmp = {}
    multiply_mp(tmp_tmp, tmp, mpo, [0, 3], [3, 1])
    # tmp_tmp
    #     3| |-0
    #  2-|   |
    #  1-|___|
    multiply_mp(dst, tmp_tmp, mps_up, [0, 3], [2, 1])
    # dst
    # 2 -| |
    # 1 -| |
    # 0 -|_|


def contract_dmps_mpo_mpo_dmps_left_border(dst, mps_down, mpo_one_left,mpo_two_left, mps_up):
    mpo_left = {}
    tmp = {}
    # mps_down
    #    2|
    # 0 -|_|-3
    #    1|
    multiply_mp(tmp, mps_down, mpo_one_left, [2], [1])
    # tmp
    #    4|
    # 3 -| |-5
    # 0 -|_|-2
    #    1|
    tmp_tmp = {}
    multiply_mp(tmp_tmp, tmp, mpo_two_left, [3,4], [0,1])
    # tmp_tmp
    #    4|
    #    | |-5
    #    | |-3
    # 0 -|_|-2
    #    1|
    multiply_mp(dst, tmp, mps_up, [0,1,4], [0, 2, 1])
    # dst
    #    | |-3
    #    | |-2
    #    | |-1
    #    |_|-0


def contract_dmps_mpo_mpo_dmps_right_border(dst, mps_down, mpo_one_right, mpo_two_right, mps_up):
    mpo_left = {}
    tmp = {}
    # mps_down
    #    2|
    # 0 -|_|-3
    #    1|
    multiply_mp(tmp, mps_down, mpo_one_right, [2], [1])
    # tmp
    #    4|
    # 3 -| |-5
    # 0 -|_|-2
    #    1|
    tmp_tmp = {}
    multiply_mp(tmp, tmp, mpo_two_right, [4,5], [1,3])
    # tmp
    #    5|
    # 4 -| |
    # 3 -| |
    # 0 -|_|-2
    #    1|
    multiply_mp(dst, tmp, mps_up, [1, 2, 5], [2, 3, 1])
    # dst
    # 3 -| |
    # 2 -| |
    # 1 -| |
    # 0 -|_|


def contract_left_very_big_bloc_dmps(dst, left_bloc, dmps_down, mpo_one, mpo_two, dmps_up):
    tmp = {}
    # dmps_down
    #    2|
    # 0 -|_|-3
    #    1|
    multiply_mp(tmp, left_bloc, dmps_down, [0], [0])
    # tmp
    # 2 -| |
    # 1 -| |
    # 0 -| ||4
    #    |___|-5
    #      3|
    tmp_tmp = {}
    multiply_mp(tmp_tmp, tmp, mpo_one, [0, 4], [0, 1])
    tmp.clear()
    # tmp_tmp
    # 1 -| |
    # 0 -| ||4
    #    |   |-5
    #    |___|-3
    #      2|
    tmp_tmp_tmp = {}
    multiply_mp(tmp_tmp_tmp, tmp_tmp, mpo_two, [0, 4], [0, 1])
    tmp_tmp.clear()
    # tmp_tmp_tmp
    # 0 -| ||4
    #    |   |-5 
    #    |   |-3
    #    |___|-2
    #      1|
    multiply_mp(dst, tmp_tmp_tmp, dmps_up, [0, 1, 4], [0, 2, 1])
    # dst
    #    | |- 3
    #    | |- 2
    #    | |- 1
    #    |_|- 0


def contract_right_very_big_bloc_dmps(dst, right_bloc, dmps_down, mpo_one,mpo_two, dmps_up):
    tmp = {}
    # mps_down
    #    2|
    # 0 -|_|-3
    #    1|
    multiply_mp(tmp, right_bloc, dmps_down, [0], [3])
    # tmp
    #      | |-2
    #      | |-1
    #    5|| |-0
    #  3-|___|
    #     4|
    tmp_tmp = {}
    multiply_mp(tmp_tmp, tmp, mpo_one, [0, 5], [3, 1])
    # tmp_tmp
    #      | |-1
    #    5|| |-0
    #  4-|   |
    #  2-|___|
    #     3|
    tmp_tmp_tmp = {}
    multiply_mp(tmp_tmp_tmp, tmp_tmp, mpo_two, [0, 5], [3, 1])
    # tmp_tmp_tmp
    #    5|| |-0
    #  4-|   |
    #  3-|   |
    #  1-|___|
    #     2|
    multiply_mp(dst, tmp_tmp_tmp, dmps_up, [0, 2, 5], [3, 2, 1])
    # dst
    # 3 -| |
    # 2 -| |
    # 1 -| |
    # 0 -|_|



def contract_left_right_very_big_bloc(dst, left_bloc,right_bloc):
    multiply_mp(dst, left_bloc, right_bloc, [0,1,2,3], [0,1,2,3])