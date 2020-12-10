import os


def read_input(is_example=False, suffix=''):
    """
    :param bool is_example:
    :param str suffix:
    :return list[str]:
    """
    prefix = is_example and 'example' or 'input'
    input_path = prefix + suffix + '.txt'
    if not os.path.exists(input_path) and suffix:
        input_path = (is_example and 'example' or 'input') + '.txt'
    with open(input_path) as f:
        return [x.strip() for x in f.readlines() if x and x != '\n']


def read_input_int(is_example=False, suffix=''):
    return [int(x) for x in read_input(is_example, suffix)]


def solve_part(solve_fn, part=1, example_result=0) -> int:
    """
    :param function solve_fn:
    :param int part:
    :param int example_result:
    :return int:
    """
    return solve_fn(read_input(True, str(part))) == example_result and solve_fn(read_input()) or 0


def solve(solve_fn_1=None, result_1=0, solve_fn_2=None, result_2=0):
    """
    :param function solve_fn_1:
    :param int result_1:
    :param function solve_fn_2:
    :param int result_2:
    :return:
    """
    return (
        solve_fn_1 and solve_part(solve_fn_1, 1, result_1) or 0,
        solve_fn_2 and solve_part(solve_fn_2, 2, result_2) or 0
    )
