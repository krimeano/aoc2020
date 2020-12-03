input_file = './input2.txt'


class InputItem:
    def __init__(self, s: str):
        parts = s.split(':')
        req = parts[0].split(' ')
        numbers = req[0].split('-')

        self.m = int(numbers[0])
        self.n = int(numbers[1])
        self.needle = req[1].strip()
        self.haystack = parts[1].strip()

    def __str__(self):
        return '%d-%d %s: %s' % (self.m, self.n, self.needle, self.haystack_highlighted())

    def is_valid(self):
        k = 0
        for x in self.haystack:
            k += x == self.needle
            if k > self.n:
                return False

        return k >= self.m

    def haystack_highlighted(self):
        return self.haystack


class InputItemNew(InputItem):

    def is_valid(self):
        if not self.m:
            print('AAAAAAAAA')
            exit(1)
        a = self.haystack[self.m - 1] == self.needle
        b = self.haystack[self.n - 1] == self.needle
        return (a and not b) or (not a and b)

    def haystack_highlighted(self):
        chunks = [
            self.haystack[:self.m - 1],
            '\033[31m',
            self.haystack[self.m - 1],
            '\033[0m',
            self.haystack[self.m:self.n - 1],
            '\033[31m',
            self.haystack[self.n - 1],
            '\033[0m',
            self.haystack[self.n:],
        ]
        return ''.join(chunks)


def read_input():
    with open(input_file) as f:
        return sorted([x for x in f.readlines() if x.strip()])


def solve_2_1():
    data = [InputItem(x) for x in read_input()]
    print(len([x for x in data if x.is_valid()]))
    pass


def solve_2_2():
    data = [InputItemNew(x) for x in read_input()]
    for x in data:
        print(x, x.is_valid())
    print(len([x for x in data if x.is_valid()]))
    pass


if __name__ == '__main__':
    solve_2_2()
