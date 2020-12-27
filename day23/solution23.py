example = '389125467'
expected_0 = 92658374
expected = 67384529
expected_2 = 149245887792
input_data = '364289715'

PICKUP = [1, 2, 3]


class Game:
    def __init__(self, data, total=0):
        self.step = 0
        self.current = 0
        self.cups = []
        self.max_n = 0
        self.size = 0
        self.cup_ixs = [0]
        self.current = 0
        self.pick_up = [0, 0, 0]

        self.init_cups([int(x) for x in data], total)

        # print(self.cups, self.cup_ixs)

    def init_cups(self, cups, total=0):
        self.cups = cups + [x + 1 for x in range(max(cups), total)]
        self.size = len(self.cups)
        self.max_n = max(self.cups)
        self.cup_ixs = [0] * (self.max_n + 1)
        for ix in range(len(self.cups)):
            self.cup_ixs[self.cups[ix]] = ix

    def move(self):
        pick_up_ixs = [(self.current + x) % self.size for x in PICKUP]
        n = (self.cups[self.current] - 1) or self.max_n
        move_ix = self.cup_ixs[n]
        while move_ix in pick_up_ixs:
            n = (n - 1) or self.max_n
            move_ix = self.cup_ixs[n]

        for ix in range(3):
            self.pick_up[ix] = self.cups[pick_up_ixs[ix]]

        # print(pick_up_ixs, self.pick_up, n, self.cup_ixs[n])

        ix = self.current
        jy = (self.current + 3) % self.size
        while jy != move_ix:
            ix = (ix + 1) % self.size
            jy = (jy + 1) % self.size
            x = self.cups[jy]
            self.cups[ix] = x
            self.cup_ixs[x] = ix

        for jy in range(3):
            ix = (ix + 1) % self.size
            x = self.pick_up[jy]
            self.cups[ix] = x
            self.cup_ixs[x] = ix

        # current_cup = self.cups[0]
        # pick_up = self.cups[1:4]
        # rest = self.cups[4:]
        # n = (current_cup - 1) or self.max_n
        # while n in pick_up:
        #     n = (n - 1) or self.max_n
        # ix = rest.index(n)
        # self.cups = rest[:ix + 1] + pick_up + rest[ix + 1:] + [current_cup]
        self.step += 1
        self.current = (self.current + 1) % self.size
        return self

    def __str__(self):
        out = 'cups: '
        for ix in range(len(self.cups)):
            f = ' {x} '
            if ix == self.current:
                f = '({x})'
            elif ix in [(self.current + x) % len(self.cups) for x in [1, 2, 3]]:
                f = '\033[31m' + ' {x} ' + '\033[0m'
            out += f.format(x=self.cups[ix])

        return out

    def __int__(self):
        ix = self.cups.index(1)
        out = self.cups[ix + 1:] + self.cups[:ix]
        return int(''.join(str(x) for x in out))


class BigGame(Game):
    def __init__(self, data, total=0):
        super().__init__(data, total)

    def __int__(self):
        ix = self.cups.index(1)
        return self.cups[(ix + 1) % self.max_n] * self.cups[(ix + 2) % self.max_n]


def part_1(data, debug=False):
    moves = debug and 10 or 100
    game = Game(data)
    print(game)
    while game.step < moves:
        game.move()
        debug and print(game.step, game)
    out = int(game)
    return out


def part_2(data):
    moves = 10 ** 7
    game = BigGame(data, 10 ** 6)
    while game.step < moves:
        game.move()
        if not game.step % 10:
            print(game.step)
    out = int(game)
    print('OUT = ', out)
    return out


def solve_23():
    return (
        part_1(example, debug=True) == expected_0 and part_1(example) == expected and part_1(input_data),
        part_2(example) == expected_2
    )


if __name__ == '__main__':
    print(solve_23())
