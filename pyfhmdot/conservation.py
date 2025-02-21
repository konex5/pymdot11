def conserve_qnum_list(*, size, qnum_conserved, d):
    """
    0 = qnum_min < qnum_conserved < qnum_max
    """
    inc = d - 1

    minimal_qnum = [0]
    maximal_qnum = [qnum_conserved]

    count_min = 0
    for i in range(size):
        if qnum_conserved > count_min:
            count_min += inc
        minimal_qnum.append(count_min)

    count_max = qnum_conserved
    for i in range(size):
        if 0 < count_max:
            count_max -= inc
        maximal_qnum.append(count_max)

    output = []
    for i in range(len(minimal_qnum)):
        output.append(range(maximal_qnum[::-1][i], minimal_qnum[i] + 1))

    return output


def conserve_qnum(position, *, size, qnum_conserved, d):
    qcons_list = conserve_qnum_list(size=size, qnum_conserved=qnum_conserved, d=d)

    return qcons_list[position]
