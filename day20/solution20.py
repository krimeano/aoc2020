from aoclib import read_input

SIDES = 4

SHIFTS = [
    {'x': -1, 'y': 0},
    {'x': 0, 'y': 1},
    {'x': 1, 'y': 0},
    {'x': 0, 'y': -1},
]

SHIFTS_ODD = [
    {'x': 1, 'y': 0},
    {'x': 0, 'y': -1},
    {'x': -1, 'y': 0},
    {'x': 0, 'y': 1},
]

MONSTER = [
    '                  # ',
    '#    ##    ##    ###',
    ' #  #  #  #  #  #   '
]
MH = len(MONSTER)
MW = len(MONSTER[0])


class Puzzle:
    def __init__(self, raw):
        self.tiles = {}
        self.pairs = {}
        self.slots = {0: dict()}
        self.taken_tiles = set()
        self.fulfilled_tiles = set()
        self.tiles_queue = []
        self.big_tile = []

        current_tile = None
        for row in raw:
            if ':' in row:
                current_tile = Tile(row)
                self.tiles[current_tile.id] = current_tile
                continue
            current_tile.add_row(row)

    def __str__(self):
        return '\n'.join([str(self.tiles[x]) for x in self.tiles])

    def find_pairs(self):
        tt = sorted(self.tiles)
        s = len(tt)
        self.pairs = {t: {} for t in tt}
        for ix in range(0, s - 1):
            x = self.tiles[tt[ix]]
            for jy in range(ix + 1, s):
                y = self.tiles[tt[jy]]
                if x.find_any_matching_side(y) >= 0:
                    self.pairs[x.id][y.id] = self.pairs[y.id][x.id] = True

    def solve(self):
        self.find_pairs()
        corner = self.get_first_corner()

        self.slots = {0: dict()}
        self.taken_tiles = set()

        self.slots[0][0] = corner
        self.taken_tiles.add(corner)
        self.tiles_queue = []
        self.add_neighbours_to_queue(corner).process_queue()
        self.merge_tiles()

    def get_first_corner(self):
        """
        :return Tile:
        """
        expected = [1, 2]
        corners = [self.tiles[ix] for ix in self.pairs if len(self.pairs[ix]) == 2]
        for corner in corners:
            sides = [corner.find_any_matching_side(self.tiles[ix]) for ix in self.pairs[corner.id]]
            if sorted(sides) == expected:
                return corner

        corner = corners[0]
        sides = []
        while sides != expected:
            corner.rotate()
            sides = sorted([corner.find_any_matching_side(self.tiles[ix]) for ix in self.pairs[corner.id]])
        return corner

    def add_neighbours_to_queue(self, current):
        # print(current, current.x, current.y)
        self.tiles_queue += [x for x in self.get_free_neighbours(current) if x not in self.tiles_queue]
        return self

    def process_queue(self):
        if not self.tiles_queue:
            return True
        self.tiles_queue = sorted(self.tiles_queue, key=lambda n: len(self.pairs[n.id]))
        other = self.tiles_queue.pop(0)
        current = self.get_taken_neighbours(other).pop()
        self.put_next_tile(current, other)

    def put_next_tile(self, current, other):
        # print('PUTTING', other, 'NEAR', current)
        side = current.find_any_matching_side(other)
        shift = (current.is_odd() and SHIFTS_ODD or SHIFTS)[side]
        other.move_to(current.x + shift['x'], current.y + shift['y'])
        r = 0
        while current.side_matches(other) < 0 and r < 8:
            # print('rotate', other)
            r += 1
            other.rotate()
            if r == 4:
                other.flip()
                # print('flip', other)
        if current.side_matches(other) >= 0:
            # print('MATCHES', current, current.x, current.y, other, other.x, other.y, current.side_matches(other))
            if other.x not in self.slots:
                self.slots[other.x] = dict()
            if other.y not in self.slots[other.x]:
                if not self.check_does_tile_fit(other):
                    raise Exception('TILE DOESNT FIT')
                self.slots[other.x][other.y] = other
                self.taken_tiles.add(other)
                self.add_neighbours_to_queue(other).process_queue()
            else:
                print(other.x, other.y, 'ALREADY TAKEN!')
        else:
            raise Exception('CAN NOT MATCH!!!')
        pass

    def get_taken_neighbours(self, tile):
        """
        :param Tile tile:
        :return list[Tile]:
        """
        return [self.tiles[ix] for ix in self.pairs[tile.id] if self.tiles[ix] in self.taken_tiles]

    def get_free_neighbours(self, tile):
        """
        :param Tile tile:
        :return list[Tile]:
        """
        return [self.tiles[ix] for ix in self.pairs[tile.id] if self.tiles[ix] not in self.taken_tiles]

    def check_does_tile_fit(self, tile):
        """
        :param Tile tile:
        :return bool:
        """
        for shift in SHIFTS:
            x, y = tile.x + shift['x'], tile.y + shift['y']
            if x in self.slots and y in self.slots[x] and tile.side_matches(self.slots[x][y]) < 0:
                return False
        return True

    def merge_tiles(self):
        self.big_tile = []
        for x in sorted(self.slots):
            # print('x=', x)
            band = [self.slots[x][y].get_rows_after_transition() for y in sorted(self.slots[x])]
            # for y in sorted(self.slots[x]):
            #     tile = self.slots[x][y]
            #     print('\ty=', y, tile, tile.is_flipped, tile.rotation)
            #     # print('\t\t' + '\n\t\t'.join(tile.rows), '\n')
            #     print('\t\t\t' + '\n\t\t\t'.join(tile.get_rows_after_transition()), '\n')
            for kz in range(len(band[0])):
                self.big_tile.append(''.join([band[jy][kz] for jy in range(len(band))]))


