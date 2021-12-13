from solutions.get_inputs import read_inputs


def run_1(inputs):
    points, folds = _parse_inputs(inputs)
    fold = folds[0]
    points = _do_fold(points, fold)
    return len(points)


def run_2(inputs):
    points, folds = _parse_inputs(inputs)
    for fold in folds:
        points = _do_fold(points, fold)
    _print_grid(points)


def _parse_inputs(inputs):
    points = set()
    folds = []
    for line in [i.strip() for i in inputs]:
        if not line:
            continue
        if 'fold' in line:
            is_vert = 'x' in line
            val = int(line.split('=')[-1])
            folds.append((val, is_vert))
        else:
            parts = line.split(',')
            points.add((int(parts[0]), int(parts[1])))
    return points, folds


def _do_fold(points, fold):
    fold_line, is_vert = fold
    new_points = set()
    for x, y in points:
        mover = x if is_vert else y
        if mover > fold_line:
            distance = mover - fold_line
            new_value = mover - 2 * distance
            new_point = (new_value, y) if is_vert else (x, new_value)
            new_points.add(new_point)
        else:
            new_points.add((x, y))
    return new_points


def _print_grid(points):
    max_x = max(i[0] for i in points)
    max_y = max(i[1] for i in points)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) in points:
                print('\033[1;31m' + 'X', end=' ')
            else:
                print("\033[0;0m" + ' ', end=' ')
        print()


def run_tests():
    test_inputs = """
    6,10
    0,14
    9,10
    0,3
    10,4
    4,11
    6,0
    6,12
    4,1
    0,13
    10,12
    3,4
    3,0
    8,4
    1,10
    2,14
    8,10
    9,0

    fold along y=7
    fold along x=5
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 17:
        raise Exception(f"Test 1 did not pass, got {result_1}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(13)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
