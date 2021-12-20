from solutions.get_inputs import read_inputs


def run_1(inputs):
    algo = inputs[0].strip()
    grid = _parse_grid(inputs[2:])
    _print_grid(grid)
    for _ in range(2):
        grid = _iterate(grid, algo)
        _print_grid(grid)
    return sum([i == '#' for i in grid.values()])


def run_2(inputs):
    pass


def _iterate(grid, algo):
    new_grid = {}
    buffer = 1
    min_x = min(i[0] for i in grid.keys()) - buffer
    max_x = max(i[0] for i in grid.keys()) + buffer
    min_y = min(i[1] for i in grid.keys()) - buffer
    max_y = max(i[1] for i in grid.keys()) + buffer
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            # if (0,1) == (x,y):
            #     import pdb; pdb.set_trace()
            index = _get_index(x, y, grid)
            new_grid[(x,y)] = algo[index]
    return new_grid


def _get_index(x, y, grid):
    binary = []
    surrounding = [
        (x-1,y-1),
        (x,y-1),
        (x+1,y-1),

        (x-1,y),
        (x,y),
        (x+1,y),

        (x-1,y+1),
        (x,y+1),
        (x+1,y+1),
    ]
    for point in (surrounding):
    # surrounding = [
    #     (x-1,y-1),
    #     (x-1,y),
    #     (x-1,y+1),
    #     (x,y-1),
    #     (x,y),
    #     (x,y+1),
    #     (x+1,y-1),
    #     (x+1,y),
    #     (x+1,y+1),
    # ]
    # for point in reversed(surrounding):
        val = grid.get((point[0],point[1]), '.')
        binary.append('1' if val == '#' else '0')
        if (x,y) == (0,2):
            print(point, val, binary)
    return int(''.join(binary), 2)


def _parse_grid(lines):
    result = {}
    for y, line in enumerate(lines):
        for x, val in enumerate(line.strip()):
            result[(x,y)] = val
    return result



def _print_grid(grid):
    buffer = 2
    min_x = min(i[0] for i in grid.keys()) - buffer
    max_x = max(i[0] for i in grid.keys()) + buffer
    min_y = min(i[1] for i in grid.keys()) - buffer
    max_y = max(i[1] for i in grid.keys()) + buffer
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            val = grid.get((x,y), '.')
            if (x,y) == (0,0):
                val = '0'
            print(str(val), end=' ')
        print()
    print()


def run_tests():
    test_inputs = """
    ..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

    #..#.
    #....
    ##..#
    ..#..
    ..###
    """.strip().split('\n')
    grid = _parse_grid(test_inputs[2:])
    if (result := _get_index(2, 2, grid)) != 34:
        raise Exception(result)

    result_1 = run_1(test_inputs)
    if result_1 != 35:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    # result_2 = run_2(test_inputs)
    # if result_2 != 0:
    #     raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(20)

    result_1 = run_1(input)
    # 5881 is not right
    # 5860 is too high
    print(f"Finished 1 with result {result_1}")

    # result_2 = run_2(input)
    # print(f"Finished 2 with result {result_2}")
