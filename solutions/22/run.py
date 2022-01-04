from collections import defaultdict
from time import time

from solutions.get_inputs import read_inputs


debug = False


CUBOIDS_FOR_SLICE_CACHE = {}


def run_1(inputs):
    commands = [_parse_line(line) for line in inputs]
    commands = [c for c in commands if c[1][0] >= -50 and c[1][1] <= 50]
    return _run(commands)


def run_2(inputs):
    commands = [_parse_line(line) for line in inputs]
    return _run(commands)


def _get_points_for_interval(values):
    values = sorted(set(values))
    result = values
    result.append(result[-1]+1)
    return result


def _get_intervals_from_values(values):
    paired = sorted([(i, i) for i in values], key=lambda x: x[0])
    result = []
    for i in range(len(paired) - 1):
        pair = paired[i]
        next_pair = paired[i+1]
        result.append(pair)
        if pair[0] + 1 < next_pair[0]:
            result.append((pair[0] + 1, next_pair[0] - 1))
    result.append(paired[-1])
    return result


def _run(commands):
    x_values = []
    y_values = []
    for is_on, (x1, x2), (y1, y2), (z1, z2) in commands:
        x_values.append(x1)
        x_values.append(x2)
        y_values.append(y1)
        y_values.append(y2)
    x_values = _get_points_for_interval(x_values)
    y_values = _get_points_for_interval(y_values)

    x_intervals = _get_intervals_from_values(x_values)
    y_intervals = _get_intervals_from_values(y_values)
    # import pdb; pdb.set_trace()

    cuboids = []
    # import pdb; pdb.set_trace()
    # for i in range(len(x_values) - 1):
    #     for j in range(len(y_values) - 1):
    #         x1, x2 = x_values[i], x_values[i+1] - 1
    #         y1, y2 = y_values[j], y_values[j+1] - 1
    for x1, x2 in x_intervals:
        for y1, y2 in y_intervals:
            if debug: print(f'{x1}..{x2} {y1}..{y2}')
            assert x1 <= x2
            assert y1 <= y2
            overlapping_commands = [c for c in commands if _is_valid_slice_for_command(x1,x2,y1,y2, c)]
            if _is_valid_slice(x1, x2, y1, y2, commands):
                cuboids_this_slice = _get_cuboids_for_slice(x1, x2, y1, y2, overlapping_commands)
                if debug: print(f'adding size {sum(c.size() for c in cuboids_this_slice)}')
                cuboids += cuboids_this_slice
                # if debug: print(f'cuboids {cuboids}')
            else:
                if debug: print(f'skipped slice {x1, x2, y1, y2}')

            if debug: print(f'total size {sum(c.size() for c in cuboids)}\n')
            # import pdb; pdb.set_trace()

    return sum(c.size() for c in cuboids)


"""
find and sort all x values regardless of position in interval
find and sort all y values regardless of position in interval
for each x,y rectangle, calculate z intervals (see below). Input to z intervals function are the z ranges of any
cuboid that shares at least one x AND at least one y value with this x,y rectangle plus whether the interval is an on or off.

# Separate function for calculating z intervals (remember must stay in order to preserve on/off ordering)
In this function iterate through chunks and make new chunks by combining.
    If any chunk does not overlap with the current chunk, make a new one and continue
    If this chunk is an "off" chunk, we should subtract its values from any other chunks we're keeping track of
sum list
"""

