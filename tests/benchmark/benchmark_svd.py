from scipy.linalg import svd as _svd
import tracemalloc
import time
import numpy as np
import csv

add_header = True

datalist = [(10 * _**2, 10 * _**2) for _ in range(2, 10)]  # N,K


def create_random_matrix(N, M):
    return np.random.random(N * M).reshape(N, M)


with open("/tmp/pyfhmdot_benchmark_svd.txt", "w") as f:
    if add_header:
        f.write("N,time[ms],memory[KiB]\n")

    for N, _ in datalist:
        a = create_random_matrix(N, N)

        tracemalloc.start()
        time_start = time.time()
        u, s, vd = _svd(
            a,
            full_matrices=False,
            compute_uv=True,
            overwrite_a=True,
        )
        time_end = time.time()
        print("elapsed time {} sec", time_end - time_start)
        memory_snapshot = tracemalloc.take_snapshot()
        top_stats = memory_snapshot.statistics("lineno")
        size = sum(stat.size for stat in top_stats[3:])
        print("%s other: %.1f KiB" % (len(top_stats[3:]), size / 1024))
        total = sum(stat.size for stat in top_stats)
        print("Total allocated size: %.1f KiB" % (total / 1024))

        elapsed_time = time_end * 10**-4  # ms
        memory = total
        f.write(f"{N},{elapsed_time},{memory}\n")
