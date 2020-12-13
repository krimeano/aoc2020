from aoclib import read_input


def solve_13():
    example_data = StopData(read_input(True))
    data = StopData(read_input())
    return (
        solve_13_1(example_data) == 295 and solve_13_1(data),
        solve_13_2(example_data.buses) == 1068781 and solve_13_2(data.buses)
    )


class StopData:
    def __init__(self, input_data):
        """
        :param list[str] input_data:
        """
        self.t = int(input_data[0])
        self.buses = [x != 'x' and int(x) or 0 for x in input_data[1].split(',')]

    def __str__(self):
        return '%d / %s' % (self.t, ','.join([str(x) for x in self.buses if x]))


def solve_13_1(data: StopData) -> int:
    best_time = data.t
    best_bus = 0

    for bus in data.buses:
        if not bus:
            continue
        last_bus = data.t % bus
        wait = last_bus and (bus - last_bus)
        if wait < best_time:
            best_time = wait
            best_bus = bus
    print('best bus', best_bus, 'wait', best_time)
    return best_bus * best_time


def solve_13_2(buses) -> int:
    """
    :param list[int] buses:
    :return int:
    """
    return 0


if __name__ == '__main__':
    try:
        print(solve_13())
    except Exception as e:
        print(e)
        exit(1)
