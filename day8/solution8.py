def read_input(is_example=False, suffix=''):
    input_path = (is_example and 'example' or 'input') + suffix + '.txt'
    with open(input_path) as f:
        return tuple([(y[0], int(y[1]),) for y in [x.split(' ') for x in f.readlines() if x.strip()]])


def execute(instructions):
    executed_lines = dict()
    value = 0
    ix = 0
    s = len(instructions)

    while ix < s and ix not in executed_lines:
        executed_lines[ix] = True
        cmd, n = instructions[ix]
        if cmd == 'nop':
            ix += 1
        elif cmd == 'acc':
            value += n
            ix += 1
        elif cmd == 'jmp':
            ix += n

    return ix == s, value


def solve_8_1(instructions) -> int:
    return execute(instructions)[1]


def solve_8_2(instructions) -> int:
    copy = [[x[0], x[1]] for x in instructions]
    s = len(instructions)

    for ix in range(s):
        x = copy[ix]
        if x[0][2] != 'p':
            continue
        x[0] = (x[0] == 'nop') and 'jmp' or 'nop'
        r, n = execute(copy)
        if r:
            return n

        x[0] = (x[0] == 'nop') and 'jmp' or 'nop'

    return 0


def solve_8():
    return (
        solve_8_1(read_input(True)) == 5 and solve_8_1(read_input()),
        solve_8_2(read_input(True)) == 8 and solve_8_2(read_input())
    )


if __name__ == '__main__':
    try:
        print(solve_8())
    except Exception as e:
        print('ERROR', e)
        exit(1)
