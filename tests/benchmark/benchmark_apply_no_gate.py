import tracemalloc
import time
import numpy as np

from pyfhmdot.algorithm import apply_mm

add_header = True

datalist = [2 ** _ for _ in range(2, 11)]  # N


def create_random_matrix(chi, d):
    return np.random.random(chi * d * chi).reshape(chi, d, chi)


def create_random_blocs(chi, max_index=3):
    blocs = {}  # sh
    for i in range(max_index):
        for j in range(max_index):
            blocs[(i, 0, j)] = create_random_matrix(chi, d=1)
            blocs[(i, 1, j)] = create_random_matrix(chi, d=2)
            blocs[(i, 2, j)] = create_random_matrix(chi, d=1)
    return blocs


with open("/tmp/pyfhmdot_benchmark_apply_no_gate.txt", "w") as f:
    if add_header:
        f.write("N,time[ms],memory[KiB]\n")
    for N in datalist:
        mp = [create_random_blocs(N), create_random_blocs(N)]
        dst = {}
        #
        tracemalloc.start()
        time_start = time.time()
        #
        mp[0], mp[1] = apply_mm(
            mp[0],
            mp[1],
            {"dw_one_serie": 0},
            N,
            True,
            10 ** -62,
            is_um=None,
            conserve_left_right_before=False,
            direction_right=-1,
        )
        #
        time_end = time.time()
        print("elapsed time {} sec", time_end - time_start)
        memory_snapshot = tracemalloc.take_snapshot()
        top_stats = memory_snapshot.statistics("lineno")
        size = sum(stat.size for stat in top_stats[3:])
        print("%s other: %.1f KiB" % (len(top_stats[3:]), size / 1024))
        total = sum(stat.size for stat in top_stats)
        print("Total allocated size: %.1f KiB" % (total / 1024))
        elapsed_time = time_end * 10 ** -4  # ms
        memory = total
        f.write(f"{N},{elapsed_time},{memory}\n")
        #
        dst.clear()
