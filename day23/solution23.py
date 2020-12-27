example = '389125467'
expected_0 = 92658374
expected = 67384529
expected_2 = 149245887792
input_data = '364289715'

PICKUP = [1, 2, 3]


class Cup:
    def __init__(self, n: int):
        self.n = n
        self.target: Cup = None
        self.next: Cup = None
        self.is_picked_up = False

    def __str__(self):
        return '{n:>2}'.format(n=self.n)

    def __int__(self):
        return self.n

    def pick_up(self, n=3):
        self.is_picked_up = True
        if n - 1:
            self.next.pick_up(n - 1)

    def get_next(self):
        return self.next.is_picked_up and self.next.get_next() or self.next

    def get_target(self):
        return self.target.is_picked_up and self.target.get_target() or self.target

    def move_before(self, after_target):
        """
        :param Cup after_target:
        :return:
        """
        if not self.is_picked_up:
            raise Exception('can move only picked up cups', self)
        self.is_picked_up = False
        if self.next.is_picked_up:
            self.next.move_before(after_target)
        else:
            self.next = after_target


class Game:
    def __init__(self, data: str, total=0):
        print(data)
        self.one: Cup = None
        self.current: Cup = None
        self.init_cups(data, total)
        self.step = 0

    def init_cups(self, data: str, total=0):
        cups = [Cup(int(x)) for x in data]
        max_n = max(int(x) for x in cups)
        for x in range(max_n, total):
            cups.append(Cup(x + 1))

        self.current = cups[0]
        s = len(cups)
        for ix in range(len(cups)):
            cups[ix].next = cups[(ix + 1) % s]

        cups = sorted(cups, key=lambda x: x.n)
        self.one = cups[0]
        for ix in range(s):
            cups[(ix + 1) % s].target = cups[ix]

        return self

    def move(self):
        # print('MOVE')
        self.step += 1
        picked_up = self.current.next
        picked_up.pick_up()
        next_cup = self.current.get_next()
        target_cup = self.current.get_target()
        after_target = target_cup.next
        target_cup.next = picked_up
        picked_up.move_before(after_target)
        self.current.next = next_cup
        self.current = next_cup
        return self

    def str_picked_up(self, picked_up: Cup):
        if not picked_up.is_picked_up:
            return ''
        return str(picked_up) + self.str_picked_up(picked_up.next)

    def __str__(self):
        out = '(' + str(self.current) + ')'
        x = self.current.next
        while x != self.current:
            out += ' {x} '.format(x=x)
            x = x.next

        return out

    def __int__(self):
        out = 0
        x = self.one.next
        while x != self.one:
            out = 10 * out + int(x)
            x = x.next
        return out


class BigGame(Game):
    def __init__(self, data, total=0):
        super().__init__(data, total)

    def __int__(self):
        a = self.one.next
        print('AFTER 1:', a, a.next)
        return int(a) * int(a.next)


def part_1(data, debug=False):
    moves = debug and 10 or 100
    game = Game(data)
    while game.step < moves:
        game.move()
        debug and print(game.step, game)
    out = int(game)
    return out


def part_2(data):
    moves = 10 ** 7
    game = BigGame(data, 10 ** 6)
    print('INITIATED')
    while game.step < moves:
        game.move()
        if not game.step % 10 ** 6:
            print(game.step, int(game))
    out = int(game)
    return out


def solve_23():
    return (
        part_1(example, debug=True) == expected_0 and part_1(example) == expected and part_1(input_data),
        part_2(example) == expected_2 and part_2(input_data)
    )


if __name__ == '__main__':
    print(solve_23())
