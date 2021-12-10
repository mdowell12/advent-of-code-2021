from collections import deque

from solutions.get_inputs import read_inputs


SCORES = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

SCORES_COMPLETION = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

LEFT_TO_RIGHT = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

RIGHT_TO_LEFT = {v: k for k, v in LEFT_TO_RIGHT.items()}


def run_1(inputs):
    scores = []
    for line in inputs:
        error = _find_syntax_error(line.strip())
        if error is not None:
            scores.append(SCORES[error])
    return sum(scores)


def run_2(inputs):
    scores = []
    for line in inputs:
        if _find_syntax_error(line.strip()) is not None:
            continue
        completion = _find_completion(line.strip())
        score = _score_completion(completion)
        print(f'{line.strip()} score {score}')
        scores.append(score)
    return sorted(scores)[int(len(scores) / 2 - 0.5)]


def _find_syntax_error(line):
    stack = deque()
    for c in line:
        if c in LEFT_TO_RIGHT:
            stack.append(c)
        else:
            val = stack.pop()
            if val != RIGHT_TO_LEFT[c]:
                print(f'expected {LEFT_TO_RIGHT[val]} got {c}')
                return c
    print(f'No error for line {line}')
    return None


def _find_completion(line):
    stack = deque()
    for c in line:
        if c in LEFT_TO_RIGHT:
            stack.append(c)
        else:
            if not stack:
                import pdb; pdb.set_trace()
            val = stack.pop()

    result = []
    while stack:
        val = stack.pop()
        if val in LEFT_TO_RIGHT:
            result.append(LEFT_TO_RIGHT[val])
        else:
            stack.append(val)
    return result


def _score_completion(completion):
    result = 0
    for c in completion:
        result *= 5
        result += SCORES_COMPLETION[c]
    return result


def run_tests():
    test_inputs = """
    [({(<(())[]>[[{[]{<()<>>
    [(()[<>])]({[<{<<[]>>(
    {([(<{}[<>[]}>{[]{[(<()>
    (((({<>}<{<{<>}{[]{[]{}
    [[<[([]))<([[{}[[()]]]
    [{[{({}]{}}([{[{{{}}([]
    {<[[]]>}<{[{[{[]{()[[[]
    [<(<(<(<{}))><([]([]()
    <{([([[(<>()){}]>(<<{{
    <{([{{}}[<[[[<>{}]]]>[]]
    """.strip().split('\n')

    _find_syntax_error('()')
    _find_syntax_error('(((()))')
    _find_syntax_error('()[]')
    _find_syntax_error('(]')

    result_1 = run_1(test_inputs)
    if result_1 != 26397:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 288957:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(10)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    print(_find_completion('[({(<(())[]>[[{[]{<()<>>'))

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
