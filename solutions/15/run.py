from solutions.get_inputs import read_inputs


def run_1(inputs):
    points = _parse_inputs(inputs)
    max_x = len(inputs[0]) - 1
    max_y = len(inputs) - 1
    _print_grid(points, max_x, max_y)
    return _find_best_path(points, (0, 0), max_x, max_y)


def run_2(inputs):
    pass

# def _find_best_path(points,
#                     curr_point,
#                     max_x,
#                     max_y):
#     queue = {curr_point,}
#     cache = {}
#     import pdb; pdb.set_trace()
#     while queue:
#         x, y = queue.pop()
#         if (x,y) in cache:
#             continue
#         nexts = [
#             (x + 1, y),
#             (x, y + 1),
#             (x - 1, y),
#             (x, y - 1),
#         ]
#         min_value = None
#         for next_x, next_y in nexts:
#             if (next_x, next_y) in cache:
#                 if min_value is None or points[(next_x, next_y)] + cache[(next_x, next_y)] < min_value:
#                     min_value = points[(next_x, next_y)] + cache[(next_x, next_y)]
#                 continue
#             if next_x < 0 or next_x > max_x or next_y < 0 or next_y > max_y:
#                 continue
#             elif next_x == max_x and next_y == max_y:
#                 import pdb; pdb.set_trace()
#                 cache[(next_x, next_y)] = points[(next_x, next_y)]
#                 continue
#             else:
#                 # queue.append((next_x, next_y))
#                 queue.add((next_x, next_y))
#     return cache[curr_point]

def _find_best_path(points,
                    curr_point,
                    max_x,
                    max_y):
    cache = {(max_x, max_y): points[(max_x, max_y)]}
    i = 0
    while (0,0) not in cache:
        for x in range(max_x + 1):
            for y in range(max_y + 1):
                nexts = [
                    (x + 1, y),
                    (x, y + 1),
                    (x - 1, y),
                    (x, y - 1),
                ]
                results = []
                for next_x, next_y in nexts:
                    if (next_x, next_y) in cache:
                        results.append(cache[(next_x, next_y)] + points[(x,y)])
                    elif next_x < 0 or next_x > max_x or next_y < 0 or next_y > max_y:
                        continue
                if results:
                    cache[(x, y)] = min(results)
        # import pdb; pdb.set_trace()
        i += 1
        print(cache)
        if len(points) > 100 and i < 5:
            import pdb; pdb.set_trace()
    return cache[(0,0)] - points[(0,0)]


# def _find_best_path(points,
#                     curr_point,
#                     max_x,
#                     max_y,
#                     path=None,
#                     cache=None):
#     # print(f'path {path}')
#     if path is None:
#         # path = set()
#         path = []
#     if cache is None:
#         cache = {}
#     curr_x, curr_y = curr_point
#     # print(curr_x, curr_y)
#     if curr_x==8 and curr_y == 8:
#         import pdb; pdb.set_trace()
#     # if curr_x==9 and curr_y == 8:
#     #     import pdb; pdb.set_trace()
#     # path.add((curr_x,curr_y))
#     path.append((curr_x,curr_y))
#     nexts = [
#         (curr_x + 1, curr_y),
#         (curr_x, curr_y + 1),
#         (curr_x - 1, curr_y),
#         (curr_x, curr_y - 1),
#     ]
#     min_point = None
#     min_value = None
#
#     for x, y in nexts:
#         if (x, y) in path:
#             continue
#         if (x, y) in cache:
#             print(path)
#             if min_value is None or cache[(x,y)] < min_value:
#                 min_value = cache[(x,y)]
#                 min_point = (x,y)
#             # results.append(cache[(x,y)])
#             continue
#         if x == max_x and y == max_y:
#             # import pdb; pdb.set_trace()
#             print(path)
#             return points[(x, y)]
#         elif x < 0 or x > max_x or y < 0 or y > max_y:
#             continue
#         else:
#             new_path = [i for i in path]
#             best = _find_best_path(points, (x,y), max_x, max_y, cache=cache, path=new_path)
#             if best is None:
#                 continue
#             from_here = best + points[(x,y)]
#             if max_x - x < 5 and max_y - y < 5:
#                 print(f'best from ({x}, {y}) is {best}')
#             cache[(x,y)] = from_here
#             if min_value is None or from_here < min_value:
#                 min_value = from_here
#                 min_point = (x,y)
#             # results.append(from_here)
#     # print(f'From {curr_point} found results {results}')
#     # return min(results)
#     # path.add(min_point)
#     # if min_value is None:
#         # import pdb; pdb.set_trace()
#     return min_value



def _parse_inputs(inputs):
    result = {}
    for y, line in enumerate(inputs):
        for x, val in enumerate(line.strip()):
            result[(x,y)] = int(val)
    return result


def _print_grid(points, max_x, max_y):
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print(points[(x,y)], end=' ')
        print()


def run_tests():
    test_inputs = """
    1163751742
    1381373672
    2136511328
    3694931569
    7463417111
    1319128137
    1359912421
    3125421639
    1293138521
    2311944581
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 40:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    # result_2 = run_2(test_inputs)
    # if result_2 != 0:
    #     raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(15)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")
    # 394 is too high

    # result_2 = run_2(input)
    # print(f"Finished 2 with result {result_2}")
