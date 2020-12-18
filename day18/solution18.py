from aoclib import read_input

EXPECTED = [71, 51, 26, 437, 12240, 13632]
EXPECTED_2 = [231, 51, 46, 1445, 669060, 23340]
SPACE = ' '
NUMS = '1234567890'
OPS = '+*'
PAR_OPEN = '('
PAR_CLOSE = ')'
PARS = PAR_OPEN + PAR_CLOSE
VOC = NUMS + OPS + PARS + SPACE


def apply_operator(a, op, b):
    if op == '+':
        return a + b
    if op == '*':
        return a * b


def evaluate_expression(line: str, level=0):
    # print('  > ' * level, line)
    a = 0
    op = '+'
    pp = 0
    ix = 0
    s = len(line)
    while ix < s:
        x = line[ix]
        ix += 1

        if x == SPACE:
            continue

        if x in OPS:
            op = x
            continue

        if x in NUMS:
            a = apply_operator(a, op, int(x))
            continue

        if x == PAR_OPEN:
            pp += 1
            jy = ix

            while jy < s:
                y = line[jy]
                jy += 1
                pp += y == PAR_OPEN
                pp -= y == PAR_CLOSE
                if not pp:
                    sub = line[ix:jy - 1]
                    a = apply_operator(a, op, evaluate_expression(sub, level + 1))
                    ix = jy
                    break
            continue

        print('unhandled symbol', x)
    return a


def evaluate_advanced(line: str):
    while PAR_OPEN in line:
        line = resolve_par(line)
    parts = line.split('*')
    out = 1
    for x in parts:
        out *= sum(int(y.strip()) for y in x.split('+'))
    return out


def resolve_par(line):
    s = len(line)
    ix = line.index(PAR_OPEN)
    if ix < 0:
        return line
    jy = ix + 1
    pp = 1
    prefix = ix > 0 and line[0:ix] or ''
    # print('line = ', line)
    while jy < s:
        y = line[jy]
        jy += 1
        pp += y == PAR_OPEN
        pp -= y == PAR_CLOSE
        if not pp:
            sub = line[ix + 1:jy - 1]
            suffix = line[jy:]
            # print('prefix=', prefix)
            # print('sub=', sub)
            # print('suffix=', suffix)
            val = evaluate_advanced(sub)
            return prefix + str(val) + suffix
    print('wff closed not found', ix, line)
    return '0'


def solve_18_1(lines: str):
    out = [evaluate_expression(line) for line in lines]
    return out


def solve_18_2(lines: str):
    out = [evaluate_advanced(line) for line in lines]
    return out


def solve_18():
    return (
        solve_18_1(read_input(True)) == EXPECTED and sum(solve_18_1(read_input())),
        solve_18_2(read_input(True)) == EXPECTED_2 and sum(solve_18_2(read_input())),
    )


if __name__ == '__main__':
    print(solve_18())
