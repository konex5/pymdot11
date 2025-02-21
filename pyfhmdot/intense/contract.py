from pyfhmdot.intense.mul_mp import multiply_mp, fuse_mp, permute_blocs


def contract_dmps_mpo_dmps_left_border(dst,mps_down,mpo,mps_up):
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
    #    | |-1
    #    |_|-0

 
def contract_dmps_mpo_dmps_right_border(dst,mps_down,mpo,mps_up):
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
    # 1 -| |
    # 0 -|_|

 
def contract_left_bloc_dmps(dst,left_bloc, mps_down,mpo,mps_up):
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
    #    | |- 1
    #    |_|- 0


def contract_right_bloc_dmps(dst,right_bloc, mps_down,mpo,mps_up):
    tmp = {}
    # mps_down
    #    2|
    # 0 -|_|-3
    #    1|
    multiply_mp(tmp,right_bloc,mps_down,[0],[3])
    # tmp
    #      | |-1
    #    4|| |-0
    #  2-|___|
    #     3|
    tmp_tmp = {}
    multiply_mp(tmp_tmp,tmp,mpo,[0,4],[3,1])
    # tmp
    #     4| |-0
    #  3-|   |
    #  1-|___|
    #     2|
    multiply_mp(dst,tmp_tmp,mps_up,[0,2,4],[3,2,1])
    # dst
    # 2 -| |
    # 1 -| |
    # 0 -|_|


def contract_left_right_bloc(dst,left_blocs,right_blocs):
    multiply_mp(dst,left_blocs,right_blocs,[0,1,2],[0,1,2])
    

def contract_left_right_bloc_with_mpo(dst,left_blocs,mpo,right_blocs):
    tmp = {}
    # mpo
    #    2|
    # 0 -|_|-3
    #    1|
    multiply_mp(tmp,left_blocs,mpo,[1],[0])
    # tmp
    #  1-| ||3    
    #    |   |-4
    #  0-|_||2
    tmp_tmp = {}
    multiply_mp(tmp_tmp,tmp,right_blocs,[4],[1])
    # tmp_tmp
    #  1-| |_ |3_| |-5  
    #    |  _   _  |
    #  0-|_|  |2 | |-4
    permute_blocs(dst,tmp_tmp,[(0,1,2,3,4,5),(0,2,4,1,3,5)])
    # dst
    #  3-| |_ |4_| |-5  
    #    |  _   _  |
    #  0-|_|  |1 | |-2




def contract_mps_mpo_mps_left_border(dst,mps_down,mpo,mps_up):
    mpo_left = {}
    fuse_mp(mpo_left, mpo,0)
    tmp = {}
    # mps_down
    #    1|
    # 0 -|_|-2
    multiply_mp(tmp,mps_down,mpo_left,[1],[0])
    # tmp
    #    2|
    #    | |-3
    # 0 -|_|-1
    multiply_mp(dst,tmp,mps_up,[0,2],[0,1])
    # dst
    #    | |-2
    #    | |-1
    #    |_|-0

# TODO
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
    # 1 -| |
    # 0 -|_|

 
def contract_left_bloc_mps(dst,left_bloc, mps_down,mpo,mps_up):
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
    #    | |- 1
    #    |_|- 0


def contract_right_bloc_mps(dst,right_bloc, mps_down,mpo,mps_up):
    tmp = {}
    # mps_down
    #    2|
    # 0 -|_|-3
    #    1|
    multiply_mp(tmp,right_bloc,mps_down,[0],[3])
    # tmp
    #      | |-1
    #    4|| |-0
    #  2-|___|
    #     3|
    tmp_tmp = {}
    multiply_mp(tmp_tmp,tmp,mpo,[0,4],[3,1])
    # tmp
    #     4| |-0
    #  3-|   |
    #  1-|___|
    #     2|
    multiply_mp(dst,tmp_tmp,mps_up,[0,2,4],[3,2,1])
    # dst
    # 2 -| |
    # 1 -| |
    # 0 -|_|