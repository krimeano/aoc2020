from aoclib import read_input_int


def solve_10_1(data) -> int:
    xx = sorted(data)
    out = {1: 1, 3: 1}
    for ix in range(1, len(xx)):
        d = xx[ix] - xx[ix - 1]
        out[d] = out[d] + 1
    return out[3] * out[1]


def solve_10_2(data) -> int:
    xx = sorted(data)
    ww = {0: 1}
    for x in xx:
        ww[x] = 0
        for w in range(x - 3, x):
            if w in ww:
                ww[x] += ww[w]
    return ww[x]


def solve_10():
    return (
        solve_10_1(read_input_int(True)) == 35
        and solve_10_1(read_input_int(True, '1')) == 220
        and solve_10_1(read_input_int()),
        solve_10_2(read_input_int(True)) == 8
        and solve_10_2(read_input_int(True, '1')) == 19208
        and solve_10_2(read_input_int()),
    )


if __name__ == '__main__':
    try:
        print(solve_10())
    except Exception as e:
        print('ERROR', e)
        exit(1)
