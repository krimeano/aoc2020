def read_input(is_example=False):
    input_path = is_example and 'example.txt' or 'input.txt'
    return read_input_separated_by_lines(input_path)


def read_input_separated_by_lines(f_name: str):
    data = []
    with open(f_name) as f:
        chunk = ''
        for x in f.readlines():
            if x.strip():
                chunk += x
            else:
                data.append(chunk)
                chunk = ''
    if chunk:
        data.append(chunk)
    return data


def solve_6_1(data) -> int:
    return sum([len(set([x for x in group if x != '\n'])) for group in data])


def solve_6_2(data) -> int:
    out = 0
    for group in data:
        users = [set([x for x in user]) for user in group.strip().split('\n')]
        group_selected = users.pop()
        while users:
            group_selected = group_selected.intersection(users.pop())
        out += len(group_selected)
    return out


def solve6():
    return (
        solve_6_1(read_input(True)) == 11 and solve_6_1(read_input()),
        solve_6_2(read_input(True)) == 6 and solve_6_2(read_input())
    )


if __name__ == '__main__':
    try:
        print(solve6())
    except Exception as e:
        print('ERROR', e)
        exit(1)
