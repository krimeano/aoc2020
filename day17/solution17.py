from aoclib import read_input


def init_cube(d=1):
    if not d:
        return tuple(),
    out = []
    for u in init_cube(d - 1):
        for v in (-1,), (0,), (1,):
            out.append(u + v)
    return tuple(out)


def init_neighbours(d=3):
    return tuple(x for x in init_cube(d) if sum([abs(y) for y in x]))


def get_zero(d=3):
    if d < 1:
        return tuple()
    return (0,) + get_zero(d - 1)


class Conway:
    KEEP_ACTIVE = 2
    ACTIVATE = 3

    def __init__(self, data, d=3):
        """
        :param list[str] data:
        """
        self.dimensions = d
        self.NN = init_neighbours(d)
        self.limits = [[0, 0] for x in range(d)]
        self.known_cells = dict()
        self.active_cells = dict()
        self.tension = dict()
        self.init_cells(data)
        print('\n'.join(data))
        # print(self.limits)
        # print(sorted(self.active_cells))
        self.generation = 0

    def next_generation(self):
        self.generation += 1
        new_cells = dict()
        self.calculate_field_tension()
        for c in self.tension:
            if self.tension[c] == self.ACTIVATE or (self.tension[c] == self.KEEP_ACTIVE and c in self.active_cells):
                new_cells[c] = True
        self.active_cells = new_cells
        return self.generation

    def init_cells(self, data):
        """
        :param list[str] data:
        :return Conway:
        """
        self.active_cells = dict()
        h = len(data)
        x0 = -(h // 2)
        w = len(data[0])
        y0 = -(w // 2)
        zz = get_zero(self.dimensions - 2)
        for row in range(h):
            for col in range(w):
                if data[row][col] == '#':
                    self.active_cells[self.get_cell(row + x0, col + y0, *zz)] = True
        return self

    def get_cell(self, *axes):
        known_cells_slice = self.known_cells
        k = len(axes) - 1

        for ix in range(k):
            axis = axes[ix]
            if axis not in known_cells_slice:
                known_cells_slice[axis] = dict()
                self.update_limits(ix, axis)
            known_cells_slice = known_cells_slice[axis]

        axis = axes[k]

        if axis not in known_cells_slice:
            known_cells_slice[axis] = axes
            self.update_limits(k, axis)

        return known_cells_slice[axis]

    def update_limits(self, axis: int, value: int):
        if value < self.limits[axis][0]:
            self.limits[axis][0] = value
        elif value > self.limits[axis][1]:
            self.limits[axis][1] = value
        return self

    def calculate_field_tension(self):
        self.tension = dict()
        for element in self.active_cells:
            for neighbour in self.NN:
                cell = self.get_cell(*[a + b for a, b in zip(element, neighbour)])
                if cell not in self.tension:
                    self.tension[cell] = 0
                self.tension[cell] += 1
        return self

    def __str__(self):
        if self.dimensions != 3:
            return 'PRINT ONLY 3 DIMENSIONS, TOO LAZY TO IMPLEMENT'
        zz = '\n\n'.join([self.str_slice(z) for z in self.get_range(2)])
        w = max(13, self.limits[1][1] - self.limits[1][0])
        return '-' * w + '\nGeneration {g}\n{zz}'.format(g=self.generation, zz=zz) + '\n' + '-' * w

    def str_slice(self, z: int) -> str:
        rr = '\n'.join([self.str_row(y, z) for y in self.get_range(1)])
        return '\nz={z}:\n{rr}'.format(z=z, rr=rr)

    def str_row(self, y: int, z: int) -> str:
        return ''.join([self.str_cell(x, y, z) for x in self.get_range(0)])

    def str_cell(self, x: int, y: int, z: int) -> str:
        return self.get_cell(x, y, z) in self.active_cells and '#' or '.'

    def get_range(self, axis: int):
        return range(self.limits[axis][0], self.limits[axis][1] + 1)


def solve_17():
    return (
        solve_17_1(read_input(True)) == 112 and solve_17_1(read_input()),
        solve_17_2(read_input(True)) == 848 and solve_17_2(read_input())
    )


def solve_17_1(data, d=3):
    conway = Conway(data, d)

    while conway.next_generation() < 6:
        # print(conway)
        pass
    print(conway, conway.generation, len(conway.active_cells))
    return len(conway.active_cells)


def solve_17_2(data):
    return solve_17_1(data, 4)


if __name__ == '__main__':
    print(solve_17())
