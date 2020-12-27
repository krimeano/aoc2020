from aoclib import read_input

DIRECTIONS = {'e': [0, 1], 'se': [1, 1], 'sw': [1, 0], 'w': [0, -1], 'nw': [-1, -1], 'ne': [-1, 0]}


def part_1(lines: str) -> int:
    return len(process_lines(lines))


def process_lines(lines: str):
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


def part_2(lines: str):
    tiles = process_lines(lines)
    day = 0

    print('START:')
    print(str_tiles(tiles))
    while day < 100:
        day += 1
        tiles = next_day(tiles)
        print('\nDay {day}'.format(day=day))
        print((day <= 10 or day == 100) and str_tiles(tiles) or len(tiles))
    return len(tiles)


def str_tiles(black_tiles):
    xx = sorted(set([x[0] for x in black_tiles]))
    yy = sorted(set([y[1] for y in black_tiles]))
    x0, x1 = min(xx[0], 0), xx[-1]
    y0, y1 = min(yy[0], 0), yy[-1]
    out = ['x0, y0 = {x}, {y}, total = {total}'.format(x=x0, y=y0, total=len(black_tiles))]
    for x in range(x0, x1 + 1):
        line = ' ' * (x1 - x)
        for y in range(y0, y1 + 1):
            item = (x, y) in black_tiles and 'X' or 'O'
            if not x and not y:
                item = '\033[31m{item}\033[0m'.format(item=item)
            elif not x or not y:
                item = '\033[32m{item}\033[0m'.format(item=item)
            line += item + ' '
        out.append(line)
    return '\n'.join(out)


def next_day(old_tiles):
    new_tiles = []
    field = get_field(old_tiles)
    for x in sorted(set([x[0] for x in field])):
        for y in sorted(set([y[1] for y in field])):
            ix = (x, y)
            if ix in field and (field[ix] == 2 or (ix in old_tiles and field[ix] == 1)):
                new_tiles.append(ix)
    return new_tiles


def get_field(black_tiles):
    field = {}
    for x0, y0 in black_tiles:
        for d in DIRECTIONS:
            ix = (x0 + DIRECTIONS[d][0], y0 + DIRECTIONS[d][1])
            if ix not in field:
                field[ix] = 0
            field[ix] += 1
    return field


def solve_24():
    return (
        part_1(read_input(True)) == 10 and part_1(read_input()),
        part_2(read_input(True)) == 2208 and part_2(read_input())
    )


if __name__ == '__main__':
    print(solve_24())
