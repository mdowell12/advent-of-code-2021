import json
from math import ceil
from math import floor

from solutions.get_inputs import read_inputs


def run_1(inputs):
    numbers = [_parse_line(i) for i in inputs]
    import pdb; pdb.set_trace()
    summed = _get_sum(numbers)

    return _magnitude(summed)


def run_2(inputs):
    pass


def _parse_line(line):
    return json.loads(line)


def _get_sum(numbers):
    import pdb; pdb.set_trace()
    result = numbers[0]
    for number in numbers[1:]:
        added = _add(result, number)
        result, _, _ = _reduce(added)
    return result


def _add(pair_left, pair_right):
    return [pair_left, pair_right]


def _reduce(pairs, depth=0):
    import pdb; pdb.set_trace()
    result = pairs
    while True:
        before = result
        result, _, _ = _explode(result, depth=depth)
        result, changed = _split(result)
        if before == result:
            break
    return result


def _split(pairs):
    if isinstance(pairs, int):
        if pairs < 10:
            return pairs, False
        else:
            return _split_num(pairs), True
    else:
        left, changed_left = _split(pairs[0])
        right, changed_right = _split(pairs[1])
        return [left, right], (changed_left or changed_right)


def _explode(pairs, depth=0):
    # print('   '*depth, pairs)
    if isinstance(pairs, int):
        return pairs, None, None, None
        # if pairs < 10:
        #     return pairs, None, None
        # else:
        #     return _split(pairs), None, None
    elif depth == 4:
        import pdb; pdb.set_trace()
        return 0, pairs[0], pairs[1], 32
    else:
        left, add_left_1, add_right_1, from_i_1 = _explode(pairs[0], depth=depth+1)
        right, add_left_2, add_right_2, from_i_2 = _explode(pairs[1], depth=depth+1)
        # left, add_left_1, add_right_1 = _reduce(pairs[0], depth=depth+1)
        # right, add_left_2, add_right_2 = _reduce(pairs[1], depth=depth+1)

        if depth == 0:
            import pdb; pdb.set_trace()
        result = [left, right]
        result, add_left_remaining, add_right_remaining = _distribute_remaining(result, add_left_1, add_right_1, from_i_1)
        result, add_left_remaining, add_right_remaining = _distribute_remaining(result, add_left_2, add_right_2, from_i_2)


        # add_left_remaining = None
        # if add_left_1:
        #     print('   l1'*depth, add_left_1, pairs[0], left)
        #     if isinstance(pairs[0], int):
        #         left += add_left_1
        #     else:
        #         add_left_remaining = add_left_1
        # elif add_left_2:
        #     print('   l2'*depth, add_left_2, pairs[0], left)
        #     if isinstance(pairs[0], int):
        #         left += add_left_2
        #     else:
        #         add_left_remaining = add_left_2
        #
        # add_right_remaining = None
        # if add_right_1:
        #     print('   r1'*depth, add_right_1, pairs[1], right)
        #     # import pdb; pdb.set_trace()
        #     if isinstance(pairs[1], int):
        #         right += add_right_1
        #     else:
        #         add_right_remaining = add_right_1
        # elif add_right_2:
        #     # import pdb; pdb.set_trace()
        #     print('   r2'*depth, add_right_2, pairs[1], right)
        #     if isinstance(pairs[1], int):
        #         right += add_right_2
        #     else:
        #         add_right_remaining = add_right_2
        # result = [left, right]
        from_i = None
        if add_left_1 or add_right_1:
            from_i = from_i_1
        elif add_left_2 or add_right_2:
            from_i = from_i_2

        print('   '*depth, result, add_left_remaining, add_right_remaining, from_i)
        return result, add_left_remaining, add_right_remaining, from_i

def _distribute_remaining(pairs, add_left, add_right, from_i):
    pair_string = json.dumps(pairs)
    if add_left:
        i = from_i
        while i < len(pair_string):
            if pair_string[i].isdigit():
                val = int(pair_string[i]) + add_left
                pair_string = pair_string[:i] + str(val) + pair_string[i+1:]
                add_left = None
                break
            else:
                i+=1

    if add_right:
        i = from_i
        while i >= 0:
            if pair_string[i].isdigit():
                val = int(pair_string[i]) + add_right
                pair_string = pair_string[:i] + str(val) + pair_string[i+1:]
                add_right = None
                break
            else:
                i+=1
    return json.loads(pair_string), add_left, add_right


def _split_num(number):
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

    # if (result := _explode([1,4])) != ([1,4], None, None):
    #     raise Exception(result)
    #
    # if (result := _explode([[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]])[0]) != [[[[0,7],4],[[7,8],[6,0]]],[8,1]]:
    #     raise Exception(result)

    if (result := _split([4,10])) != ([4,[5,5]], True):
        raise Exception(result)

    if (result := _split([11,4])) != ([[5,6],4], True):
        raise Exception(result)

    # if (result := _reduce([[[[[9,8],1],2],3],4])) != [[[[0,9],2],3],4]:
    #     raise Exception(result)
    #
    # if (result := _reduce([7,[6,[5,[4,[3,2]]]]])) != [7,[6,[5,[7,0]]]]:
    #     raise Exception(result)
    #
    # if (result := _reduce([[6,[5,[4,[3,2]]]],1])) != [[6,[5,[7,0]]],3]:
    #     raise Exception(result)

    if (result := _reduce([[[[[4,3],4],4],[7,[[8,4],9]]], [1,1]])) != [[[[0,7],4],[[7,8],[6,0]]],[8,1]]:
        raise Exception(result)

    if (result := _get_sum([[1,1],[2,2],[3,3],[4,4]])) != [[[[1,1],[2,2]],[3,3]],[4,4]]:
        raise Exception(result)

    # if (result := _reduce([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]])[0]) != [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]:
    #     raise Exception(result)

    # if (result := _reduce([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]])[0]) != [[3,[2,[8,0]]],[9,[5,[7,0]]]]:
    #     raise Exception(result)

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

    # result_2 = run_2(test_inputs)
    # if result_2 != 0:
    #     raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(18)

    # result_1 = run_1(input)
    # print(f"Finished 1 with result {result_1}")

    # result_2 = run_2(input)
    # print(f"Finished 2 with result {result_2}")
