from matplotlib.pyplot import legend
import numpy as np
import matplotlib.pyplot as plt

add_header = True

N_arr = []
sec_arr = []
mem_arr = []

with open("/tmp/pyfhmdot_benchmark_mul_dgemm.txt", "r") as f:
    if add_header:
        print(f.readline())

    for line in f.readlines():
        N, sec, mem = line.split(",")
        N_arr.append(N)
        sec_arr.append(sec)
        mem_arr.append(mem)

    plt.figure(1)
    plt.subplot(1, 2, 1)
    plt.plot(N_arr, sec_arr, "b.", label="time [s]")
    plt.grid()
    plt.ylabel("time [s]")
    plt.legend("north east")
    plt.subplot(1, 2, 2)
    plt.plot(N_arr, mem_arr, "r.", label="memory [KiB]")
    plt.grid()
    plt.ylabel("memory [KiB]")
    plt.legend("north east")
    plt.show()
    pass
