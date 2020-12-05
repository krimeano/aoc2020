def ticket_to_id(ticket):
    out = 0
    ones = ('B', 'R')
    for x in ticket:
        out = out << 1
        out += x in ones
    return out


def solve_5_1(tickets) -> int:
    ids = [ticket_to_id(x) for x in tickets]
    return max(ids)


def solve_5_2(tickets) -> int:
    ids_map = {ticket_to_id(x): x for x in tickets}
    print(ids_map)
    for ix in ids_map:
        if (ix - 2) in ids_map and (ix - 1) not in ids_map:
            return ix - 1
        if (ix + 2) in ids_map and (ix + 1) not in ids_map:
            return ix + 1
    return 0


def solve_5():
    example_tickets = ['BFFFBBFRRR', 'FFFBBBFRRR', 'BBFFBBFRLL']
    input_data = []
    with open('input.txt') as f:
        input_data = [x.strip() for x in f.readlines()]
    return (solve_5_1(example_tickets) == 820) and solve_5_1(input_data), solve_5_2(input_data)


if __name__ == '__main__':
    print(solve_5())
