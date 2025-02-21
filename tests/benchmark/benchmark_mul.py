from numpy import tensordot
import tracemalloc
import time
import numpy as np
import csv

add_header = True

datalist = [(10 * _ ** 2, 10 * _ ** 2) for _ in range(10)]  # N,K


def create_random_matrix(N, M):
    return np.random.random(N * M).reshape(N, M)


with open("/tmp/pyfhmdot_benchmark_mul_dgemm.txt", "w") as f:
    if add_header:
        f.write("N,time[ms],memory[KiB]\n")

    for N, K in datalist:
        arr1 = create_random_matrix(N, K)
        arr2 = create_random_matrix(N, K)

        tracemalloc.start()
        time_start = time.time()
        res = np.dot(arr1, arr2)  # np.tensordot(arr1,arr2,axes=[1,0])
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
