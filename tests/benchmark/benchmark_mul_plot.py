from matplotlib.pyplot import legend
import numpy as np
import matplotlib.pyplot as plt

add_header = True

N_arr = []
time_arr = []
mem_arr = []

with open("/tmp/pymdot_benchmark_mul.txt", "r") as f:
    if add_header:
        print(f.readline())

    for line in f.readlines():
        N, sec, mem = line.split(",")
        N_arr.append(int(N))
        time_arr.append(float(sec))
        mem_arr.append(float(mem))

    plt.figure(1)
    plt.subplot(1, 2, 1)
    plt.plot(N_arr, time_arr, "bx", label="time [s]")
    plt.grid()
    plt.ylabel("time [s]")
    plt.subplot(1, 2, 2)
    plt.plot(N_arr, mem_arr, "rx", label="memory [KiB]")
    plt.grid()
    plt.ylabel("memory [KiB]")
    plt.show()
    pass
