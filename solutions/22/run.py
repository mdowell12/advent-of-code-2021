from collections import defaultdict
from time import time

from solutions.get_inputs import read_inputs


# def run_1(inputs):
#     commands = [_parse_line(line) for line in inputs]
#     # print('\n'.join(str(l) for l in commands))
#     # grid = defaultdict(lambda: False)
#     grid = {}
#     for command in commands:
#         grid = _do_command(command, grid)
#         # print(sorted(k for k,v in grid.items() if v))
#         print(f'{command} {sum(int(i) for i in grid.values())}')
#         # import pdb; pdb.set_trace()
#     return sum(int(i) for i in grid.values())

def run_1(inputs):
    commands = [_parse_line(line) for line in inputs]
    commands = [c for c in commands if c[1][0] >= -50 and c[1][1] <= 50]
    return _run(commands)


def run_2(inputs):
    commands = [_parse_line(line) for line in inputs]
    return _run(commands)


def _run(commands):
    x_values = []
    y_values = []
    for is_on, (x1, x2), (y1, y2), (z1, z2) in commands:
        # Does this double count the borders?
        # Saw an interval (6,6), should we include something like this?
        x_values.append(x1)
        x_values.append(x2)
        y_values.append(y1)
        y_values.append(y2)
    x_values = sorted(set(x_values))
    x_values.append(x_values[-1] + 1)
    y_values = sorted(set(y_values))
    y_values.append(y_values[-1] + 1)

    cuboids = []
    import pdb; pdb.set_trace()
    for i in range(len(x_values) - 1):
        for j in range(len(y_values) - 1):
            x1, x2 = x_values[i], x_values[i+1] - 1
            y1, y2 = y_values[j], y_values[j+1] - 1
            print(f'{x1}..{x2} {y1}..{y2}')
            assert x1 <= x2
            assert y1 <= y2
            cuboids_this_slice = _get_cuboids_for_slice(x1, x2, y1, y2, commands)
            cuboids += cuboids_this_slice

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
    debug = False

    intervals = []
    if debug: print(f"cuboids for slice {slice_x1, slice_x2, slice_y1, slice_y2}")
    # import pdb; pdb.set_trace()
    for is_on, (x1, x2), (y1, y2), (z1, z2) in commands:
        if debug: print(f'\tcommand: {is_on, (x1, x2), (y1, y2), (z1, z2)} and intervals: {intervals}')

        if not (_does_overlap((slice_x1, slice_x2), (x1, x2)) and _does_overlap((slice_y1, slice_y2), (y1, y2))):
            if debug: print(f'\tno overlap for {x1}..{x1} {y1}..{y2}')
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
            continue


        if len(intervals) == 0:
            if is_on:
                if debug: print(f'\tfirst ON interval {x1}..{x1} {y1}..{y2}. Added {z1}..{z2}.')
                intervals.append([z1,z2])
            else:
                if debug: print(f'\tfirst interval, but OFF {x1}..{x1} {y1}..{y2}. Skipped.')
            # print(slice_x1, slice_x2, slice_y1, slice_y2, intervals)
            continue

        if len(intervals) == 1:
            # import pdb; pdb.set_trace()
            if _does_overlap(intervals[0], (z1, z2)):
                if is_on:
                    intervals[0][1] = max(intervals[0][1], z2)
                    if debug: print(f'\tON interval {z1}..{z2} overlapped. Intervals now: {intervals}')
                else:
                    intervals[0][1] = z1 - 1
                    new_intervals = _turn_off(intervals[0], None, z1, z2)
                    intervals[0] = new_intervals[0]
                    if len(new_intervals) > 1:
                        intervals.append(new_intervals[1])
                    if debug: print(f'\tOFF interval {z1}..{z2} overlapped. Intervals now: {intervals}')
            else:
                if is_on:
                    intervals.append([z1,z2])
                    if debug: print(f'\ON interval {z1}..{z2} did not overlap. Intervals now: {intervals}')
                else:
                    if debug: print(f'\tOFF interval {z1}..{z2} did not overlap. Skipped. Intervals now: {intervals}')
            # print(slice_x1, slice_x2, slice_y1, slice_y2, intervals)
            continue
        # import pdb; pdb.set_trace()

        for i in range(len(intervals) - 1):
            left = intervals[i]
            right = intervals[i+1]

            if _does_overlap(left, (z1, z2)):
                if _does_overlap((z1, z2), right):
                    if is_on:
                        # stitch together
                        left[1] = right[0] - 1
                        if debug: print(f'\ON interval {z1}..{z2} overlapped with {left} and {right}. Intervals now: {intervals}')
                    else:
                        left[1] = z1 - 1
                        right[0] = z2 + 1
                        if debug: print(f'\OFF interval {z1}..{z2} overlapped with {left} and {right}. Intervals now: {intervals}')
                else:
                    if is_on:
                        left[1] = z2
                        if debug: print(f'\ON interval {z1}..{z2} overlapped with {left} but not {right}. Intervals now: {intervals}')
                    else:
                        left[1] = z1 - 1
                        if debug: print(f'\OFF interval {z1}..{z2} overlapped with {left} but not {right}. Intervals now: {intervals}')
                break
            else:
                if _does_overlap((z1, z2), right):
                    if is_on:
                        right[0] = z2
                        if debug: print(f'\ON interval {z1}..{z2} overlapped with {right} but not {left}. Intervals now: {intervals}')
                    else:
                        right[0] = z2 + 1
                        if debug: print(f'\OFF interval {z1}..{z2} overlapped with {right} but not {left}. Intervals now: {intervals}')
                break
        else:
            if is_on:
                intervals.append([z1,z2])
                if debug: print(f'\ON interval {z1}..{z2} did not overlap any intervals, appending. Intervals now: {intervals}')
            else:
                if debug: print(f'\OFF interval {z1}..{z2} did not overlap any intervals, skipping.')

        intervals = sorted(intervals, key=lambda t: t[0])
        intervals = [i for i in intervals if i[0] <= i[1]]
        # print(slice_x1, slice_x2, slice_y1, slice_y2, intervals)
        # import pdb; pdb.set_trace()
        if debug: print(f'\Finished with intervals {intervals}')
        if debug: print()

    if debug: print(f"final intervals {intervals}")
    if debug: print()
    cuboids = [Cuboid(slice_x1, slice_x2, slice_y1, slice_y2, z1, z2) for z1, z2 in intervals]

    return cuboids

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


