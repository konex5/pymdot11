from pyfhmdot.intense.mul_mp import multiply_mp, fuse_mp


def contract_mps_mpo_mps_left_border(dst,mps_down,mpo,mps_up):
    mpo_left = {}
    fuse_mp(mpo_left, mpo,0)
    tmp = {}
    # mps_down
    #    2|
    # 0 -|_|-3
    #    1|
    multiply_mp(tmp,mps_down,mpo_left,[2],[0])
    # tmp
    #    3|
    #    | |-4
    #    | |
    # 0 -|_|-2
    #    1|
    multiply_mp(dst,tmp,mps_up,[0,1,3],[0,2,1])
    # dst
    #    | |-2
    #    | |
    #    | |-1
    #    | |
    #    |_|-0

 
def contract_mps_mpo_mps_right_border(dst,mps_down,mpo,mps_up):
    mpo_left = {}
    fuse_mp(mpo_left, mpo, 2)
    tmp = {}
    # mps_down
    #    2|
    # 0 -|_|-3
    #    1|
    multiply_mp(tmp,mps_down,mpo_left,[2],[1])
    # tmp
    #    4|
    # 3 -| |
    #    | |
    # 0 -|_|-2
    #    1|
    #tmp_left_bloc = {}
    multiply_mp(dst,tmp,mps_up,[1,2,4],[2,3,1])
    # dst
    # 2 -| |
    #    | |
    # 1 -| |
    #    | |
    # 0 -|_|

 
def contract_left_bloc(dst,left_bloc, mps_down,mpo,mps_up):
    tmp = {}
    # mps_down
    #    2|
    # 0 -|_|-3
    #    1|
    multiply_mp(tmp,left_bloc,mps_down,[0],[0])
    # tmp
    # 1 -| |
    # 0 -| ||3
    #    |___|-4
    #      2|
    tmp_tmp = {}
    multiply_mp(tmp_tmp,tmp,mpo,[0,3],[0,1])
    # tmp
    # 0 -| ||3
    #    |   |-4
    #    |___|-2
    #      1|
    multiply_mp(dst,tmp_tmp,mps_up,[0,1,3],[0,2,1])
    # dst
    #    | |- 2
    #    | |
    #    | |- 1
    #    | |
    #    |_|- 0

