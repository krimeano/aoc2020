from aoclib import read_input

DIRECTIONS = {'e': [0, 1], 'se': [1, 1], 'sw': [1, 0], 'w': [0, -1], 'nw': [-1, -1], 'ne': [-1, 0]}


def part_1(lines):
    return len(process_lines(lines))


def process_lines(lines):
    tiles = {}
    for line in lines:

        xy = line_to_vector(line)

        if xy not in tiles:
            tiles[xy] = False

        tiles[xy] = not tiles[xy]
    return [x for x in tiles if tiles[x]]


def line_to_vector(line):
    x, y = 0, 0
    direction = ''
    for char in line:
        direction += char
        if char in 'sn':
            continue
        x += DIRECTIONS[direction][0]
        y += DIRECTIONS[direction][1]
        direction = ''
    return x, y


def solve_24():
    return (
        part_1(read_input(True)) == 10 and part_1(read_input()),
        0
    )


if __name__ == '__main__':
    print(solve_24())
