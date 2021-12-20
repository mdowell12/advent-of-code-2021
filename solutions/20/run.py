from solutions.get_inputs import read_inputs


def run_1(inputs):
    algo = inputs[0].strip()
    grid = _parse_grid(inputs[2:])
    _print_grid(grid)
    for _ in range(2):
        grid = _iterate(grid, algo)
        _print_grid(grid)

    trimmed = _trim_grid(grid)
    _print_grid(trimmed)

    return sum([i == '#' for i in trimmed.values()])


def run_2(inputs):
    algo = inputs[0].strip()
    grid = _parse_grid(inputs[2:])
    for i in range(50):
        print(i)
        grid = _iterate(grid, algo)
        grid = _trim_grid(grid)
    _print_grid(grid)
    return sum([i == '#' for i in grid.values()])


def _trim_grid(grid):
    """
    Trim borders of the grid by creating a new one that only contains points that are
    relevant to the picture. Start in the middle of the picture and work outwards in each
    direction until you find a big blank space, then mark that as the new border on that side.

    Probably doesn't work for pictures with long "corners" that stick out far from the middle.
    """
    min_x, max_x, min_y, max_y = _get_min_max(grid, 10)
    middle = (int((max_x + min_x) / 2), int((max_y + min_y) / 2))

    x, y = middle
    while x >= min_x:
        x -= 1
        if _is_surrounded_by_dots(x, y, grid) and all(_is_surrounded_by_dots(i,j,grid) for i,j in _surrounding(x,y)):
            left_x = x
            break
    else:
        import pdb; pdb.set_trace()
        raise Exception(x)

    x, y = middle
    while x <= max_x:
        x += 1
        if _is_surrounded_by_dots(x, y, grid) and all(_is_surrounded_by_dots(i,j,grid) for i,j in _surrounding(x,y)):
            right_x = x
            break
    else:
        raise Exception(x)

    x, y = middle
    while y >= min_y:
        y -= 1
        if _is_surrounded_by_dots(x, y, grid) and all(_is_surrounded_by_dots(i,j,grid) for i,j in _surrounding(x,y)):
            bottom_y = y
            break
    else:
        raise Exception(y)

    x, y = middle
    while y <= max_y:
        y += 1
        if _is_surrounded_by_dots(x, y, grid) and all(_is_surrounded_by_dots(i,j,grid) for i,j in _surrounding(x,y)):
            top_y = y
            break
    else:
        raise Exception(y)

    return {k: v for k,v in grid.items() if left_x<=k[0]<=right_x and bottom_y<=k[1]<=top_y}


def _is_surrounded_by_dots(x, y, grid):
    return all(grid.get((i,j), '.') == '.' for i,j in _surrounding(x,y))


def _iterate(grid, algo):
    new_grid = {}
    buffer = 10
    min_x, max_x, min_y, max_y = _get_min_max(grid, buffer)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            index = _get_index(x, y, grid)
            new_grid[(x,y)] = algo[index]
    return new_grid


def _get_min_max(grid, buffer):
    min_x = min(i[0] for i in grid.keys()) - buffer
    max_x = max(i[0] for i in grid.keys()) + buffer
    min_y = min(i[1] for i in grid.keys()) - buffer
    max_y = max(i[1] for i in grid.keys()) + buffer
    return min_x, max_x, min_y, max_y


def _get_index(x, y, grid):
    binary = []
    for point in _surrounding(x, y):
        val = grid.get((point[0],point[1]), '.')
        binary.append('1' if val == '#' else '0')
    return int(''.join(binary), 2)


def _surrounding(x, y):
    return [
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


def _parse_grid(lines):
    result = {}
    for y, line in enumerate(lines):
        for x, val in enumerate(line.strip()):
            result[(x,y)] = val
    return result


def _print_grid(grid):
    buffer = 2
    min_x, max_x, min_y, max_y = _get_min_max(grid, buffer)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            val = grid.get((x,y), '.')
            if (x,y) == (0,0):
                val = '0'
            print(str(val), end=' ')
        print()
    print()


def run_tests():
    if (result := _surrounding(0,0)) != [(-1,-1),(0,-1),(1,-1),(-1,0),(0,0),(1,0),(-1,1),(0,1),(1,1)]:
        raise Exception(result)

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

    if (result := _get_index(299, 233, grid)) != 0:
        raise Exception(result)

    result_1 = run_1(test_inputs)
    if result_1 != 35:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 3351:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(20)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
