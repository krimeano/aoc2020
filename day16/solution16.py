from aoclib import read_input


class Field:
    def __init__(self, line: str):
        self.name, data = line.split(':')
        self.limits = tuple(tuple(int(y.strip()) for y in x.split('-')) for x in data.split('or'))

    def __str__(self):
        return '{0:>20}: {1}'.format(self.name, ', '.join(['%d-%d' % x for x in self.limits]))


class Value:
    def __init__(self, value: str):
        self.value = int(value.strip())
        self.is_valid = True

    def __str__(self):
        prefix = suffix = ''
        if not self.is_valid:
            prefix = '\033[31m'
            suffix = '\033[39m'
        return prefix + '{:>4}'.format(self.value) + suffix

    def validate(self, limits) -> bool:
        """
        :param list[int] limits:
        :return bool:
        """

        for a, z in limits:
            if a <= self.value <= z:
                break
        else:
            self.is_valid = False

        return self.is_valid


class Ticket:
    def __init__(self, line, is_your=False):
        self.values = tuple(Value(x) for x in line.split(','))
        self.is_your = is_your

    def __str__(self):
        prefix = suffix = ''
        if self.is_your:
            prefix = '\033[43m'
            suffix = '\033[49m'
        return prefix + ','.join(str(x) for x in self.values) + suffix

    def validate_values(self, limits) -> int:
        """
        :param list[int] limits:
        :return int:
        """
        return sum([x.value for x in self.values if not x.validate(limits)])


class TicketNotes:
    def __init__(self, data):
        self.fields = []
        self.tickets = []
        self.limits = []

        mode = 0

        for line in data:
            if line == 'your ticket:':
                mode = 1
                continue

            if line == 'nearby tickets:':
                mode = 2
                continue

            if mode:
                self.tickets.append(Ticket(line, mode == 1))
            else:
                self.fields.append(Field(line))

        for f in self.fields:
            self.limits += f.limits

    def validate_tickets(self) -> int:
        return sum([x.validate_values(self.limits) for x in self.tickets])

    def __str__(self):
        fields = '\n'.join([str(f) for f in self.fields])
        tickets = '\n'.join([str(t) for t in self.tickets])
        return '-' * 79 + '\nFIELDS:\n{0}\n\nTICKETS:\n{1}\n'.format(fields, tickets) + '-' * 79


def solve_16_1(data):
    notes = TicketNotes(data)
    # print(notes)
    return notes.validate_tickets()


def solve_16_2(data):
    notes = TicketNotes(data)
    notes.validate_tickets()
    print(notes)
    return 0


def solve_16():
    return (
        solve_16_1(read_input(True)) == 71 and solve_16_1(read_input()),
        solve_16_2(read_input(True)) and solve_16_2(read_input()),
    )


if __name__ == '__main__':
    print(solve_16())
