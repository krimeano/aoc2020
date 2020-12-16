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

    def __int__(self):
        return self.value

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


class Reader:
    def __init__(self, notes: TicketNotes):
        self.notes = notes
        self.notes.validate_tickets()
        self.possible_fields = []
        self.fields_map = {}
        self.found_indexes = []

    def process(self):
        self.init_fields(self.notes.tickets[0])
        for ticket in self.notes.tickets:
            self.process_ticket(ticket)
        return self

    def init_fields(self, ticket: Ticket):
        self.fields_map = {}
        s = len(ticket.values)
        self.possible_fields = [self.notes.fields[:] for i in range(s)]
        self.found_indexes = [False for i in range(s)]
        for xx in self.possible_fields:
            print('|'.join([x.name for x in xx]))

    def process_ticket(self, ticket: Ticket):
        print('ticket', ticket)
        for ix in range(len(ticket.values)):
            self.process_position(ix, ticket.values[ix])

    def process_position(self, pos: int, value: Value):
        if not value.is_valid:
            return
        fields = self.possible_fields[pos]
        if len(fields) < 2:
            return
        # print('\t{0:>3} value ='.format(pos), value)

        valid_fields = []

        for f in fields:
            for a, z in f.limits:
                if a <= value.value <= z:
                    break
            else:
                continue
            valid_fields.append(f)

        self.possible_fields[pos] = valid_fields
        if len(valid_fields) == 1:
            self.clean_up_field(pos, valid_fields[0])

    def clean_up_field(self, found_pos: int, field: Field):
        print('FIELD FOUND!', found_pos, field)
        self.fields_map[field.name] = found_pos
        for ix in range(len(self.possible_fields)):
            if field in self.possible_fields[ix]:
                self.possible_fields[ix].remove(field)
                if len(self.possible_fields[ix]) == 1:
                    self.clean_up_field(ix, self.possible_fields[ix][0])


def solve_16_1(data):
    notes = TicketNotes(data)
    x = notes.validate_tickets()
    # print(notes)
    return x


def solve_16_2(data):
    reader = Reader(TicketNotes(data)).process()
    ticket = [x for x in reader.notes.tickets if x.is_your].pop()
    values = [int(ticket.values[ix]) for ix in [reader.fields_map[p] for p in reader.fields_map if 'departure' in p]]
    out = 1
    for v in values:
        out *= v
    return out


def solve_16():
    return (
        solve_16_1(read_input(True)) == 71 and solve_16_1(read_input()),
        solve_16_2(read_input()),
    )


if __name__ == '__main__':
    print(solve_16())
