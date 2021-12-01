from solutions.get_inputs import read_inputs


def run_1(inputs):
    nums = [int(i) for i in inputs]
    increases = 0
    previous = None
    for i in nums:
        if previous is not None and i > previous:
            increases += 1
        previous = i

    return increases


def run_2(inputs):
    nums = [int(i) for i in inputs]
    increases = 0
    previous = (nums[0], nums[1], nums[2])
    for i in nums[3:]:
        next = (previous[1], previous[2], i)
        if sum(next) > sum(previous):
            increases += 1
        previous = next

    return increases


def run_tests():
    test_inputs = """
    199
    200
    208
    210
    200
    207
    240
    269
    260
    263
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 7:
        raise Exception(f"Test 1 did not past, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 5:
        raise Exception(f"Test 2 did not past, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(1)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
