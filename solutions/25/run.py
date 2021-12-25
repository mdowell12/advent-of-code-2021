from solutions.get_inputs import read_inputs


def run_1(inputs):
    grid, max_x, max_y = _parse_input(inputs)
    _print_grid(grid, max_x, max_y)
    changed = True
    i = 0
    while changed:
        i += 1
        changed, grid = _do_step(grid, max_x, max_y)
        print(i)
    return i


def _do_step(grid, max_x, max_y):
    changed = False
    new_grid = {k: v for k, v in grid.items()}

    # East facing
    for (x, y), val in grid.items():
        if val == '.':
            continue
        next_position, next_value = _get_next_position_east(x, y, val, max_x, max_y, grid)
        if next_value and next_value == '.':
            new_grid[next_position] = val
            new_grid[(x,y)] = '.'
            changed = True

    final_grid = {k: v for k, v in new_grid.items()}
    # South facing
    for (x, y), val in grid.items():
        if val == '.':
            continue
        next_position, next_value = _get_next_position_south(x, y, val, max_x, max_y, new_grid)
        if next_value and next_value == '.':
            final_grid[next_position] = val
            final_grid[(x,y)] = '.'
            changed = True

    return changed, final_grid


def _get_next_position_east(x, y, val, max_x, max_y, grid):
    if val != '>':
        return None, None
    x = x + 1
    if x > max_x:
        x = 0
    return (x, y), grid[(x,y)]


def _get_next_position_south(x, y, val, max_x, max_y, grid):
    if val != 'v':
        return None, None
    y = y + 1
    if y > max_y:
        y = 0
    return (x, y), grid[(x,y)]


def _parse_input(inputs):
    grid = {}
    for y, line in enumerate(inputs):
        for x, val in enumerate(line.strip()):
            grid[(x,y)] = val
    return grid, x, y


def _print_grid(grid, max_x, max_y):
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            val = grid[(x,y)]
            print(str(val), end='')
        print()
    print()


def _assert_grid_equals(expected_input, grid, max_x, max_y):
    expected_grid, _, _ = _parse_input(expected_input)
    if expected_grid == grid:
        return
    else:
        _print_grid(grid, max_x, max_y)
        raise Exception()


def run_tests():
    test_inputs = """
    ...>>>>>...
    """.strip().split('\n')
    grid, max_x, max_y = _parse_input(test_inputs)
    changed, new_grid = _do_step(grid, max_x, max_y)
    _assert_grid_equals("...>>>>.>..".strip().split('\n'), new_grid, max_x, max_y)
    changed, new_grid = _do_step(new_grid, max_x, max_y)
    _assert_grid_equals("...>>>.>.>.".strip().split('\n'), new_grid, max_x, max_y)

    test_inputs = """
    ..........
    .>v....v..
    .......>..
    ..........
    """.strip().split('\n')
    grid, max_x, max_y = _parse_input(test_inputs)
    changed, new_grid = _do_step(grid, max_x, max_y)
    _assert_grid_equals("""
    ..........
    .>........
    ..v....v>.
    ..........
    """.strip().split('\n'), new_grid, max_x, max_y)

    test_inputs = """
    ...>...
    .......
    ......>
    v.....>
    ......>
    .......
    ..vvv..
    """.strip().split('\n')
    grid, max_x, max_y = _parse_input(test_inputs)
    changed, new_grid = _do_step(grid, max_x, max_y)
    _assert_grid_equals("""
    ..vv>..
    .......
    >......
    v.....>
    >......
    .......
    ....v..
    """.strip().split('\n'), new_grid, max_x, max_y)

    test_inputs = """
    v...>>.vv>
    .vv>>.vv..
    >>.>v>...v
    >>v>>.>.v.
    v>v.vv.v..
    >.>>..v...
    .vv..>.>v.
    v.v..>>v.v
    ....v..v.>
    """.strip().split('\n')
    grid, max_x, max_y = _parse_input(test_inputs)
    changed, new_grid = _do_step(grid, max_x, max_y)
    _assert_grid_equals("""
    ....>.>v.>
    v.v>.>v.v.
    >v>>..>v..
    >>v>v>.>.v
    .>v.v...v.
    v>>.>vvv..
    ..v...>>..
    vv...>>vv.
    >.v.v..v.v
    """.strip().split('\n'), new_grid, max_x, max_y)
    changed, new_grid = _do_step(new_grid, max_x, max_y)
    _assert_grid_equals("""
    >.v.v>>..v
    v.v.>>vv..
    >v>.>.>.v.
    >>v>v.>v>.
    .>..v....v
    .>v>>.v.v.
    v....v>v>.
    .vv..>>v..
    v>.....vv.
    """.strip().split('\n'), new_grid, max_x, max_y)

    test_inputs = """
    v...>>.vv>
    .vv>>.vv..
    >>.>v>...v
    >>v>>.>.v.
    v>v.vv.v..
    >.>>..v...
    .vv..>.>v.
    v.v..>>v.v
    ....v..v.>
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 58:
        raise Exception(f"Test 1 did not pass, got {result_1}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(25)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")
