from copy import deepcopy
from itertools import permutations, combinations
import json
from math import ceil
from math import floor

from solutions.get_inputs import read_inputs


def run_1(inputs):
    numbers = [_parse_line(i) for i in inputs]
    summed = _get_sum(numbers)
    return _magnitude(summed)


def run_2(inputs):
    numbers = [_parse_line(i) for i in inputs]
    maximum = None
    for pair in combinations(numbers, 2):
        summed = _get_sum(deepcopy(pair))
        mag = _magnitude(summed)
        if maximum is None or mag > maximum:
            maximum = mag

        # Not commutative so try the other direction too
        reverse_pair = deepcopy([pair[1], pair[0]])
        summed = _get_sum(reverse_pair)
        mag = _magnitude(summed)
        if maximum is None or mag > maximum:
            maximum = mag

    return maximum



def _parse_line(line):
    return json.loads(line)


def _get_sum(numbers):
    result = numbers[0]
    result = _reduce(result)
    for number in numbers[1:]:
        added = _add(result, number)
        result = _reduce(added)
    return result


def _add(pair_left, pair_right):
    return [pair_left, pair_right]


def _reduce(pairs, depth=0):
    # print("reducing ", pairs)
    result = pairs
    while True:
        before = result
        result, a, b, did_explode = _explode(result, depth=depth)
        # print(result)
        if did_explode:
            continue
        result, changed = _split(result)
        # print(result)
        # print()
        if before == result:
            break
    # print("finished ", result, " \n\n\n")
    return result


def _split(pairs):
    if isinstance(pairs, int):
        if pairs < 10:
            return pairs, False
        else:
            return _split_num(pairs), True
    else:
        left, changed_left = _split(pairs[0])
        if not changed_left:
            right, changed_right = _split(pairs[1])
        else:
            right, changed_right = pairs[1], False
        return [left, right], (changed_left or changed_right)


'''
always a right remaining and a left remaining after an exploded pair
we care which side of an outer pair an exploded pair came from
after the explosion, we can always immediately increment the *other* side of the pair
going further outwards, we should continue trying to increment something on the exploded side

'''
def _try_adding_right(right, amount):
    if isinstance(right, int):
        return right + amount, None
    new_right, amount = _try_adding_right(right[0], amount)
    right[0] = new_right
    return right, amount


def _try_adding_left(left, amount):
    if isinstance(left, int):
        return left + amount, None
    new_left, amount = _try_adding_left(left[1], amount)
    left[1] = new_left
    return left, amount


def _explode(pairs, depth=0, did_explode=False):
    # print(depth, '     '*depth, pairs)
    if isinstance(pairs, int):
        return pairs, None, None, did_explode
    elif depth == 4:
        if not (isinstance(pairs[0], int) and isinstance(pairs[1], int)):
            import pdb; pdb.set_trace()
            raise Exception("Too deep baby ", pairs)
        # print("exploding ", pairs)
        return 0, pairs[0], pairs[1], True
    else:
        left, add_left_1, add_right_1, did_explode = _explode(pairs[0], depth=depth+1, did_explode=did_explode)
        if not did_explode:
            right, add_left_2, add_right_2, did_explode = _explode(pairs[1], depth=depth+1, did_explode=did_explode)
        else:
            right, add_left_2, add_right_2 = pairs[1], None, None

        add_left_remaining = None
        add_right_remaining = None

        if add_right_1 is not None:
            # came_from_left_and_needs_to_go_right
            right, add_right_remaining = _try_adding_right(right, add_right_1)
        if add_left_1 is not None:
            # came_from_left_and_needs_to_go_left
            # Since came from left, do not modify left, wait until higher level
            add_left_remaining = add_left_1
        if add_right_2 is not None:
            # came_from_right_and_needs_to_go_right
            # Since came from right, do not modify right, wait until higher level
            add_right_remaining = add_right_2
        if add_left_2 is not None:
            # came_from_right_and_needs_to_go_left
            left, add_left_remaining = _try_adding_left(left, add_left_2)

        return [left, right], add_left_remaining, add_right_remaining, did_explode


def _split_num(number):
    # print("splitting ", number)
    left = floor(number / 2)
    right = ceil(number / 2)
    return [left, right]


def _magnitude(pairs):
    if isinstance(pairs[0], int):
        mag_left = pairs[0]
    else:
        mag_left = _magnitude(pairs[0])

    if isinstance(pairs[1], int):
        mag_right = pairs[1]
    else:
        mag_right = _magnitude(pairs[1])

    return 3 * mag_left + 2 * mag_right


