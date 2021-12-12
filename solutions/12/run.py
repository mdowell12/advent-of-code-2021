from collections import Counter, defaultdict

from solutions.get_inputs import read_inputs


def run_1(inputs):
    connections = defaultdict(lambda: set())
    for line in inputs:
        left = Cave(line.strip().split('-')[0])
        right = Cave(line.strip().split('-')[1])
        connections[left].add(right)
        connections[right].add(left)
    all_paths = _get_paths_to_end(Cave('start'), connections, _small_cave_used_fn_1)
    return len(all_paths)


def _get_paths_to_end(from_cave, connections, small_cave_used_fn, acc=None):
    if acc is None:
        acc = []
    acc.append(from_cave)

    result = []

    for to_cave in connections[from_cave]:
        if to_cave.is_end():
            result.append(acc + [to_cave])
        elif to_cave.is_start():
            continue
        elif to_cave.is_small() and small_cave_used_fn(to_cave, acc):
            continue
        else:
            paths = _get_paths_to_end(to_cave, connections, small_cave_used_fn, [i for i in acc])
            result += paths
    return result


def _small_cave_used_fn_1(to_cave, acc):
    return to_cave in acc


def _small_cave_used_fn_2(to_cave, acc):
    cave_counts = Counter(acc)
    if cave_counts[to_cave] == 0:
        return False
    elif any(k.is_small() and v > 1 for k, v in cave_counts.items()):
        return True
    else:
        return False


def run_2(inputs):
    connections = defaultdict(lambda: set())
    for line in inputs:
        left = Cave(line.strip().split('-')[0])
        right = Cave(line.strip().split('-')[1])
        connections[left].add(right)
        connections[right].add(left)
    all_paths = _get_paths_to_end(Cave('start'), connections, _small_cave_used_fn_2)
    print('\n'.join(sorted(' '.join(p.name for p in path) for path in all_paths)))
    return len(all_paths)


class Cave:

    def __init__(self, name):
        self.name = name.strip()

    def is_start(self):
        return self.name == 'start'

    def is_end(self):
        return self.name == 'end'

    def is_big(self):
        return not self.is_start() and not self.is_end() and self.name[0].isupper()

    def is_small(self):
        return not self.is_start() and not self.is_end() and self.name[0].islower()

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, Cave):
            return self.name == other.name
        return NotImplemented


def run_tests():
    test_inputs = """
    start-A
    start-b
    A-c
    A-b
    b-d
    A-end
    b-end
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 10:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    test_inputs_2 = """
    dc-end
    HN-start
    start-kj
    dc-start
    dc-HN
    LN-dc
    HN-end
    kj-sa
    kj-HN
    kj-dc
    """.strip().split('\n')

    result_1_2 = run_1(test_inputs_2)
    if result_1_2 != 19:
        raise Exception(f"Test 1.2 did not pass, got {result_1_2}")

    test_inputs_3 = """
    fs-end
    he-DX
    fs-he
    start-DX
    pj-DX
    end-zg
    zg-sl
    zg-pj
    pj-he
    RW-he
    fs-DX
    pj-RW
    zg-RW
    start-pj
    he-WI
    zg-he
    pj-fs
    start-RW
    """.strip().split('\n')

    result_1_3 = run_1(test_inputs_3)
    if result_1_3 != 226:
        raise Exception(f"Test 1.3 did not pass, got {result_1_2}")

    result_2 = run_2(test_inputs)
    if result_2 != 36:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(12)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