def _get_cuboids_for_slice(slice_x1, slice_x2, slice_y1, slice_y2, commands):

    intervals = []
    if debug: print(f"cuboids for slice {slice_x1, slice_x2, slice_y1, slice_y2}")

    for is_on, (x1, x2), (y1, y2), (z1, z2) in commands:
        if debug: print(f'\tcommand: {is_on, (x1, x2), (y1, y2), (z1, z2)} and intervals: {intervals}')

        if not (_does_overlap((slice_x1, slice_x2), (x1, x2)) and _does_overlap((slice_y1, slice_y2), (y1, y2))):
            if debug: print(f'\tno overlap for {x1}..{x2} {y1}..{y2}')
            continue

        if not is_on:
            new_intervals = []
            for interval in intervals:
                if _does_overlap(interval, (z1, z2)):
                    after_turn_off = _turn_off(interval, z1, z2)
                    if after_turn_off:
                        new_intervals += after_turn_off
                else:
                    new_intervals.append(interval)
            intervals = new_intervals
            if debug: print(f'\tOFF interval {z1}..{z2}. Intervals now: {intervals}')

        elif len(intervals) == 0:
            if is_on:
                if debug: print(f'\tfirst ON interval {x1}..{x1} {y1}..{y2}. Added {z1}..{z2}.')
                intervals.append([z1,z2])
            else:
                if debug: print(f'\tfirst interval, but OFF {x1}..{x1} {y1}..{y2}. Skipped.')

        elif len(intervals) == 1:
            if _does_overlap(intervals[0], (z1, z2)):
                if is_on:
                    intervals[0] = _turn_on(intervals[0], z1, z2)
                    if debug: print(f'\tON interval {z1}..{z2} overlapped. Intervals now: {intervals}')
                else:
                    raise Exception()
            else:
                if is_on:
                    intervals.append([z1,z2])
                    if debug: print(f'\tON interval {z1}..{z2} did not overlap. Intervals now: {intervals}')
                else:
                    raise Exception()

        # if len(intervals) > 2:
        #     import pdb; pdb.set_trace()
        else:
            for i in range(len(intervals) - 1):
                left = intervals[i]
                right = intervals[i+1]

                if _does_overlap(left, (z1, z2)):
                    if _does_overlap((z1, z2), right):
                        if is_on:
                            # stitch together
                            new = _turn_on(left, z1, z2)
                            new = _turn_on(right, new[0], new[1])
                            intervals[i] = new
                            del intervals[i+1]
                            if debug: print(f'\tON interval {z1}..{z2} overlapped with {left} and {right}. Intervals now: {intervals}')
                        else:
                            raise Exception()
                    else:
                        if is_on:
                            intervals[i] = _turn_on(left, z1, z2)
                            if debug: print(f'\tON interval {z1}..{z2} overlapped with {left} (left) but not {right} (right). Intervals now: {intervals}')
                        else:
                            raise Exception()
                    break
                else:
                    if _does_overlap((z1, z2), right):
                        if is_on:
                            intervals[i+1] = _turn_on(right, z1, z2)
                            if debug: print(f'\tON interval {z1}..{z2} overlapped with {right} (right) but not {left} (left). Intervals now: {intervals}')
                        else:
                            raise Exception()
                    break
            else:
                if is_on:
                    # if debug: import pdb; pdb.set_trace()
                    import pdb; pdb.set_trace()
                    intervals.append([z1,z2])
                    if debug: print(f'\tON interval {z1}..{z2} did not overlap any intervals, appending. Intervals now: {intervals}')
                else:
                    raise Exception()

        if intervals:
            intervals = sorted(intervals, key=lambda t: t[0])
            # intervals = [i for i in intervals if i[0] <= i[1]]
            intervals = _stitch_intervals(intervals)

        if debug: print(f'\tFinished with intervals {intervals}')
        if debug: print()

    if debug: print(f"final intervals {intervals}")

    cuboids = [Cuboid(slice_x1, slice_x2, slice_y1, slice_y2, z1, z2) for z1, z2 in intervals]

    return cuboids


def _stitch_intervals(intervals):
    """
    e.g. [[-50, -48], [-36, 18], [4, 44]] -> [[-50, -48], [-36, 44]]
    assumes intervals are sorted already
    """
    result = []
    result = [intervals[0]]
    for i in range(1, len(intervals)):
        left = intervals[i-1]
        right = intervals[i]
        if left[1] < right[0]:
            result.append(right)
        else:
            left[1] = max(right[1], left[1])
    return result


def _is_valid_slice(slice_x1, slice_x2, slice_y1, slice_y2, commands):
    midpoint = _midpoint(slice_x1, slice_x2, slice_y1, slice_y2)
    for _, x, y, _ in commands:
        if _does_overlap(x, (midpoint[0],midpoint[0])) and _does_overlap(y, (midpoint[1],midpoint[1])):
            return True
    return False

def _is_valid_slice_for_command(slice_x1, slice_x2, slice_y1, slice_y2, command):
    midpoint = _midpoint(slice_x1, slice_x2, slice_y1, slice_y2)
    _, x, y, _ = command
    return _does_overlap(x, (midpoint[0],midpoint[0])) and _does_overlap(y, (midpoint[1],midpoint[1]))


def _midpoint(slice_x1, slice_x2, slice_y1, slice_y2):
    x = int((slice_x1 + slice_x2) / 2)
    y = int((slice_y1 + slice_y2) / 2)
    return [x,y]


