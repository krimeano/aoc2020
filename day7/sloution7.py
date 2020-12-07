def read_input(is_example=False):
    input_path = is_example and 'example.txt' or 'input.txt'
    with open(input_path) as f:
        return f.readlines()


def process_data(input_data):
    out = dict()
    for line in input_data:
        bag_data = process_line(line)
        if not bag_data:
            continue
        out[bag_data[0]] = bag_data[1]
    return out


def process_line(string: str):
    parts = string.strip().split(' bags contain ')
    if len(parts) < 2:
        return None

    if parts[1] == 'no other bags.':
        return parts[0], {}

    out = {}
    for bag in [x.split(' bag')[0] for x in parts[1].split(', ')]:
        bag_info = bag.split(' ')
        n = int(bag_info.pop(0))
        out[' '.join(bag_info)] = n

    return parts[0], out


def revert_bags_map(bags_contain):
    out = dict()
    for x in bags_contain:
        for y in bags_contain[x]:
            if y not in out:
                out[y] = {}
            out[y][x] = bags_contain[x][y]
    return out


def walk_bags(bags_in, target_color='shiny gold'):
    possible_bags = set()
    if target_color not in bags_in:
        return possible_bags
    for x in bags_in[target_color]:
        possible_bags.add(x)
        possible_bags.update(walk_bags(bags_in, x))
    return possible_bags


def solve_7_1(input_data, target_color='shiny gold') -> int:
    bags_contain = process_data(input_data)
    for x in bags_contain:
        print(x, '<', ', '.join(sorted(bags_contain[x])) or '---')
    bags_in = revert_bags_map(bags_contain)
    print('-' * 79)
    for x in bags_in:
        print(x, '>', ', '.join(sorted(bags_in[x])) or '---')
    possible_bags = walk_bags(bags_in, target_color)
    return len(possible_bags)


def solve_7():
    return solve_7_1(read_input(True)) == 4 and solve_7_1(read_input())


if __name__ == '__main__':
    try:
        print(solve_7())
    except Exception as e:
        print('ERROR', e)
        exit(1)
