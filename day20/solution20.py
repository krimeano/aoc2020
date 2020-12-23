from aoclib import read_input
from functools import total_ordering


class Puzzle:

    def __init__(self, raw):
        self.tiles = {}
        self.pairs = {}
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

                for a in x.get_sides():
                    for b in y.get_sides():
                        if a == b or a == revert_side(b):
                            self.pairs[x.id][y.id] = self.pairs[y.id][x.id] = True


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
        return tuple(revert_side(x) for x in self.sides[::-1])

    def rotate(self, is_cw=False):
        op = is_cw and [3, 0, 1, 2] or [1, 2, 3, 0]
        self.sides = tuple(self.sides[op[ix]] for ix in range(len(self.sides)))
        self.rotation = (self.rotation + (is_cw and -1 or 1)) % 4
        return self

    def flip(self, is_vertical=False):
        op = is_vertical and [2, 1, 0, 3] or [0, 3, 2, 1]
        self.sides = tuple(revert_side(self.sides[op[ix]]) for ix in range(len(self.sides)))
        self.is_flipped = not self.is_flipped
        return self

    def get_sides(self, is_double_reverted=False):
        is_odd = (self.x + self.y + is_double_reverted) % 2
        return is_odd and self.get_sides_reverted() or self.sides

    def move_to(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y
        return self

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


def solve_20():
    return solve_20_1(read_input(True)) == 20899048083289 and solve_20_1(read_input())


if __name__ == '__main__':
    print(solve_20())
