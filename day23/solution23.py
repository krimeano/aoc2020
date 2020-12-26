example = '389125467'
expected_0 = 92658374
expected = 67384529
input_data = '364289715'


class Game:
    def __init__(self, cups: str):
        self.cups = [int(x) for x in cups]
        self.pick_up = [0, 0, 0]
        self.step = 0
        self.current = 0

    def move(self):
        self.step += 1
        current_cup = self.cups[0]
        pick_up = self.cups[1:4]
        rest = self.cups[4:]
        n = current_cup
        while n not in rest:
            n = (n - 1) or 9
        ix = rest.index(n)
        self.cups = rest[:ix + 1] + pick_up + rest[ix + 1:] + [current_cup]
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


def part_1(data, debug=False):
    moves = debug and 10 or 100
    game = Game(data)
    while game.step < moves:
        game.move()
        debug and print(game.step, game)
    out = int(game)
    return out


def part_2(data):
    return 0


def solve_23():
    return (
        part_1(example, debug=True) == expected_0 and part_1(example) == expected and part_1(input_data),
        part_2(input_data)
    )


if __name__ == '__main__':
    print(solve_23())
