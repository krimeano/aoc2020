from aoclib import read_input


def init_neighbours_relative():
    out = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                x = i - 1
                y = j - 1
                z = k - 1
                if not x and not y and not z:
                    continue
                out.append((z, y, x))
    return tuple(out)


NN = init_neighbours_relative()


class Conway:
    KEEP_ACTIVE = 2
    ACTIVATE = 3

    def __init__(self, data):
        """
        :param list[str] data:
        """
        self.limits = {
            'x': [0, 0],
            'y': [0, 0],
            'z': [0, 0]
        }
        self.known_cells = dict()
        self.active_cells = dict()
        self.tension = dict()
        self.init_cells(data)
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
        y0 = -(h // 2)
        w = len(data[0])
        x0 = -(w // 2)
        for row in range(h):
            for col in range(w):
                if data[row][col] == '#':
                    self.active_cells[self.get_cell(col + x0, row + y0)] = True
        return self

    def get_cell(self, x: int, y: int, z=0):
        if z not in self.known_cells:
            self.update_limits('z', z).known_cells[z] = dict()

        if y not in self.known_cells[z]:
            self.update_limits('y', y).known_cells[z][y] = dict()

        if x not in self.known_cells[z][y]:
            self.update_limits('x', x).known_cells[z][y][x] = (x, y, z)

        return self.known_cells[z][y][x]

    def update_limits(self, axis: str, value: int):
        if value < self.limits[axis][0]:
            self.limits[axis][0] = value
        elif value > self.limits[axis][1]:
            self.limits[axis][1] = value
        return self

    def calculate_field_tension(self):
        self.tension = dict()
        for a, b, c in self.active_cells:
            for i, j, k in NN:
                cell = self.get_cell(a + i, b + j, c + k)
                if cell not in self.tension:
                    self.tension[cell] = 0
                self.tension[cell] += 1
        return self

    def __str__(self):
        zz = '\n\n'.join([self.str_slice(z) for z in self.get_range('z')])
        w = max(13, self.limits['y'][1] - self.limits['y'][0])
        return '-' * w + '\nGeneration {g}\n{zz}'.format(g=self.generation, zz=zz) + '\n' + '-' * w

    def str_slice(self, z: int) -> str:
        rr = '\n'.join([self.str_row(y, z) for y in self.get_range('y')])
        return '\nz={z}:\n{rr}'.format(z=z, rr=rr)

    def str_row(self, y: int, z: int) -> str:
        return ''.join([self.str_cell(x, y, z) for x in self.get_range('x')])

    def str_cell(self, x: int, y: int, z: int) -> str:
        return self.get_cell(x, y, z) in self.active_cells and '#' or '.'

    def get_range(self, axis: str):
        return range(self.limits[axis][0], self.limits[axis][1] + 1)


def solve_17_1(data):
    conway = Conway(data)

    while conway.next_generation() < 6:
        # print(conway)
        pass
    print(conway, conway.generation, len(conway.active_cells))
    return len(conway.active_cells)


def solve_17():
    return solve_17_1(read_input(True)) == 112 and solve_17_1(read_input())


if __name__ == '__main__':
    print(solve_17())