def run_tests():

    if (result := _try_adding_right([1,1], 7)) != ([8,1], None):
        raise Exception(result)

    if (result := _try_adding_right([[1,1], 1], 7)) != ([[8,1],1], None):
        raise Exception(result)

    if (result := _try_adding_left([[1,1], 1], 7)) != ([[1,1],8], None):
        raise Exception(result)

    if (result := _add([1,2],[[3,4],5])) != [[1,2],[[3,4],5]]:
        raise Exception(result)

    if (result := _magnitude([[1,2],[[3,4],5]])) != 143:
        raise Exception(result)

    if (result := _magnitude([[[[0,7],4],[[7,8],[6,0]]],[8,1]])) != 1384:
        raise Exception(result)

    if (result := _magnitude([[[[1,1],[2,2]],[3,3]],[4,4]])) != 445:
        raise Exception(result)

    if (result := _magnitude([[[[3,0],[5,3]],[4,4]],[5,5]])) != 791:
        raise Exception(result)

    if (result := _magnitude([[[[5,0],[7,4]],[5,5]],[6,6]])) != 1137:
        raise Exception(result)

    if (result := _magnitude([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]])) != 3488:
        raise Exception(result)

    if (result := _explode([1,4])) != ([1,4], None, None, False):
        raise Exception(result)
    #
    if (result := _explode([[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]])[0]) != [[[[0,7],4],[[7,8],[6,0]]],[8,1]]:
        raise Exception(result)

    if (result := _split([4,10])) != ([4,[5,5]], True):
        raise Exception(result)

    if (result := _split([11,4])) != ([[5,6],4], True):
        raise Exception(result)

    if (result := _split([11,11])) != ([[5,6],11], True):
        raise Exception(result)

    if (result := _reduce([[[[[9,8],1],2],3],4])) != [[[[0,9],2],3],4]:
        raise Exception(result)

    if (result := _reduce([7,[6,[5,[4,[3,2]]]]])) != [7,[6,[5,[7,0]]]]:
        raise Exception(result)

    if (result := _reduce([[6,[5,[4,[3,2]]]],1])) != [[6,[5,[7,0]]],3]:
        raise Exception(result)

    if (result := _reduce([[6,[5,[4,[3,2]]]],1])) != [[6,[5,[7,0]]],3]:
        raise Exception(result)

    if (result := _reduce([[[[[4,3],4],4],[7,[[8,4],9]]], [1,1]])) != [[[[0,7],4],[[7,8],[6,0]]],[8,1]]:
        raise Exception(result)

    if (result := _get_sum([[1,1],[2,2],[3,3],[4,4]])) != [[[[1,1],[2,2]],[3,3]],[4,4]]:
        raise Exception(result)

    test = [json.loads(i) for i in """
    [1,1]
    [2,2]
    [3,3]
    [4,4]
    """.strip().split('\n')]
    if (result := _get_sum(test)) != [[[[1,1],[2,2]],[3,3]],[4,4]]:
        raise Exception(result)

    test = [json.loads(i) for i in """
    [1,1]
    [2,2]
    [3,3]
    [4,4]
    [5,5]
    """.strip().split('\n')]
    if (result := _get_sum(test)) != [[[[3,0],[5,3]],[4,4]],[5,5]]:
        raise Exception(result)

    test = [json.loads(i) for i in """
    [1,1]
    [2,2]
    [3,3]
    [4,4]
    [5,5]
    [6,6]
    """.strip().split('\n')]
    if (result := _get_sum(test)) != [[[[5,0],[7,4]],[5,5]],[6,6]]:
        raise Exception(result)

    test = [json.loads(i) for i in """
    [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]
    [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
    """.strip().split('\n')]
    if (result := _get_sum(test)) != [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]:
        raise Exception(result)

    test = [json.loads(i) for i in """
    [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
    [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
    """.strip().split('\n')]
    if (result := _get_sum(test)) != [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]:
        raise Exception(result)

    test = [json.loads(i) for i in """
    [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
    [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
    [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
    [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
    [7,[5,[[3,8],[1,4]]]]
    [[2,[2,2]],[8,[8,1]]]
    [2,9]
    [1,[[[9,3],9],[[9,0],[0,7]]]]
    [[[5,[7,4]],7],1]
    [[[[4,2],2],6],[8,7]]
    """.strip().split('\n')]
    if (result := _get_sum(test)) != [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]:
        raise Exception(result)

    test_inputs = """
    [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
    [[[5,[2,8]],4],[5,[[9,9],0]]]
    [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
    [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
    [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
    [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
    [[[[5,4],[7,7]],8],[[8,3],8]]
    [[9,3],[[9,9],[6,[4,9]]]]
    [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
    [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 4140:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 3993:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(18)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