class Tile:
    def __init__(self, header: str):
        self.sides = (0, 0, 0, 0)
        self.id = int(header[5:-1])
        self.rows = []
        self.x = 0
        self.y = 0
        self.rotation = 0
        self.is_flipped = False
        pass

    def add_row(self, row: str):
        self.rows.append(row)
        if len(self.rows) == len(row):
            self.finalize_tile()
        pass

    def finalize_tile(self):
        self.sides = (
            calc_side(self.rows[0]),
            calc_side([row[-1] for row in self.rows]),
            calc_side(self.rows[-1][::-1]),
            calc_side([row[0] for row in self.rows[::-1]])
        )

    def get_sides_reverted(self):
        op = [2, 3, 0, 1]
        return tuple(revert_side(self.sides[op[ix]]) for ix in range(SIDES))

    def rotate(self, is_cw=False):
        op = is_cw and [3, 0, 1, 2] or [1, 2, 3, 0]
        self.sides = tuple(self.sides[op[ix]] for ix in range(SIDES))
        self.rotation = (self.rotation + (is_cw and -1 or 1)) % 4
        return self

    def flip(self, is_vertical=False):
        op = is_vertical and [2, 1, 0, 3] or [0, 3, 2, 1]
        self.sides = tuple(revert_side(self.sides[op[ix]]) for ix in range(SIDES))
        self.is_flipped = not self.is_flipped
        return self

    def is_odd(self):
        return (self.x + self.y) % 2

    def get_sides(self, is_double_reverted=False):
        is_odd = self.is_odd() ^ is_double_reverted
        return is_odd and self.get_sides_reverted() or self.sides

    def move_to(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y
        return self

    def side_matches(self, other):
        """
        :param Tile other:
        :return:
        """
        my_sides = self.get_sides()
        other_sides = other.get_sides()
        for ix in range(SIDES):
            if my_sides[ix] == other_sides[ix]:
                return ix
        return -1

    def find_any_matching_side(self, other):
        my_sides = self.get_sides()
        other_sides = other.get_sides()
        other_sides_reverted = other.get_sides(True)
        for ix in range(SIDES):
            a = my_sides[ix]
            for jy in range(SIDES):
                if a == other_sides[jy] or a == other_sides_reverted[jy]:
                    return ix
        return -1

    def get_rows_after_transition(self):
        rows = rotate_rows(self.is_flipped and [x[::-1] for x in self.rows] or self.rows[:], self.rotation)
        return [x[1:-1] for x in rows[1:-1]]

    def __str__(self):
        return '{id}: {sides}'.format(id=self.id, sides=self.get_sides())


def calc_side(side):
    """
    :param list[str]|str side:
    :return:
    """
    out = 0
    for x in side:
        out <<= 1
        out += x == '#'
    return out


def revert_side(side: int, size=10) -> int:
    out = 0
    while size:
        size -= 1
        out <<= 1
        out += side & 1
        side >>= 1
    return out


def flip_rows(rows):
    """
    :param list[str] rows:
    :return:
    """
    return [x[::-1] for x in rows]


def rotate_rows(rows, rotations=0):
    rotations = rotations % 4
    if not rotations:
        return rows
    if rotations == 2:
        return [x[::-1] for x in rows[::-1]]
    out = ['' for x in rows[0]]
    if rotations == 1:
        for ix in range(len(rows)):
            for jy in range(len(rows[ix])):
                out[-jy - 1] += rows[ix][jy]
    else:
        for ix in range(len(rows)):
            for jy in range(len(rows[ix])):
                out[jy] = rows[ix][jy] + out[jy]
    return out


def solve_20_1(data):
    puzzle = Puzzle(data)
    puzzle.find_pairs()
    ixs = []
    out = 1
    for p in puzzle.pairs:
        if len(puzzle.pairs[p]) == 2:
            ixs.append(p)
            out *= p
    # print(ixs)
    return out


def get_monster_indexes():
    out = []
    for i in range(MH):
        for j in range(MW):
            if MONSTER[i][j] == '#':
                out.append([i, j])

    return out


CHECK_MONSTER = get_monster_indexes()


def find_monster(area):
    """
    :param list[str] area:
    :return:
    """
    # print('MONSTER:\n' + '\n'.join(MONSTER))
    # print('AREA:\n' + '\n'.join(area))

    # print(CHECK_MONSTER)
    ah = len(area)
    aw = len(area[0])
    # print(ah, aw)
    monsters_found = []
    m = len(CHECK_MONSTER)
    for ix in range(ah - MH):
        for jy in range(aw - MW):
            found = [area[ix + xy[0]][jy + xy[1]] == '#' for xy in CHECK_MONSTER]
            if sum(found) == m:
                monsters_found.append([ix, jy])
    return monsters_found


def draw_monsters(area, found):
    """
    :param list[str] area:
    :param list[list[int]] found:
    :return:
    """
    # print('MONSTER:\n' + '\n'.join(MONSTER))
    # print('AREA:\n' + '\n'.join(area))
    for x0, y0 in found:
        for x, y in CHECK_MONSTER:
            row = [c for c in area[x0 + x]]
            row[y0 + y] = '0'
            area[x0 + x] = ''.join(row)

    print('FOUND\n' + '\n'.join(area))
    return area


def solve_20_2(data):
    puzzle = Puzzle(data)
    puzzle.solve()
    area = puzzle.big_tile
    r = 0
    monsters_found = find_monster(area)
    while not monsters_found and r < 8:
        r += 1
        area = rotate_rows(area, 1)
        if r == 4:
            area = flip_rows(area)

        monsters_found = find_monster(area)
    print(monsters_found)
    area = draw_monsters(area, monsters_found)
    out = 0
    for row in area:
        for c in row:
            out += c == '#'
    return out


def solve_20():
    return (
        solve_20_1(read_input(True)) == 20899048083289 and solve_20_1(read_input()),
        solve_20_2(read_input(True)) == 273 and solve_20_2(read_input())
    )


if __name__ == '__main__':
    print(solve_20())
