from collections import defaultdict

from solutions.get_inputs import read_inputs


def run_1(inputs):
    commands = [_parse_line(line) for line in inputs]
    # print('\n'.join(str(l) for l in commands))
    # grid = defaultdict(lambda: False)
    grid = {}
    for command in commands:
        grid = _do_command(command, grid)
        # print(sorted(k for k,v in grid.items() if v))
        print(f'{command} {sum(int(i) for i in grid.values())}')
        # import pdb; pdb.set_trace()
    return sum(int(i) for i in grid.values())


def run_2(inputs):
    pass


def _do_command(command, grid):
    limit = 50
    is_on, (x1, x2), (y1, y2), (z1, z2) = command
    if x1 < -50 or x1 > 50:
        return grid
    x1, x2 = max(min(x1, limit), -limit), max(min(x2, limit), -limit)
    y1, y2 = max(min(y1, limit), -limit), max(min(y2, limit), -limit)
    z1, z2 = max(min(z1, limit), -limit), max(min(z2, limit), -limit)
    print(x1,x2)
    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            for z in range(z1, z2+1):
                # if -50<=x<=50 and -50<=y<=50 and -50<=z<=50:
                grid[(x,y,z)] = is_on
    return grid


def _parse_line(line):
    line = line.strip()
    is_on = line.split(' ')[0].strip() == 'on'
    x,y,z = line.replace('on ', '').replace('off ', '').split(',')
    # import pdb; pdb.set_trace()
    x1, x2 = map(int, x.replace('x=','').split('..'))
    y1, y2 = map(int, y.replace('y=','').split('..'))
    z1, z2 = map(int, z.replace('z=','').split('..'))
    return is_on, (x1,x2), (y1,y2), (z1,z2)


def run_tests():
    test_inputs = """
    on x=10..12,y=10..12,z=10..12
    on x=11..13,y=11..13,z=11..13
    off x=9..11,y=9..11,z=9..11
    on x=10..10,y=10..10,z=10..10
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 39:
        raise Exception(f"Test 1a did not pass, got {result_1}")

    test_inputs = """
    on x=-20..26,y=-36..17,z=-47..7
    on x=-20..33,y=-21..23,z=-26..28
    on x=-22..28,y=-29..23,z=-38..16
    on x=-46..7,y=-6..46,z=-50..-1
    on x=-49..1,y=-3..46,z=-24..28
    on x=2..47,y=-22..22,z=-23..27
    on x=-27..23,y=-28..26,z=-21..29
    on x=-39..5,y=-6..47,z=-3..44
    on x=-30..21,y=-8..43,z=-13..34
    on x=-22..26,y=-27..20,z=-29..19
    off x=-48..-32,y=26..41,z=-47..-37
    on x=-12..35,y=6..50,z=-50..-2
    off x=-48..-32,y=-32..-16,z=-15..-5
    on x=-18..26,y=-33..15,z=-7..46
    off x=-40..-22,y=-38..-28,z=23..41
    on x=-16..35,y=-41..10,z=-47..6
    off x=-32..-23,y=11..30,z=-14..3
    on x=-49..-5,y=-3..45,z=-29..18
    off x=18..30,y=-20..-8,z=-3..13
    on x=-41..9,y=-7..43,z=-33..15
    on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
    on x=967..23432,y=45373..81175,z=27513..53682
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 590784:
        raise Exception(f"Test 1b did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 2758514936282235:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(22)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    # result_2 = run_2(input)
    # print(f"Finished 2 with result {result_2}")
