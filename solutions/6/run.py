from collections import defaultdict

from solutions.get_inputs import read_inputs


def run_1(inputs):
    fish = [int(i) for i in inputs[0].strip().split(',')]
    for _ in range(80):
        for i in range(len(fish)):
            if fish[i] > 0:
                fish[i] = fish[i] - 1
            else:
                fish[i] = 6
                fish.append(8)
    return len(fish)


def run_2(inputs):
    fish = [int(i) for i in inputs[0].strip().split(',')]
    counts = {i: 0 for i in range(9)}
    for f in fish:
        counts[f] = counts[f] + 1
    for _ in range(256):
        temp = {k: v for k, v in counts.items()}
        for day, quantity in counts.items():
            if day > 0:
                temp[day-1] = quantity
            else:
                temp[8] = quantity
        temp[6] = temp[6] + temp[8]
        counts = {k: v for k, v in temp.items()}

    return sum(counts.values())


def run_tests():
    test_inputs = """
    3,4,3,1,2
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 5934:
        raise Exception(f"Test 1 did not past, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 26984457539:
        raise Exception(f"Test 2 did not past, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(6)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
