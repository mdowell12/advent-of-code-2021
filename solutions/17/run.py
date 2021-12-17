from solutions.get_inputs import read_inputs

# p_x(t) = p_x(t-1) + v_x(t)
# v_x(t) = max(v_x(t-1) - 1, 0)
# v_y(t) = v_y(t-1) - 1
# Initial v_x must be less than max x of target otherwise guaranteed to overshoot
# Initial v_y must be at least min y of target otherwise guaranteed to undershoot
# Must have positive x else will not move forward ever


def run(inputs):
    target_area = _parse_input(inputs)
    return _find_hits(target_area)


def _find_hits(target_area):
    x, y = target_area
    min_x, max_x = x
    min_y, max_y = y

    highest_point = 0
    num_hits = 0
    for v_x in range(1, max_x + 1):
        print(v_x, target_area)
        hits, highest = _find_hits_for_vx(v_x, min_x, max_x, min_y, max_y)
        print(hits)
        num_hits += len(hits)
        if highest and highest > highest_point:
            highest_point = highest
    return highest_point, num_hits


def _find_hits_for_vx(v_x, min_x, max_x, min_y, max_y):
    highest = None
    hits = []
    v_y = min_y
    while True:
        # get sequence of points that goes until y less than min y and x gt max x
        sequence, hit, highest_y = _get_sequence(v_x, v_y, min_x, max_x, min_y, max_y)
        # if hit, check highest and record
        if hit:
            hits.append((v_x, v_y))
            if highest is None or highest_y > highest:
                highest = highest_y
        # if no x reached min x, break
        if not _should_try_next_y(sequence, min_x, max_x, max_y, v_y):
            break
        # increase y
        v_y += 1
    return hits, highest


def _should_try_next_y(sequence, min_x, max_x, max_y, v_y):
    # This is dumb but works for the inputs
    return v_y < 1000


def _get_sequence(v_x, v_y, min_x, max_x, min_y, max_y):
    x, y = (0, 0)
    sequence = [(x, y)]
    highest = 0
    hit = False
    while x <= max_x and (v_y > 0 or y > min_y):
        x += v_x
        y += v_y
        if y > highest:
            highest = y
        sequence.append((x, y))
        if x >= min_x and x <= max_x and y >= min_y and y <= max_y:
            hit = True
            break
        v_x = max(v_x - 1, 0)
        v_y -= 1
    return sequence, hit, highest


def _parse_input(inputs):
    line = inputs[0]
    x_range = line.split('x=')[1].split(',')[0]
    x = (int(x_range.split('..')[0]), int(x_range.split('..')[1]))
    y = (int(line.split('y=')[1].split('..')[0]), int(line.split('y=')[1].split('..')[1]))
    return (x, y)


def run_tests():
    test_inputs = """
    target area: x=20..30, y=-10..-5
    """.strip().split('\n')

    sequence, hit, highest = _get_sequence(7, 2, 20, 30, -10, -5)
    if not hit or highest != 3:
        raise Exception()

    sequence, hit, highest = _get_sequence(6, 3, 20, 30, -10, -5)
    if not hit or highest != 6:
        raise Exception()

    sequence, hit, highest = _get_sequence(9, 0, 20, 30, -10, -5)
    if not hit or highest != 0:
        raise Exception()

    sequence, hit, highest = _get_sequence(17, -4, 20, 30, -10, -5)
    if hit:
        raise Exception()

    _, highest = _find_hits_for_vx(6, 20, 30, -10, -5)
    if highest != 45:
        raise Exception()

    highest, num_hits = run(test_inputs)
    if highest != 45:
        raise Exception(f"Test 1 did not pass, got {highest}")
    if num_hits != 112:
        raise Exception(f"Test 2 did not pass, got {num_hits}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(17)

    highest, num_hits = run(input)
    print(f"Finished 1 with result {highest}")
    print(f"Finished 2 with result {num_hits}")
