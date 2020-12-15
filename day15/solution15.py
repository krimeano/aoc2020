EXAMPLE = [0, 3, 6]
PUZZLE_INPUT = [2, 15, 0, 9, 1, 20]
TURN_1 = 2020
TURN_2 = 30000000
EXAMPLE_RESULT_1 = 436
EXAMPLE_RESULT_2 = 175594


def solve_15():
    return (
        solve_15_1(EXAMPLE) == EXAMPLE_RESULT_1 and solve_15_1(PUZZLE_INPUT),
        solve_15_2(EXAMPLE) == EXAMPLE_RESULT_2 and solve_15_2(PUZZLE_INPUT)
    )


def solve_15_1(data, turn=TURN_1):
    spoken = dict()

    prev_n = -1
    prev_ix = -1
    n = -1
    for ix in range(turn):
        n = (prev_n in spoken) and (prev_ix - spoken[prev_n]) or 0
        if ix < len(data):
            n = data[ix]
        if not ix % 1000000:
            print('Step', ix + 1, 'say', n)
        spoken[prev_n] = prev_ix
        prev_n = n
        prev_ix = ix
    print(n)
    return n


def solve_15_2(data):
    return solve_15_1(data, TURN_2)


if __name__ == '__main__':
    print(solve_15())
