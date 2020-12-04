"""
https://adventofcode.com/2020/day/4

byr (Birth Year) - four digits; at least 1920 and at most 2002.
iyr (Issue Year) - four digits; at least 2010 and at most 2020.
eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
hgt (Height) - a number followed by either cm or in:
If cm, the number must be at least 150 and at most 193.
If in, the number must be at least 59 and at most 76.
hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
pid (Passport ID) - a nine-digit number, including leading zeroes.
cid (Country ID) - ignored, missing or not.
"""
import re


class Field:
    def __init__(self, name, compare_to=None):
        """
        :param str name:
        :param compare_to:
        """
        self.property_name = name
        self.compare_to = compare_to

    def is_valid(self, record):
        """
        :param dict record:
        :return bool:
        """
        return (self.property_name not in record) and True or self.check_value(record[self.property_name])

    def check_value(self, value):
        """
        :param str value:
        :return:
        """
        return True


class Validator:
    def __init__(self, fields=[]):
        """
        :param list[Field] fields:
        """
        self.fields = fields

    def append_field(self, field):
        """
        :param Field field:
        :return:
        """
        self.fields.append(field)
        return self

    def validate(self, record):
        # print('check', record)
        for v in self.fields:
            if not v.is_valid(record):
                return False
        return True


class FieldRequired(Field):
    def __init__(self, name):
        super().__init__(name)

    def is_valid(self, record):
        return self.property_name in record


class FieldRx(Field):
    def __init__(self, name, rx):
        super().__init__(name, rx)

    def check_value(self, value):
        return re.match(self.compare_to, value)


class FieldYear(FieldRx):
    def __init__(self, name, rx='^\\d{4}$'):
        super().__init__(name, rx)


class FieldMin(Field):
    def __init__(self, name, min_v):
        super().__init__(name, min_v)

    def check_value(self, value):
        return self.compare_to <= int(value)


class FieldMax(Field):
    def __init__(self, name, max_v):
        super().__init__(name, max_v)

    def check_value(self, value):
        return self.compare_to >= int(value)


class FieldColorHex(FieldRx):
    def __init__(self, name, rx='^\\#[\\da-f]{6}$'):
        super().__init__(name, rx)


class FieldOneOf(Field):
    def __init__(self, name, items):
        super().__init__(name, items)

    def check_value(self, value):
        return value in self.compare_to


class FieldEyeColor(FieldOneOf):
    def __init__(self, name, items=('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth',)):
        super().__init__(name, items)


class FieldPassportNumber(FieldRx):
    def __init__(self, name, rx='^\\d{9}$'):
        super().__init__(name, rx)


class FieldHeight(FieldRx):
    def __init__(self, name):
        super().__init__(name, '^\\d{2,3}(in|cm)$')

    def check_value(self, value):
        if not re.match(self.compare_to, value):
            return False
        n = int(value[:-2])
        items = value[-2:]
        return (items == 'cm' and (150 <= n <= 193)) or (items == 'in' and (59 <= n <= 76))


def read_input(is_example=False, suffix=''):
    """
    :param bool is_example:
    :param str suffix:
    :return list[dict]:
    """
    input_path = (is_example and 'example' or 'input') + suffix + '.txt'
    with open(input_path) as f:
        return fill_data([x.strip() for x in f.readlines()])


def fill_data(lines):
    """
    :param list[str] lines:
    :return list[dict]:
    """
    out = []
    current = None
    for string in lines:
        if string:
            current = current or {}
            fill_record(current, string)
        else:
            out.append(current)
            current = None
    if current:
        out.append(current)

    return out


def fill_record(record, string):
    """
    :param dict record:
    :param str string:
    :return:
    """
    pp = string.split(' ')

    for p in pp:
        item = p.split(':')
        record[item[0]] = item[1]


def solve_4_1(data) -> int:
    v = Validator([FieldRequired(x) for x in ('byr', 'ecl', 'eyr', 'hcl', 'hgt', 'iyr', 'pid')])
    v.append_field(Field('cid'))
    return sum([v.validate(x) for x in data])


def solve_4_2(data) -> int:
    v = Validator([FieldRequired(x) for x in ('byr', 'ecl', 'eyr', 'hcl', 'hgt', 'iyr', 'pid')])
    v.append_field(Field('cid'))

    v.append_field(FieldYear('byr'))
    v.append_field(FieldMin('byr', 1920))
    v.append_field(FieldMax('byr', 2002))

    v.append_field(FieldYear('iyr'))
    v.append_field(FieldMin('iyr', 2010))
    v.append_field(FieldMax('iyr', 2020))

    v.append_field(FieldYear('eyr'))
    v.append_field(FieldMin('eyr', 2020))
    v.append_field(FieldMax('eyr', 2030))

    v.append_field(FieldHeight('hgt'))

    v.append_field(FieldColorHex('hcl'))

    v.append_field(FieldEyeColor('ecl'))

    v.append_field(FieldPassportNumber('pid'))

    v.append_field(Field('cid'))

    return sum([v.validate(x) for x in data])


def solve_4():
    return (
        (solve_4_1(read_input(True)) == 2) and solve_4_1(read_input()),
        (
                solve_4_2(read_input(True, '_invalid')) == 0
                and solve_4_2(read_input(True, '_valid')) == 4
        ) and solve_4_2(read_input()),
    )


if __name__ == '__main__':
    print(solve_4())
