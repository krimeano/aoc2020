from aoclib import read_input

ONE = 2 ** 36 - 1


def solve_14():
    return (
        solve_14_1(read_input(True)) == 165 and solve_14_1(read_input()),
        solve_14_2(read_input(True, '2')) == 208 and solve_14_2(read_input())
    )


def solve_14_1(data):
    m_and = ONE
    m_or = 0
    stored = dict()

    for line in data:
        address, value = line.split(' = ')

        if address == 'mask':
            m_and = m_or = 0
            for bit in value:
                m_and <<= 1
                m_or <<= 1
                m_or += bit == '1'
                m_and += bit != '0'
        else:
            stored[address] = (int(value) | m_or) & m_and
    return sum([stored[ix] for ix in stored])


def solve_14_2(data):
    stored = dict()
    m_or = 0
    m_par = []
    par_max = 1
    for line in data:
        cmd, value = line.split(' = ')
        if cmd == 'mask':
            m_or = 0
            m_par = []
            for bit in value:
                m_or <<= 1
                m_par = [x << 1 for x in m_par]
                if bit == '1':
                    m_or += 1
                elif bit == 'X':
                    m_par.append(1)
            par_max = 2 ** len(m_par)
        else:
            address0 = int(cmd.split(']')[0].split('[')[1]) | m_or
            stored[address0] = int(value)
            if par_max < 2:
                continue
            for i in range(par_max):
                addr = address0
                for pos in range(len(m_par)):
                    if i & (2 ** pos):
                        addr |= m_par[pos]
                    else:
                        addr &= ONE ^ m_par[pos]
                stored[addr] = int(value)
    return sum([stored[ix] for ix in stored])


if __name__ == '__main__':
    print(solve_14())
