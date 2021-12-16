from collections import defaultdict
import heapq

from solutions.get_inputs import read_inputs


def run_1(inputs):
    points = _parse_inputs(inputs)
    max_x = len(inputs[0]) - 1
    max_y = len(inputs) - 1
    return _find_best_path(points, (0, 0), max_x, max_y)


def run_2(inputs):
    orig_points = _parse_inputs(inputs)
    points = _explode_points(orig_points, len(inputs))
    max_x = max(p[0] for p in points)
    max_y = max(p[1] for p in points)
    return _find_best_path(points, (0, 0), max_x, max_y)


def _explode_points(orig_points, size):
    result = {}

    for (x, y), val in orig_points.items():
        for i in range(0, 5):
            for j in range(0, 5):
                new_point = (x+i*size, y+j*size)
                new_val = int((val + i + j) % 9)
                if new_val == 0:
                    new_val = 9
                result[new_point] = new_val
    return result


def _find_best_path(points, curr_point, max_x, max_y):
    """
    Implementation of Dijkstra's algorithm with help from
    https://medium.com/basecs/finding-the-shortest-path-with-a-little-help-from-dijkstra-613149fbdc8e
    """

    open_set = [(0,0)]

    came_from = {}

    g_score = defaultdict(lambda: 1000000)
    g_score[(0,0)] = 0

    visited = set()

    while open_set:
        open_set.sort(key=lambda x: g_score[x])
        current = open_set.pop(0)
        visited.add(current)
        if current[0] == max_x and current[1] == max_y:
            score, path = _score_path(came_from, current, points)
            _print_grid(points, max_x, max_y, path)
            return score
        x,y = current
        nexts = [
            (x + 1, y),
            (x, y + 1),
            (x - 1, y),
            (x, y - 1),
        ]
        for neighbor in nexts:
            if neighbor in visited:
                continue
            if neighbor[0] < 0 or neighbor[0] > max_x or neighbor[1] < 0 or neighbor[1] > max_y:
                continue
            tentative_g_score = g_score[current] + points[neighbor]
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                if neighbor not in open_set:
                    open_set.append(neighbor)

    raise Exception("not found")


def _score_path(came_from, current, points):
    total = 0
    path = []
    while current in came_from:
        total += points[current]
        current = came_from[current]
        path.append(current)

    return total, path


def _parse_inputs(inputs):
    result = {}
    for y, line in enumerate(inputs):
        for x, val in enumerate(line.strip()):
            result[(x,y)] = int(val)
    return result


def _print_grid(points, max_x, max_y, path=None):
    if path is None:
        path = []
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x,y) in path:
                print('X', end=' ')
            else:
                print(points[(x,y)], end=' ')
        print()


def run_tests():
    test_inputs = """
    1163751742
    1381373672
    2136511328
    3694931569
    7463417111
    1319128137
    1359912421
    3125421639
    1293138521
    2311944581
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 40:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 315:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(15)
    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