# def _get_total_intersecting_size(cuboid, other_cuboids):
#     intersecting = []
#     for other_cuboid in other_cuboids:
#         intersecting_bounds = cuboid.get_bounds_of_intersection(other_cuboid)
#         if not intersecting_bounds:
#             continue
#         (x0, x1),(y0, y1),(z0,z1) = intersecting_bounds
#         intersecting.append(Cuboid(x0, x1, y0, y1, z0, z1))
#     if not intersecting:
#         return 0
#     elif len(intersecting) == 1:
#         return intersecting[0].size()
#     else:
#         return _get_total_intersecting_size(intersecting[0], intersecting[1:])

def _does_overlap(first, second):
    # import pdb; pdb.set_trace()
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

    def get_bounds_of_intersection(self, other_cuboid):
        x_overlap = self._overlap((self.x1, self.x2), (other_cuboid.x1, other_cuboid.x2))
        y_overlap = self._overlap((self.y1, self.y2), (other_cuboid.y1, other_cuboid.y2))
        z_overlap = self._overlap((self.z1, self.z2), (other_cuboid.z1, other_cuboid.z2))
        if x_overlap and y_overlap and z_overlap:
            return (x_overlap, y_overlap, z_overlap)
        return None

    def size_of_intersection(self, other_cuboids):
        now = int(time())
        all_intersecting_points = set()
        for cuboid in other_cuboids:
            intersecting = self.get_bounds_of_intersection(cuboid)
            if not intersecting:
                continue
            all_intersecting_points = all_intersecting_points.union(self.generate_points_from_bounds(intersecting))
        print(f'elapsed secs: {str(now - int(time()))}')
        return len(all_intersecting_points)

    def _overlap(self, first, second):
        if first[1] < second[0] or second[1] < first[0]:
            return None
        return (max(first[0], second[0]), min(first[1], second[1]))

    def generate_points(self):
        return self.generate_points_from_bounds(((self.x1, self.x2), (self.y1, self.y2), (self.z1, self.z2)))

    def generate_points_from_bounds(self, bounds):
        (x1, x2),(y1, y2),(z1, z2) = bounds
        result = set()
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                for z in range(z1, z2+1):
                    result.add((x,y,z))
        return result

    def __repr__(self):
        return f'({self.x1}..{self.x2}),({self.y1}..{self.y2}),({self.z1}..{self.z2})'




def run_tests():
    if (result := _does_overlap((0,5), (3,6))) != True:
        raise Exception(result)

    if (result := _does_overlap((6,10), (3,6))) != True:
        raise Exception(result)

    if (result := _does_overlap((0,5), (100,105))) != False:
        raise Exception(result)

    if (result := _does_overlap((-46, -41), (-4100, -4000))) != False:
        raise Exception(result)

    if (result := _does_overlap((10, 10), (9,11))) != True:
        raise Exception(result)

    if (result := _does_overlap((9,11), (10, 10))) != True:
        raise Exception(result)

    test_inputs = """
    on x=10..12,y=10..12,z=10..12
    on x=11..13,y=11..13,z=11..13
    off x=9..11,y=9..11,z=9..11
    on x=10..10,y=10..10,z=10..10
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 39:
        raise Exception(f"Test 1a did not pass, got {result_1}")
    #
    # cuboid = Cuboid(10,12,10,12,10,12)
    # if (result := cuboid.size()) != 27:
    #     raise Exception(result)
    # if (result := cuboid.get_bounds_of_intersection(Cuboid(11,13,11,13,11,13))) != ((11, 12),(11, 12),(11, 12)):
    #     raise Exception(result)
    # if (result := cuboid.get_bounds_of_intersection(Cuboid(11,13,-4,5,11,13))) != None:
    #     raise Exception(result)
    #
    # if (result := cuboid.get_bounds_of_intersection(Cuboid(0,20,-4,50,9,14))) != ((10, 12),(10, 12),(10, 12)):
    #     raise Exception(result)
    #
    # if (result := Cuboid(-1,1,-8,-4,0,3).size()) != 60:
    #     raise Exception(result)
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
    if result_2 != 2758514936282235:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(22)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    # result_2 = run_2(input)
    # print(f"Finished 2 with result {result_2}")
