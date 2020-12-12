from aoclib import read_input

SEAT_FLOOR = '.'
SEAT_EMPTY = 'L'
SEAT_OCCUPIED = '#'


def solve_11():
    return (
        solve_11_1(read_input(True)) == 37 and solve_11_1(read_input()),
        solve_11_2(read_input(True)) == 26 and solve_11_2(read_input())
    )


def solve_11_1(seats) -> int:
    behavior = PassengerBehavior(seats)
    while behavior.iterate() and behavior.counter < 100:
        pass
    return behavior.total


def solve_11_2(seats) -> int:
    behavior = AdjustedBehavior(seats)
    while behavior.iterate() and behavior.counter < 100:
        pass
    return behavior.total


class PassengerBehavior:
    total = 0
    counter = 0
    intolerance = 4

    directions = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))

    def __init__(self, seats):
        """
        :param list[list[str]] seats:
        """
        self.seats = seats
        self.h = len(seats)
        self.w = len(seats[0])

    def iterate(self, debug=False):
        self.counter += 1
        self.total = 0

        has_changed = False
        new_seats = []

        for i in range(self.h):
            new_seats.append('')
            for j in range(self.w):
                new_seats[i] += self.get_new_state(i, j)
                has_changed = has_changed or (new_seats[i][j] != self.seats[i][j])
                self.total += new_seats[i][j] == SEAT_OCCUPIED
            debug and print(new_seats[i])

        self.seats = new_seats

        return has_changed

    def get_new_state(self, row, col):
        s = self.seats[row][col]

        if s == SEAT_FLOOR:
            return SEAT_FLOOR

        neighbours = 0

        for direction in self.directions:
            if self.is_direction_occupied(row, col, direction):
                if s == SEAT_EMPTY:
                    return SEAT_EMPTY
                neighbours += 1
                if neighbours >= self.intolerance:
                    return SEAT_EMPTY

        return SEAT_OCCUPIED

    def is_direction_occupied(self, row, col, direction):
        i, j = row + direction[0], col + direction[1]
        return 0 <= i < self.h and 0 <= j < self.w and self.seats[i][j] == SEAT_OCCUPIED


class AdjustedBehavior(PassengerBehavior):
    intolerance = 5

    def __init__(self, seats):
        super().__init__(seats)

    def is_direction_occupied(self, row, col, direction):
        i, j = row + direction[0], col + direction[1]
        if 0 <= i < self.h and 0 <= j < self.w:
            if self.seats[i][j] == SEAT_FLOOR:
                return self.is_direction_occupied(i, j, direction)
            return self.seats[i][j] == SEAT_OCCUPIED
        return False


if __name__ == '__main__':
    try:
        print(solve_11())
    except Exception as e:
        print('ERROR', e)
        exit(1)
