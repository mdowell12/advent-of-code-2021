from solutions.get_inputs import read_inputs


def run_1(inputs):
    pass


def run_2(inputs):
    pass


def run_tests():
    test_inputs = """

    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 0:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    # result_2 = run_2(test_inputs)
    # if result_2 != 0:
    #     raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(24)

    # result_1 = run_1(input)
    # print(f"Finished 1 with result {result_1}")

    # result_2 = run_2(input)
    # print(f"Finished 2 with result {result_2}")
