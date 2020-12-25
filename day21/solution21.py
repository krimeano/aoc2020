from aoclib import read_input


class Menu:
    def __init__(self, lines):
        self.dishes = []
        self.allergens_in_dishes = {}
        self.allergens_found = {}
        self.all_allergens = set()

        for line in lines:
            self.append_dish(line)

    def append_dish(self, line):
        ii, aa = line[:-1].split(' (contains ')
        ingredients = set(ii.split(' '))
        self.dishes.append(ingredients)

        for a in aa.split(', '):
            if a not in self.allergens_in_dishes:
                self.allergens_in_dishes[a] = ingredients

            self.allergens_in_dishes[a] = self.allergens_in_dishes[a].intersection(ingredients)

    def process(self):
        while self.allergens_in_dishes:
            new_found = {}

            for a in self.allergens_in_dishes:
                if len(self.allergens_in_dishes[a]) != 1:
                    continue
                self.allergens_found[a] = new_found[a] = self.allergens_in_dishes[a]
                self.all_allergens = self.all_allergens.union(self.allergens_in_dishes[a])

            for a in new_found:
                del self.allergens_in_dishes[a]

                for b in self.allergens_in_dishes:
                    self.allergens_in_dishes[b] = self.allergens_in_dishes[b].difference(new_found[a])
        return self


def solve_21_1(data):
    menu = Menu(data).process()
    return sum([len(dish.difference(menu.all_allergens)) for dish in menu.dishes])


def solve_21_2(data):
    menu = Menu(data)
    menu.process()
    print(menu.allergens_found)
    return ','.join([list(menu.allergens_found[x]).pop() for x in sorted(menu.allergens_found)])


def solve_21():
    return (
        solve_21_1(read_input(True)) == 5 and solve_21_1(read_input()),
        solve_21_2(read_input(True)) == 'mxmxvkd,sqjhc,fvjkl' and solve_21_2(read_input())
    )


if __name__ == '__main__':
    print(solve_21())
