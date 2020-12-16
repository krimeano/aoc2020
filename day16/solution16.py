from aoclib import read_input


def solve_16():
    return solve_16_1(read_input(True)) and solve_16_1(read_input())


def solve_16_1(data):
    notes = TicketNotes(data)
    out = 0
    for t in notes.tickets:
        for v in t:
            for a, z in notes.limits:
                if a <= v <= z:
                    break
            else:
                out += v
    return out


def solve_16_2(data):
    pass


class TicketNotes:
    def __init__(self, data):
        self.tickets = []
        self.limits = []
        self.mode = 0

        for line in data:
            if line == 'your ticket:':
                self.mode = 1
                continue
            if line == 'nearby tickets:':
                self.mode = 2
                continue

            if self.mode:
                self.append_ticket(self.parse_ticket(line), self.mode == 1)
            else:
                self.append_limit(*self.parse_limit(line))

    def parse_limit(self, line):
        name, data = line.split(':')
        return name, [[int(y.strip()) for y in x.split('-')] for x in data.split('or')]

    def append_limit(self, name, limits):
        # print(name, limits)
        self.limits += limits
        pass

    def parse_ticket(self, line: str):
        return [int(x.strip()) for x in line.split(',')]

    def append_ticket(self, ticket_data, is_your=False):
        self.tickets.append(ticket_data)
        pass


if __name__ == '__main__':
    print(solve_16())
