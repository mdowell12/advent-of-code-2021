from solutions.get_inputs import read_inputs


SEGS_COUNT_TO_NUMS = {
    2: [1],
    3: [7],
    4: [4],
    5: [2, 3, 5],
    6: [0, 6, 9],
    7: [8],
}


def run_1(inputs):
    entries = _parse_input(inputs)
    num_with_unique = 0
    for _, output in entries:
        for segment in output:
            nums_with_len = SEGS_COUNT_TO_NUMS[len(segment)]
            if len(nums_with_len) == 1:
                num_with_unique += 1
    return num_with_unique


def run_2(inputs):
    entries = _parse_input(inputs)
    return sum(_line_total(pattern, output) for pattern, output in entries)


def _line_total(pattern, output):
    num_to_signal = _get_num_to_signal(pattern)
    signal_to_num = {''.join(sorted(v)): k for k, v in num_to_signal.items()}
    sequence = ''.join(str(signal_to_num[''.join(sorted(i))]) for i in output)
    result = int(sequence)
    # print(f"{output} {signal_to_num} {sequence} {result}")
    return result


def _get_num_to_signal(pattern):
    result = {}

    # Find the unique lengthed numbers
    for signal in pattern:
        nums_with_this_len = SEGS_COUNT_TO_NUMS[len(signal)]
        if len(nums_with_this_len) == 1:
            result[nums_with_this_len[0]] = signal

    right_side = [i for i in result[1]]
    # Parts of 4 that are not in 1
    four_lefts = [i for i in result[4] if i not in right_side]

    # Find 3
    for p in pattern:
        if len(p) == 5:
            if all(i in p for i in right_side):
                result[3] = p
    # Find 6
    for p in pattern:
        if len(p) == 6:
            if any(i not in p for i in right_side):
                result[6] = p

    # Find 0
    for p in pattern:
        if len(p) == 6:
            if any(i not in p for i in four_lefts):
                result[0] = p

    # Find 9
    for p in pattern:
        if len(p) == 6 and p not in result.values():
            result[9] = p

    # Find 2
    for p in pattern:
        if len(p) == 5 and p not in result.values():
            if any(i not in p for i in four_lefts):
                result[2] = p

    # Finally we have 5
    for p in pattern:
        if p not in result.values():
            if len(p) != 5:
                raise Exception()
            result[5] = p

    if len(result) != 10:
        raise Exception(f"Invalid result {result}")

    if len(set(result.values())) != 10:
        raise Exception(f"Invalid num values in result {result}")

    return result


def _parse_input(inputs):
    result = []
    for line in inputs:
        pattern = tuple(i for i in line.strip().split(' | ')[0].split(' '))
        output = tuple(i for i in line.strip().split(' | ')[1].split(' '))
        result.append((pattern, output))
    return result


def run_tests():
    test_inputs = """
    be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
    edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
    fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
    fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
    aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
    fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
    dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
    bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
    egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
    gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 26:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 61229:
        raise Exception(f"Test 2 did not pass, got {result_2}")

    smaller_input = ["acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"]
    result_3 = run_2(smaller_input)
    if result_3 != 5353:
        raise Exception(f"Test 3 did not pass, got {result_3}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(8)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
