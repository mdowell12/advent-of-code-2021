from itertools import product

from solutions.get_inputs import read_inputs


def run_1(inputs):
    grid = {(x,y): int(val) for x, line in enumerate(inputs) for y, val in enumerate(line.strip())}
    max_x = max(i[0] for i in grid.keys())
    max_y = max(i[1] for i in grid.keys())

    flashes = 0
    for _ in range(100):
        flash_points = []
        for point in grid:
            grid[point] += 1
            if grid[point] == 10:
                flash_points.append(point)
        while flash_points:
            point = flash_points.pop()
            adjacents = _get_adjacents(point, grid, max_x, max_y)
            for adjacent in adjacents:
                grid[adjacent] += 1
                if grid[adjacent] == 10:
                    flash_points.append(adjacent)
        for point in grid:
            if grid[point] > 9:
                grid[point] = 0
                flashes += 1

    return flashes


def run_2(inputs):
    grid = {(x,y): int(val) for x, line in enumerate(inputs) for y, val in enumerate(line.strip())}
    max_x = max(i[0] for i in grid.keys())
    max_y = max(i[1] for i in grid.keys())

    i = 0
    while True:
        i += 1
        flash_points = []
        for point in grid:
            grid[point] += 1
            if grid[point] == 10:
                flash_points.append(point)

        while flash_points:
            point = flash_points.pop()
            adjacents = _get_adjacents(point, grid, max_x, max_y)
            for adjacent in adjacents:
                grid[adjacent] += 1
                if grid[adjacent] == 10:
                    flash_points.append(adjacent)

        all_flashing = True
        for point in grid:
            if grid[point] > 9:
                grid[point] = 0
            else:
                all_flashing = False

        if all_flashing:
            break


    return i


def _get_adjacents(point, grid, max_x, max_y):
    x, y = point
    result = []

    for i, j in product([-1, 0, 1], [-1, 0, 1]):
        next_x = x + i
        next_y = y + j
        if 0 <= next_x <= max_x and 0 <= next_y <= max_y and (x,y) != (next_x,next_y):
            result.append((next_x, next_y))

    return result


def _print_grid(grid):
    max_x = max(i[0] for i in grid.keys())
    max_y = max(i[1] for i in grid.keys())
    for x in range(max_x + 1):
        for y in range(max_y + 1):
            val = grid[(x,y)]
            if val == 0:
                print('\033[1;31m' + str(val), end=' ')
            else:
                print("\033[0;0m" + str(val), end=' ')
        print()


def run_tests():
    test_inputs = """
    5483143223
    2745854711
    5264556173
    6141336146
    6357385478
    4167524645
    2176841721
    6882881134
    4846848554
    5283751526
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 1656:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 195:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(11)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
