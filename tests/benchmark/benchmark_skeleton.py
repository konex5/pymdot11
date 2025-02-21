import csv

add_header = True

datalist = [(0, 10), (1, 20), (2, 30)]


with open("/tmp/pyfhmdot_benchmark_skeleton.txt", "w") as f:
    if add_header:
        f.write("time,memory\n")

    for time, memory in datalist:
        f.write(f"{time},{memory}\n")
