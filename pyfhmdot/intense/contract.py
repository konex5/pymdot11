from pyfhmdot.intense.mul_mp import multiply_mp, trace_mp, fuse_mp, permute_blocs


def contract_mps_mpo_mps_left(dst,mps_down,mpo,mps_up):
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
    #tmp_left_bloc = {}
    multiply_mp(dst,tmp,mps_up,[0,1,3],[0,2,1])
    # tmp_left_bloc
    # tmp
    #     _
    #  3-| |-4
    #    | |
    #    | |-2
    #    | |
    # 0 -|_|-1
    #    
    # trace_mp(dst,tmp_left_bloc,0,3)
    
