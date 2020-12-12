from aoclib import read_input

DIRECTION_VECTORS = {
    'E': {'x': 1, 'y': 0},
    'N': {'x': 0, 'y': 1},
    'W': {'x': -1, 'y': 0},
    'S': {'x': 0, 'y': -1},
}

DIRECTIONS = [x for x in DIRECTION_VECTORS]

DIRECTION_INDEXES = {DIRECTIONS[i]: i for i in range(len(DIRECTIONS))}

ROTATE = {'L': 90, 'R': -90}


def solve_12():
    return (
        solve_12_1(read_input(True)) == 25 and solve_12_1(read_input()),
        solve_12_2(read_input(True)) == 286 and solve_12_2(read_input()),
    )


def solve_12_1(instructions) -> 0:
    ferry = Ferry()
    for x in instructions:
        ferry.process_instruction(x)
    return abs(ferry.x) + abs(ferry.y)


def solve_12_2(instructions) -> 0:
    ferry = FerryWithWaypoint()
    for x in instructions:
        ferry.process_instruction(x)
    return abs(ferry.x) + abs(ferry.y)


class Ferry:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = DIRECTIONS[0]

    def process_instruction(self, to):
        direction = to[0]
        value = int(to[1:])
        if direction in ROTATE:
            self.rotate(direction, value)
        elif direction == 'F':
            self.move_forward(value)
        else:
            self.move_to(direction, value)

    def rotate(self, direction, degrees):
        ix = (degrees // ROTATE[direction] + DIRECTION_INDEXES[self.direction]) % 4
        self.direction = DIRECTIONS[ix]

    def move_forward(self, value):
        self.move_to(self.direction, value)

    def move_to(self, direction, value):
        self.x += DIRECTION_VECTORS[direction]['x'] * value
        self.y += DIRECTION_VECTORS[direction]['y'] * value


class FerryWithWaypoint(Ferry):
    def __init__(self, wx=10, wy=1):
        super().__init__()
        self.wx = wx
        self.wy = wy

    def rotate(self, direction, degrees):
        times = (degrees // ROTATE[direction]) % 4
        for i in range(times):
            self.wx, self.wy = -self.wy, self.wx

    def move_to(self, direction, value):
        self.wx += DIRECTION_VECTORS[direction]['x'] * value
        self.wy += DIRECTION_VECTORS[direction]['y'] * value

    def move_forward(self, value):
        self.x += self.wx * value
        self.y += self.wy * value


if __name__ == '__main__':
    try:
        print(solve_12())

    except Exception as exception:
        print(exception)
        exit(1)