def _turn_off(left, z1, z2):
    assert left is not None
    assert z1 <= z2
    assert _does_overlap(left, (z1,z2))

    if z1 <= left[0] and z2 <= left[1]:
        return [[z2+1, left[1]]]
    elif z1 <= left[0] and z2 > left[1]:
        return None
    elif z1 > left[0] and z2 <= left[1]:
        return [[left[0], z1-1], [z2+1, left[1]]]
    else:
        return [[left[0], z1-1]]


def _turn_on(interval, z1, z2):
    assert _does_overlap(interval, (z1, z2))
    return [min(interval[0], z1), max(interval[1], z2)]


def _does_overlap(first, second):
    return (first[1] >= second[0] and first[0] <= second[0]) or \
     (first[0] <= second[1] and first[1] >= second[1]) or \
      (first[0] <= second[0] and first[1] >= second[1]) or \
      (first[0] >= second[0] and first[1] <= second[1])


def _do_command(command, grid):
    limit = 50
    is_on, (x1, x2), (y1, y2), (z1, z2) = command
    if x1 < -50 or x1 > 50:
        return grid
    x1, x2 = max(min(x1, limit), -limit), max(min(x2, limit), -limit)
    y1, y2 = max(min(y1, limit), -limit), max(min(y2, limit), -limit)
    z1, z2 = max(min(z1, limit), -limit), max(min(z2, limit), -limit)
    print(x1,x2)
    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            for z in range(z1, z2+1):
                grid[(x,y,z)] = is_on
    return grid


def _parse_line(line):
    line = line.strip()
    is_on = line.split(' ')[0].strip() == 'on'
    x,y,z = line.replace('on ', '').replace('off ', '').split(',')
    x1, x2 = map(int, x.replace('x=','').split('..'))
    y1, y2 = map(int, y.replace('y=','').split('..'))
    z1, z2 = map(int, z.replace('z=','').split('..'))
    return is_on, (x1,x2), (y1,y2), (z1,z2)


