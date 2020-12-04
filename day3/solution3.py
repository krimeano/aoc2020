def read_input(is_example=False):
    input_path = is_example and 'example.txt' or 'input.txt'
    with open(input_path) as f:
        return tuple(x.strip() for x in f.readlines() if x.strip())


def solve_3_1(pattern, move_i=1, move_j=3) -> int:
    h = len(pattern)
    w = len(pattern[0])
    i, j = 0, 0
    r = 0
    while i < h:
        r += pattern[i][j] == '#'
        i += move_i
        j = (j + move_j) % w
    return r


def solve_3_2(pattern):
    slopes = ((1, 1), (1, 3), (1, 5), (1, 7), (2, 1))
    r = 1
    for s in slopes:
        r *= solve_3_1(pattern, s[0], s[1])
    return r


def solve_3():
    res1 = 0
    res2 = 0

    if solve_3_1(read_input(True)) == 7:
        res1 = solve_3_1(read_input())

    if solve_3_2(read_input(True)) == 336:
        res2 = solve_3_2(read_input())

    return res1, res2


if __name__ == '__main__':
    print(solve_3())
