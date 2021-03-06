from aoclib import read_input


class Ruleset:
    def __init__(self, debug=False):
        self.rules = dict()
        self.debug = debug

    def create_rules(self, lines):
        for line in lines:
            rr = line.split(':')
            self.set_rule(int(rr[0]), rr[1])
        return self

    def set_rule(self, ix: int, definition=''):
        self.get_rule(ix).define(definition)

    def get_rule(self, ix: int):
        """
        :param ix:
        :return Rule:
        """
        if ix not in self.rules:
            self.rules[ix] = Rule(self, ix)
        return self.rules[ix]

    def optimize(self):
        for ix in self.rules:
            if self.rules[ix].optimize_rule():
                del self.rules[ix]
        return self

    def validate(self, line: str) -> bool:
        self.debug and print('\nvalidate', line)
        mm = self.rules[0].match(line)
        is_valid = len([(h, t) for h, t in mm if not t]) > 0
        self.debug and print(line, is_valid and 'is valid' or 'is not valid')
        return is_valid

    def __str__(self):
        out = 'RULESET'

        levels = []
        added_rules = set()
        current_level = {self.get_rule(0)}
        while len(current_level):
            levels.insert(0, current_level)
            added_rules = added_rules.union(current_level)
            next_level = set()
            for x in current_level:
                for yy in x.sub:
                    for y in yy:
                        if y not in added_rules:
                            next_level.add(y)
            current_level = next_level
        clean_levels = []
        considered = set()
        for level in levels:
            clean_level = level.difference(considered)
            clean_levels.insert(0, clean_level)
            considered = considered.union(clean_level)

        for t in range(len(clean_levels)):
            prefix = '\n' + '\t' * t
            for x in clean_levels[t]:
                out += prefix + str(x)

        return out


class Rule:
    def __init__(self, ruleset: Ruleset, ix: int):
        self.ix = ix
        self.ruleset = ruleset
        self.char = ''
        self.sub = []
        self.sup = dict()

    def define(self, definition=''):
        """
        :param definition:
        :return Rule:
        """
        definition = definition.strip()
        if definition[0] == definition[-1] == '"':
            self.char = definition[1:-1]
            return self
        self.sub = []
        for yy in definition.split('|'):
            self.append_sub(yy)

        return self

    def append_sub(self, sub_def: str):
        yy = sub_def.strip().split(' ')
        self.sub.append([self.ruleset.get_rule(int(y)).set_sup(self.ix) for y in yy])
        pass

    def set_sup(self, ix):
        """
        :param ix:
        :return Rule:
        """
        if ix not in self.sup:
            self.sup[ix] = self.ruleset.get_rule(ix)
        return self

    def optimize_rule(self):
        if len(self.sub) != 1 or not len(self.sup):
            return False

        print('optimizing', self)
        for y in self.sub[0]:
            y.update_sup(self)

        for hw in self.sup:
            self.sup[hw].update_sub(self)
        pass

    def update_sup(self, sup_rule):
        """
        :param Rule sup_rule:
        :return:
        """
        # print('remove sup', sup_rule.ix, 'from', self.ix)

        if sup_rule.ix not in self.sup:
            return self

        for hw in sup_rule.sup:
            self.sup[hw] = sup_rule.sup[hw]
        del self.sup[sup_rule.ix]

        return self

    def update_sub(self, sub_rule):
        """
        :param Rule sub_rule:
        :return:
        """
        # print('\t', 'remove', sub_rule.ix, 'from', self.ix)
        for ix in range(len(self.sub)):
            yy = self.sub[ix]
            if sub_rule not in yy:
                continue
            jy = yy.index(sub_rule)
            self.sub[ix] = yy[:jy] + sub_rule.sub[0] + yy[jy + 1:]
        return self

    def __str__(self):
        sup = ''
        sub = ''
        char = ''
        if self.char:
            char = '"{c}"'.format(c=self.char)
        else:
            sup = '(' + ','.join([str(w) for w in sorted(self.sup)]) + ')'
            sub = '|'.join([','.join([y.char or str(y.ix) for y in yy]) for yy in self.sub])
        return '{ix}{sup}:{sub}{char}'.format(ix=self.ix, sup=sup, sub=sub, char=char)

    def match(self, line):
        """
        :param str line:
        :return list[(str,str)]:
        """
        self.ruleset.debug and print('\t', self, 'matching', line)
        head = ''
        tail = line[:]

        if not line:
            return [(head, tail)]

        if self.char:
            if line[0] == self.char:
                head, tail = line[0], line[1:]
            return [(head, tail)]

        out = []

        for yy in self.sub:
            out += self.match_sub_rules(yy, line)

        return out

    def match_sub_rules(self, yy, line):
        """
        :param list[Rule] yy:
        :param line:
        :return list[(str,str)]:
        """
        if not yy:
            return [('', line[:])]

        y = yy[-1]
        out = []
        for h0, t0 in self.match_sub_rules(yy[:-1], line):
            out += [(h0 + h, t) for h, t in y.match(t0) if h]
        return out


def solve_19_1(data):
    rules = [line for line in data if ':' in line]
    strings = [line for line in data if ':' not in line]
    ruleset = Ruleset().create_rules(rules)

    # print(ruleset)
    # print('-' * 79)
    # ruleset.optimize()
    # print('-' * 79)
    # print(ruleset)

    out = 0
    for line in strings:
        out += ruleset.validate(line)
    print(out)
    return out


def solve_19_2(data):
    rules = [line for line in data if ':' in line]
    strings = [line for line in data if ':' not in line]

    ruleset = Ruleset(False).create_rules(rules)

    ruleset.get_rule(8).append_sub('42 8')
    ruleset.get_rule(11).append_sub('42 11 31')
    out = 0
    for line in strings:
        out += ruleset.validate(line)
    return out


def solve_19():
    return (
        solve_19_1(read_input(True)) == 2 and solve_19_1(read_input()),
        solve_19_1(read_input(True, '2')) == 3 and solve_19_2(read_input(True, '2')) == 12 and solve_19_2(read_input())
    )


if __name__ == '__main__':
    print(solve_19())
