from aoclib import read_input


def get_input(is_example=False):
    """
    :param bool is_example:
    :return list[int]:
    """
    return [int(x) for x in read_input(is_example)]


def is_valid(n, preceding):
    """
    :param int n:
    :param list[int] preceding:
    :return bool:
    """
    s = len(preceding)
    for ix in range(1, s):
        for jy in range(0, ix):
            if n == preceding[ix] + preceding[jy]:
                return True
    return False


def solve_9_1(data, pre=25) -> int:
    """
    :param list[int] data:
    :param int pre:
    :return int:
    """
    for ix in range(pre, len(data)):
        x = data[ix]
        if not is_valid(x, data[ix - pre:ix]):
            return x

    return 0


def solve_9_2(data, pre=25) -> int:
    """
    :param list[int] data:
    :param int pre:
    :return int:
    """
    invalid = solve_9_1(data, pre)
    jy = 0
    total = 0

    for ix in range(len(data)):
        x = data[ix]
        if x == invalid:
            return 0

        jy = jy or ix

        while total < invalid:
            total += data[jy]
            jy += 1

        if total == invalid:
            return min(data[ix:jy]) + max(data[ix:jy])

        total -= x
    return 0


def solve_9():
    return (
        solve_9_1(get_input(True), 5) == 127 and solve_9_1(get_input()) or 0,
        solve_9_2(get_input(True), 5) == 62 and solve_9_2(get_input()) or 0,
    )


if __name__ == '__main__':
    try:
        print(solve_9())
    except Exception as e:
        print('ERROR', e)
        exit(1)
