import numpy as np

from solutions.get_inputs import read_inputs


def run_1(inputs):
    array = np.array([[int(j) for j in i.strip()] for i in inputs])
    low_points = []
    for y in range(len(array)):
        for x in range(len(array[0])):
            adjacents = _get_adjacents(x, y, array)
            if array[y][x] < min(adjacents):
                low_points.append((x, y))

    # _print_array(array, low_points)
    return sum(array[y][x] + 1 for x, y in low_points)


def _get_adjacents(x, y, array):
    result = []
    if x > 0:
        result.append(array[y][x-1])
    if x + 1 < len(array[0]):
        result.append(array[y][x+1])
    if y + 1 < len(array):
        result.append(array[y+1][x])
    if y > 0:
        result.append(array[y-1][x])

    return result


def _print_array(array, low_points):
    for y, row in enumerate(array):
        for x, val in enumerate(row):
            if (x, y) in low_points:
                print('\033[1;31m' + str(val), end=' ')
            else:
                print("\033[0;0m" + str(val), end=' ')
        print()


def run_2(inputs):
    array = np.array([[int(j) for j in i.strip()] for i in inputs])

    basins = []
    for y, row in enumerate(array):
        for x, val in enumerate(row):
            if not any(b.is_in_basin(x, y) for b in basins) and val != 9:
                new_basin = _make_basin(x, y, array)
                basins.append(new_basin)
    sorted_sizes = sorted(b.size() for b in basins)

    result = 1
    for i in sorted_sizes[-3:]:
        result *= i
    return result


def _make_basin(x, y, array):

    processed = set()
    remaining = [(x, y)]
    while remaining:
        point = remaining.pop()
        other_points = []
        other_points += _get_points_in_direction(array, point, 1, 0)
        other_points += _get_points_in_direction(array, point, -1, 0)
        other_points += _get_points_in_direction(array, point, 0, 1)
        other_points += _get_points_in_direction(array, point, 0, -1)
        remaining += [p for p in other_points if p not in processed]
        processed.add(point)
    return Basin(processed)


def _get_points_in_direction(array, point, dir_x, dir_y):
    result = []
    x, y = point
    curr_x, curr_y = x + dir_x, y + dir_y
    while curr_x >= 0 and curr_y >= 0 and curr_x < len(array[0]) and curr_y < len(array) and array[curr_y][curr_x] != 9:
        result.append((curr_x, curr_y))
        curr_x += dir_x
        curr_y += dir_y
    return result


class Basin:

    def __init__(self, points):
        self.points = set(points)

    def size(self):
        return len(self.points)

    def is_in_basin(self, x, y):
        return (x, y) in self.points

    def __repr__(self):
        return f"{self.points}"


def run_tests():
    test_inputs = """
    2199943210
    3987894921
    9856789892
    8767896789
    9899965678
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 15:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 1134:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(9)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
