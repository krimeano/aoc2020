modulus = 20201227
subject = 7
example = [5764801, 17807724]
expected = 14897079
input_data = [12578151, 5051300]


def part_1(data):
    v = 1
    count = 0
    max_count = modulus
    a = b = 0
    while count < max_count:
        count += 1
        v = v * subject % modulus
        if not count % 1000000:
            print(count, v)
        if v in data:
            if not a:
                a = count
                print('FIRST FOUND', a)
            else:
                b = count
                print('SECOND FOUND', b)
                break
    print(a, b, v)
    s = v
    v = 1
    for ix in range(a):
        v = v * s % modulus
    return v


if __name__ == '__main__':
    print('PART 1')
    print(part_1(example) == expected and part_1(input_data))