class Cuboid:

    def __init__(self, x1, x2, y1, y2, z1, z2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2

    def size(self):
        return (self.x2 - self.x1 + 1) * (self.y2 - self.y1 + 1) * (self.z2 - self.z1 + 1)

    def __repr__(self):
        return f'({self.x1}..{self.x2}),({self.y1}..{self.y2}),({self.z1}..{self.z2})'


def run_tests():
    # if (result := _does_overlap((0,5), (3,6))) != True:
    #     raise Exception(result)
    #
    # if (result := _does_overlap((6,10), (3,6))) != True:
    #     raise Exception(result)
    #
    # if (result := _does_overlap((0,5), (100,105))) != False:
    #     raise Exception(result)
    #
    # if (result := _does_overlap((-46, -41), (-4100, -4000))) != False:
    #     raise Exception(result)
    #
    # if (result := _does_overlap((10, 10), (9,11))) != True:
    #     raise Exception(result)
    #
    # if (result := _does_overlap((9,11), (10, 10))) != True:
    #     raise Exception(result)

    if (result := _stitch_intervals([[-50, -48], [-36, 18], [4, 44]])) != [[-50, -48], [-36, 44]]:
        raise Exception(result)

    if (result := _stitch_intervals([[-50, -48], [-36, 99], [4, 44]])) != [[-50, -48], [-36, 99]]:
        raise Exception(result)

    if (result := _stitch_intervals([[-50, -48], [4, 44]])) != [[-50, -48], [4, 44]]:
        raise Exception(result)

    if (result := _stitch_intervals([[-50, -48], [4, 44]])) != [[-50, -48], [4, 44]]:
        raise Exception(result)

    # test_inputs = """
    # on x=10..12,y=10..12,z=10..12
    # on x=11..13,y=11..13,z=11..13
    # off x=9..11,y=9..11,z=9..11
    # on x=10..10,y=10..10,z=10..10
    # """.strip().split('\n')
    #
    # result_1 = run_1(test_inputs)
    # if result_1 != 39:
    #     raise Exception(f"Test 1a did not pass, got {result_1}")
    #
    # test_inputs = """
    # on x=10..12,y=10..12,z=10..12
    # """.strip().split('\n')
    #
    # result_1 = run_1(test_inputs)
    # if result_1 != 27:
    #     raise Exception(f"Test did not pass, got {result_1}")
    #
    # test_inputs = """
    # on x=10..12,y=10..12,z=10..12
    # off x=10..12,y=10..12,z=10..12
    # """.strip().split('\n')
    #
    # result_1 = run_1(test_inputs)
    # if result_1 != 0:
    #     raise Exception(f"Test did not pass, got {result_1}")
    #
    # test_inputs = """
    # on x=10..12,y=10..12,z=10..12
    # on x=11..13,y=11..13,z=11..13
    # """.strip().split('\n')
    #
    # result_1 = run_1(test_inputs)
    # if result_1 != 46:
    #     raise Exception(f"Test did not pass, got {result_1}")
    #
    # test_inputs = """
    # on x=10..12,y=10..12,z=10..12
    # off x=10..12,y=10..12,z=10..12
    # on x=10..12,y=10..12,z=50..50
    # """.strip().split('\n')
    #
    # result_1 = run_1(test_inputs)
    # if result_1 != 9:
    #     raise Exception(f"Test did not pass, got {result_1}")
    #
    # test_inputs = """
    # on x=-20..26,y=-36..17,z=-47..7
    # """.strip().split('\n')
    #
    # result_1 = run_1(test_inputs)
    # if result_1 != 139590:
    #     raise Exception(f"Test did not pass, got {result_1}")
    #
    # test_inputs = """
    # on x=-20..26,y=-36..17,z=-47..7
    # on x=-20..33,y=-21..23,z=-26..28
    # """.strip().split('\n')
    #
    # result_1 = run_1(test_inputs)
    # if result_1 != 210918:
    #     raise Exception(f"Test did not pass, got {result_1}")
    #
    # cuboid = Cuboid(10,12,10,12,10,12)
    # if (result := cuboid.size()) != 27:
    #     raise Exception(result)
    #
    # if (result := Cuboid(-1,1,-8,-4,0,3).size()) != 60:
    #     raise Exception(result)

    # test_inputs = """
    # on x=-20..26,y=-36..17,z=-47..7
    # on x=-20..33,y=-21..23,z=-26..28
    # on x=-22..28,y=-29..23,z=-38..16
    # """.strip().split('\n')
    #
    # result_1 = run_1(test_inputs)
    # if result_1 != 225476:
    #     raise Exception(f"Test did not pass, got {result_1}")
    #
    # test_inputs = """
    # on x=-20..26,y=-36..17,z=-47..7
    # on x=-20..33,y=-21..23,z=-26..28
    # on x=-22..28,y=-29..23,z=-38..16
    # off x=-48..-20,y=23..25,z=-47..37
    # """.strip().split('\n')
    #
    # result_1 = run_1(test_inputs)
    # if result_1 != 225299:
    #     raise Exception(f"Test did not pass, got {result_1}")
    #
    # test_inputs = """
    # on x=-20..26,y=-36..17,z=-47..7
    # on x=-20..33,y=-21..23,z=-26..28
    # on x=-22..28,y=-29..23,z=-38..16
    # off x=-48..-20,y=23..25,z=10..11
    # """.strip().split('\n')
    #
    # result_1 = run_1(test_inputs)
    # if result_1 != 225470:
    #     raise Exception(f"Test did not pass, got {result_1}")
    #
    #
    test_inputs = """
    on x=-20..26,y=-36..17,z=-47..7
    on x=-20..33,y=-21..23,z=-26..28
    on x=-22..28,y=-29..23,z=-38..16
    on x=-46..7,y=-6..46,z=-50..-1
    on x=-49..1,y=-3..46,z=-24..28
    on x=2..47,y=-22..22,z=-23..27
    on x=-27..23,y=-28..26,z=-21..29
    on x=-39..5,y=-6..47,z=-3..44
    on x=-30..21,y=-8..43,z=-13..34
    on x=-22..26,y=-27..20,z=-29..19
    off x=-48..-32,y=26..41,z=-47..-37
    on x=-12..35,y=6..50,z=-50..-2
    off x=-48..-32,y=-32..-16,z=-15..-5
    on x=-18..26,y=-33..15,z=-7..46
    off x=-40..-22,y=-38..-28,z=23..41
    on x=-16..35,y=-41..10,z=-47..6
    off x=-32..-23,y=11..30,z=-14..3
    on x=-49..-5,y=-3..45,z=-29..18
    off x=18..30,y=-20..-8,z=-3..13
    on x=-41..9,y=-7..43,z=-33..15
    on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
    on x=967..23432,y=45373..81175,z=27513..53682
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 590784:
        raise Exception(f"Test 1b did not pass, got {result_1}")

    test_inputs = """
    on x=-5..47,y=-31..22,z=-19..33
    on x=-44..5,y=-27..21,z=-14..35
    on x=-49..-1,y=-11..42,z=-10..38
    on x=-20..34,y=-40..6,z=-44..1
    off x=26..39,y=40..50,z=-2..11
    on x=-41..5,y=-41..6,z=-36..8
    off x=-43..-33,y=-45..-28,z=7..25
    on x=-33..15,y=-32..19,z=-34..11
    off x=35..47,y=-46..-34,z=-11..5
    on x=-14..36,y=-6..44,z=-16..29
    on x=-57795..-6158,y=29564..72030,z=20435..90618
    on x=36731..105352,y=-21140..28532,z=16094..90401
    on x=30999..107136,y=-53464..15513,z=8553..71215
    on x=13528..83982,y=-99403..-27377,z=-24141..23996
    on x=-72682..-12347,y=18159..111354,z=7391..80950
    on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
    on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
    on x=-52752..22273,y=-49450..9096,z=54442..119054
    on x=-29982..40483,y=-108474..-28371,z=-24328..38471
    on x=-4958..62750,y=40422..118853,z=-7672..65583
    on x=55694..108686,y=-43367..46958,z=-26781..48729
    on x=-98497..-18186,y=-63569..3412,z=1232..88485
    on x=-726..56291,y=-62629..13224,z=18033..85226
    on x=-110886..-34664,y=-81338..-8658,z=8914..63723
    on x=-55829..24974,y=-16897..54165,z=-121762..-28058
    on x=-65152..-11147,y=22489..91432,z=-58782..1780
    on x=-120100..-32970,y=-46592..27473,z=-11695..61039
    on x=-18631..37533,y=-124565..-50804,z=-35667..28308
    on x=-57817..18248,y=49321..117703,z=5745..55881
    on x=14781..98692,y=-1341..70827,z=15753..70151
    on x=-34419..55919,y=-19626..40991,z=39015..114138
    on x=-60785..11593,y=-56135..2999,z=-95368..-26915
    on x=-32178..58085,y=17647..101866,z=-91405..-8878
    on x=-53655..12091,y=50097..105568,z=-75335..-4862
    on x=-111166..-40997,y=-71714..2688,z=5609..50954
    on x=-16602..70118,y=-98693..-44401,z=5197..76897
    on x=16383..101554,y=4615..83635,z=-44907..18747
    off x=-95822..-15171,y=-19987..48940,z=10804..104439
    on x=-89813..-14614,y=16069..88491,z=-3297..45228
    on x=41075..99376,y=-20427..49978,z=-52012..13762
    on x=-21330..50085,y=-17944..62733,z=-112280..-30197
    on x=-16478..35915,y=36008..118594,z=-7885..47086
    off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
    off x=2032..69770,y=-71013..4824,z=7471..94418
    on x=43670..120875,y=-42068..12382,z=-24787..38892
    off x=37514..111226,y=-45862..25743,z=-16714..54663
    off x=25699..97951,y=-30668..59918,z=-15349..69697
    off x=-44271..17935,y=-9516..60759,z=49131..112598
    on x=-61695..-5813,y=40978..94975,z=8655..80240
    off x=-101086..-9439,y=-7088..67543,z=33935..83858
    off x=18020..114017,y=-48931..32606,z=21474..89843
    off x=-77139..10506,y=-89994..-18797,z=-80..59318
    off x=8476..79288,y=-75520..11602,z=-96624..-24783
    on x=-47488..-1262,y=24338..100707,z=16292..72967
    off x=-84341..13987,y=2429..92914,z=-90671..-1318
    off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
    off x=-27365..46395,y=31009..98017,z=15428..76570
    off x=-70369..-16548,y=22648..78696,z=-1892..86821
    on x=-53470..21291,y=-120233..-33476,z=-44150..38147
    off x=-93533..-4276,y=-16170..68771,z=-104985..-24507
    """.strip().split('\n')

    result_2 = run_2(test_inputs)
                 # 6200413998736463
                 # 6194852080636271
                 #   50044647512470
                 # 2331145530588708
                 # 2673593094113518
                 # 2755019869817365
    if result_2 != 2758514936282235:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(22)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")
    if result_1 != 658691:
        raise Exception(result_1)

    # result_2 = run_2(input)
    # print(f"Finished 2 with result {result_2}")
