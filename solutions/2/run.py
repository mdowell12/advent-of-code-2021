from solutions.get_inputs import read_inputs


def run_1(inputs):
    horizontal = 0
    depth = 0

    commands = [(l.strip().split(' ')[0], int(l.strip().split(' ')[1])) for l in inputs]
    for direction, value in commands:
        if direction == "forward":
            horizontal += value
        elif direction == "down":
            depth += value
        elif direction == "up":
            depth -= value
        else:
            raise Exception()

    return horizontal * depth


def run_2(inputs):
    horizontal = 0
    depth = 0
    aim = 0

    commands = [(l.strip().split(' ')[0], int(l.strip().split(' ')[1])) for l in inputs]
    for direction, value in commands:
        if direction == "forward":
            horizontal += value
            depth += aim * value
        elif direction == "down":
            aim += value
        elif direction == "up":
            aim -= value
        else:
            raise Exception()

    return horizontal * depth


def run_tests():
    test_inputs = """
    forward 5
    down 5
    forward 8
    up 3
    down 8
    forward 2
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 150:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 900:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(2)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
