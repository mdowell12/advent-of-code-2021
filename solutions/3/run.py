from collections import defaultdict

from solutions.get_inputs import read_inputs


def run_1(inputs):
    cleaned = [i.strip() for i in inputs]

    gamma, epsilon = _get_gamma_and_epsilon(cleaned)

    gamma_10 = int(gamma, base=2)
    epsilon_10 = int(epsilon, base=2)

    print(f"gamma {gamma_10} epsilon {epsilon_10}")
    return gamma_10 * epsilon_10


def run_2(inputs):
    cleaned = [i.strip() for i in inputs]

    possible_oxy_rating = [i for i in cleaned]
    pos = 0
    while (len(possible_oxy_rating) > 1):
        gamma, epsilon = _get_gamma_and_epsilon(possible_oxy_rating)
        val = gamma[pos]
        possible_oxy_rating = [i for i in possible_oxy_rating if i[pos] == val]
        pos += 1

    possible_co2_rating = [i for i in cleaned]
    pos = 0
    while (len(possible_co2_rating) > 1):
        gamma, epsilon = _get_gamma_and_epsilon(possible_co2_rating)
        val = epsilon[pos]
        possible_co2_rating = [i for i in possible_co2_rating if i[pos] == val]
        pos += 1

    oxy_rating = int(possible_oxy_rating[0], base=2)
    co2_rating = int(possible_co2_rating[0], base=2)

    print(f"oxy {oxy_rating} co2 {co2_rating}")
    return oxy_rating * co2_rating


def _get_gamma_and_epsilon(cleaned):
    counts = defaultdict(lambda: 0)
    for line in cleaned:
        for i, val in enumerate(line):
            counts[i] += int(val)

    gamma = ""
    for i in range(len(cleaned[0])):
        if counts[i] >= len(cleaned) / 2:
            gamma += "1"
        else:
            gamma += "0"
    epsilon = "".join("0" if i == "1" else "1" for i in gamma)

    return gamma, epsilon


def run_tests():
    test_inputs = """
    00100
    11110
    10110
    10111
    10101
    01111
    00111
    11100
    10000
    11001
    00010
    01010
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 198:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 230:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(3)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
