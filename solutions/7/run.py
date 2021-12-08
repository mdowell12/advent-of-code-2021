from solutions.get_inputs import read_inputs


CACHE = {}


def run_1(inputs):
    positions = [int(i) for i in inputs[0].strip().split(',')]

    min_p, max_p = min(positions), max(positions)
    smallest_distance = None
    for i in range(min_p, max_p + 1):
        distance = _calc_total_distance(positions, i)
        if smallest_distance is None or distance < smallest_distance:
            smallest_distance = distance

    return smallest_distance


def _calc_total_distance(positions, i):
    return sum(abs(p - i) for p in positions)


def run_2(inputs):
    positions = [int(i) for i in inputs[0].strip().split(',')]

    min_p, max_p = min(positions), max(positions)
    smallest_distance = None
    for i in range(min_p, max_p + 1):
        distance = _calc_total_distance_exp(positions, i)
        if smallest_distance is None or distance < smallest_distance:
            smallest_distance = distance

    return smallest_distance


def _calc_total_distance_exp(positions, i):
    total = 0
    for p in positions:
        if (p, i) in CACHE:
            total += CACHE[(p, i)]
        else:
            total_p = 0
            for x in range(abs(p - i) + 1):
                total_p += x
            total += total_p
            CACHE[(p, i)] = total_p
    return total


def run_tests():
    test_inputs = """
    16,1,2,0,4,2,7,1,2,14
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 37:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 168:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(7)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
