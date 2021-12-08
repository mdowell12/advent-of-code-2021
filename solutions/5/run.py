from collections import defaultdict

from solutions.get_inputs import read_inputs


def run_1(inputs):
    counts = defaultdict(lambda: 0)
    for line in inputs:
        first, second = _parse_line(line)
        segment = _generate_segment(first, second)
        for point in segment:
            counts[point] += 1
    return sum([1 if i > 1 else 0 for i in counts.values()])


def _parse_line(line):
    parts = line.strip().split(' -> ')
    first = [int(i) for i in parts[0].strip().split(',')]
    second = [int(i) for i in parts[1].strip().split(',')]
    return (tuple(first), tuple(second))


def _generate_segment(first, second, count_diags=False):
    is_diag = first[0] != second[0] and first[1] != second[1]
    if not count_diags and is_diag:
        return []

    segment = []
    start_x = min(first[0], second[0])
    end_x = max(first[0], second[0])
    start_y = min(first[1], second[1])
    end_y = max(first[1], second[1])

    if not is_diag:
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                segment.append((x, y))
    else:
        start_point = first if start_x == first[0] else second
        direction = -1 if start_point[1] == end_y else 1
        for i in range(end_x - start_x + 1):
            x = start_x + i
            y = start_point[1] + i * direction
            segment.append((x, y))
    return segment


def _print_grid(counts):
    max_x = max(t[0] for t in counts.keys())
    max_y = max(t[1] for t in counts.keys())
    for y in range(max_y):
        row = []
        for x in range(max_x):
            val = counts[(x,y)]
            row.append('.' if val == 0 else str(val))
        print(''.join(row))


def run_2(inputs):
    counts = defaultdict(lambda: 0)
    for line in inputs:
        first, second = _parse_line(line)
        segment = _generate_segment(first, second, count_diags=True)
        for point in segment:
            counts[point] += 1
    # _print_grid(counts)
    return sum([1 if i > 1 else 0 for i in counts.values()])


def run_tests():
    test_inputs = """
    0,9 -> 5,9
    8,0 -> 0,8
    9,4 -> 3,4
    2,2 -> 2,1
    7,0 -> 7,4
    6,4 -> 2,0
    0,9 -> 2,9
    3,4 -> 1,4
    0,0 -> 8,8
    5,5 -> 8,2
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 5:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 12:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(5)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
