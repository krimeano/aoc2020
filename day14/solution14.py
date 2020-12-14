from aoclib import read_input


def solve_14():
    return solve_14_1(read_input(True)) == 165 and solve_14_1(read_input())


def solve_14_1(data):
    mand = 2 ** 36 - 1
    mor = 0
    stored = dict()

    for line in data:
        address, value = line.split(' = ')

        if address == 'mask':
            mand = mor = 0
            for bit in value:
                mand <<= 1
                mor <<= 1
                mor += bit == '1'
                mand += bit != '0'
        else:
            stored[address] = (int(value) | mor) & mand
    return sum([stored[ix] for ix in stored])


if __name__ == '__main__':
    try:
        print(solve_14())
    except Exception as exc:
        print(exc)
        exit(1)
