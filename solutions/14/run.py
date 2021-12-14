from collections import defaultdict

from solutions.get_inputs import read_inputs


def run_1(inputs):
    return _build_polymer(inputs, 10)


def run_2(inputs):
    return _build_polymer(inputs, 40)


def _build_polymer(inputs, num_steps):
    pair_counts = defaultdict(lambda: 0)
    sequence = list(inputs[0].strip())
    key = {line.split(' -> ')[0].strip(): line.split(' -> ')[1].strip() for line in inputs[2:]}

    # Initiate counts using input sequence
    for i in range(len(sequence) - 1):
        pair_counts[(sequence[i], sequence[i+1])] += 1

    for _ in range(num_steps):
        # Order does not matter, so just make a new counts dict by inserting
        # characters and counting the instances of each new resulting pair
        new_counts = defaultdict(lambda: 0)
        for pair, frequency in pair_counts.items():
            middle = key[f"{pair[0]}{pair[1]}"]
            new_counts[(pair[0], middle)] += frequency
            new_counts[(middle, pair[1])] += frequency
        pair_counts = new_counts

    # Count occurences of each letter in the pairs. This double counts all
    # letters EXCEPT the first and last letters of the original sequence
    letter_counts = defaultdict(lambda: 0)
    for pair, frequency in pair_counts.items():
        letter_counts[pair[0]] += frequency
        letter_counts[pair[1]] += frequency

    # "double count" the first and last letters by adding one to each
    letter_counts[sequence[0]] += 1
    letter_counts[sequence[-1]] += 1

    # Divide by 2 since we double counted before
    return int((max(letter_counts.values()) - min(letter_counts.values())) / 2)


def run_tests():
    test_inputs = """
    NNCB

    CH -> B
    HH -> N
    CB -> H
    NH -> C
    HB -> C
    HC -> B
    HN -> C
    NN -> C
    BH -> H
    NC -> B
    NB -> B
    BN -> B
    BB -> N
    BC -> B
    CC -> N
    CN -> C
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 1588:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 2188189693529:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(14)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
