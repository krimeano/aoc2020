year = 2020


def read_input():
    with open('./input1.txt') as f:
        return sorted([int(x.strip()) for x in f.readlines() if x.strip()])


def solve_1_1():
    complements = dict()
    numbers = read_input()

    for n in numbers:
        m = year - n
        if m in complements:
            print(m, n, n * m)
            break
        complements[n] = m

    else:
        print('not found')


def solve_1_2():
    complements = dict()
    numbers = read_input()
    s = len(numbers)
    for i in range(s - 2):
        x = numbers[i]
        if x > year / 3:
            continue
        for j in range(i + 1, s - 1):
            y = numbers[j]
            if y in complements:
                ab = complements[y]
                a, b = ab[0], ab[1]
                print(y, a, b, a * b * y)
                return
            z = year - x - y
            if z > y:
                complements[z] = [x, y]


if __name__ == '__main__':
    solve_1_2()
