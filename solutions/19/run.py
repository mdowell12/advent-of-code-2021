from itertools import combinations

from solutions.get_inputs import read_inputs


def run(inputs):
    """
    first scanner = scanners.pop
    all oriented scanners = []
    while scanners remain:
        for remaining in remaining scanners:
            for each oriented scanner:
                if these scanners overlap:
                    orient remaining to oriented
                    shift all points and location to be relative to zero scanner
                    add to oriented list
                    break out of loop
        if we oriented a scanner, take it out of remaining scanners
        else there is an error and we're in an infinite loop
    now that all are oriented, we should be able to take the union of all beacon coordinates

    Note that orient means we must change the scanner's beacon coordinates so that they
    are relative to scanner[0] in distance and orientation
    """
    scanners = _parse_input(inputs)
    remaining = [s for s in scanners[1:]]
    oriented = [scanners[0]]
    locations_when_oriented = []
    while remaining:
        for i, remaining_scanner in enumerate(remaining):
            for oriented_scanner in oriented:
                if remaining_scanner.overlaps_with(oriented_scanner):
                    print(f"{remaining_scanner.name} overlaps with {oriented_scanner.name}")
                    # Rotates remaining_scanner
                    remaining_scanner.set_position_relative_to(oriented_scanner)
                    locations_when_oriented.append(remaining_scanner.location)
                    print(f"{remaining_scanner.name} location set to {remaining_scanner.location}")
                    # shift remaining_scanner to be relative to zero
                    remaining_scanner.shift_to_match(oriented_scanner)
                    remaining_scanner.shift_to_zero()
                    print(f"{remaining_scanner.name} final location set to {remaining_scanner.location}")
                    break
            else:
                continue
            break
        else:
            raise Exception('could not find one')
        oriented.append(remaining.pop(i))
        print(f'{len(remaining)} remain')

    all_beacons = set([beacon for s in oriented for beacon in s.beacons])

    first, last = sorted(locations_when_oriented)[0], sorted(locations_when_oriented)[1]
    dist = _greatest_distance_between_scanners(locations_when_oriented)

    return len(all_beacons), dist


def _greatest_distance_between_scanners(locations_when_oriented):
    result = None
    for left, right in combinations(locations_when_oriented, 2):
        distance = _manhattan_distance(left, right)
        if result is None or distance > result:
            result = distance
    return result


def _manhattan_distance(first, last):
    return sum([abs(first[0]-last[0]),abs(first[1]-last[1]),abs(first[2]-last[2])])


def _parse_input(inputs):
    inputs = [i for i in inputs if i.strip()]
    beacon_lines = []
    name = None
    scanners = []
    is_first = True
    while inputs:
        line = inputs.pop(0)
        if "scanner" in line:
            if name and beacon_lines:
                location = (0,0,0) if is_first else None
                scanners.append(Scanner(name, beacon_lines, location=location))
                is_first = False
            name = line.replace('---', '').strip()
            beacon_lines = []
        else:
            beacon_lines.append(line)
    if name and beacon_lines:
        scanners.append(Scanner(name, beacon_lines))
    return scanners


'''
scanner can store set of all manhattan distances between its beacons
(we probably want to store the beacon points associated with each distance for later)
to check for matches between two scanners, look at size of intersection of distance set
    if at least min-required, then the scanners are a match. we can orient them later
'''

class Scanner:

    def __init__(self, name, lines, location=None):
        self.name = name
        beacons = self._parse_beacons(lines)
        self.location = location
        self._orient_to(beacons)

    def _orient_to(self, beacons):
        self.beacons = beacons
        self.distances = self._find_distances(beacons)
        self.distance_set = set(self.distances.values())

    def overlaps_with(self, other_scanner, threshold=12):
        overlapping = self.get_overlapping_pairs(other_scanner)
        return len(overlapping[self.name]) >= threshold

    def shift_to_match(self, other_scanner):
        '''
        If this scanner's location and beacons are marked relative to other_scanner,
        then shift this scanner's location and beacons to be relative to the scanner other_scanner is referencing.
        '''
        # Assume other_scanner already is relative to zero scanner
        distance_to_shift = other_scanner.location
        new_beacons = [self._add_points(beacon, distance_to_shift) for beacon in self.beacons]
        self._orient_to(new_beacons)
        self.location = self._add_points(self.location, distance_to_shift)

    def shift_to_zero(self):
        distance_to_shift = (self.location[0],self.location[1],self.location[2])
        new_beacons = [self._add_points(beacon, distance_to_shift) for beacon in self.beacons]
        self._orient_to(new_beacons)
        self.location = (0,0,0)

    def _add_points(self, p1, p2):
        return (p1[0]+p2[0], p1[1]+p2[1], p1[2]+p2[2])

    def get_overlapping_pairs(self, other_scanner):
        result = {self.name: set(), other_scanner.name: set()}

        for pair, distance_tup in self.distances.items():
            for other_pair, other_distance_tup in other_scanner.distances.items():
                distance = sum(distance_tup)
                other_distance = sum(other_distance_tup)
                if distance == other_distance and sorted(distance_tup) == sorted(other_distance_tup):
                    result[self.name].add(pair[0])
                    result[self.name].add(pair[1])
                    result[other_scanner.name].add(other_pair[0])
                    result[other_scanner.name].add(other_pair[1])
        return result

    def set_position_relative_to(self, other_scanner):
        if self.location is not None:
            raise Exception('Location already set ' + self)
        if other_scanner.location is None:
            raise Exception('scanner does not have location ' + other_scanner)
        self.location = self._get_position_relative_to(other_scanner)

    def _get_position_relative_to(self, other_scanner):
        '''
        If we know that two scanners are oriented in the same direction, then it's as simple
        as finding two beacons that overlap and doing subtraction, e.g. if scanner 0 thinks the
        beacon is at (5,4,1) and scanner 1 thinks it's at (-3,2,0), then scanner 1 must
        be at (5-(-3), 4-2, 1-0) == (8, 2, 1).

        But scanners will not be oriented the same. We can test this by seeing if a potential position for
        scanner 1 would make all its matching beacon positions line up with those of scanner 0. If they do
        not line up, we should rotate scanner 1 and try again. Do this until we get a match.
        '''
        all_rotations = _find_all_rotations(self.beacons)
        for rotated_beacons in all_rotations:
            self._orient_to(rotated_beacons)
            overlapping_pairs = self.get_overlapping_pairs(other_scanner)
            my_left_most = _find_lower_left_beacon(overlapping_pairs[self.name])
            other_left_most = _find_lower_left_beacon(overlapping_pairs[other_scanner.name])
            potential_position = (
                other_left_most[0] - my_left_most[0],
                other_left_most[1] - my_left_most[1],
                other_left_most[2] - my_left_most[2]
            )
            if self._position_checks_out(overlapping_pairs[self.name], overlapping_pairs[other_scanner.name], potential_position):
                return potential_position
        raise Exception("did not find orientation that matched")

    def _position_checks_out(self, my_overlapping_points, other_overlapping_points, potential_position):
        if len(my_overlapping_points) != len(other_overlapping_points):
            raise Exception()
        mine_sorted = sorted(my_overlapping_points)
        other_sorted = sorted(other_overlapping_points)
        for mine, other in zip(mine_sorted, other_sorted):
            if mine[0] != other[0] - potential_position[0]:
                return False
            if mine[1] != other[1] - potential_position[1]:
                return False
            if mine[2] != other[2] - potential_position[2]:
                return False
        return True

    def _manhattan_distance_set(self):
        return set(sum(i) for i in self.distance_set)

    def _parse_beacons(self, lines):
        result = []
        for line in lines:
            result.append(tuple(int(i) for i in line.strip().split(',')))
        return result

    def _find_distances(self, beacons):
        result = {}
        for pair in combinations(beacons, 2):
            result[pair] = _distance_tup(pair)
        return result

    def _print_beacons(self):
        print('\n'.join(str(b) for b in self.beacons))

    def __repr__(self):
        return f"{self.name} at {self.location} beacons: {self.beacons}"


def _distance_tup(pair):
    b1, b2 = pair
    return (abs(b1[0]-b2[0]), abs(b1[1]-b2[1]), abs(b1[2]-b2[2]))


def _find_lower_left_beacon(beacons):
    most_left = None
    for beacon in beacons:
        x, y, z = beacon
        if most_left is None:
            most_left = beacon
        elif x < most_left[0]:
            most_left = beacon
        elif x == most_left[0] and y < most_left[1]:
            most_left = beacon
        elif x == most_left[0] and y == most_left[1] and z < most_left[2]:
            most_left = beacon
    return most_left


def _find_all_rotations(beacons):
    all_sequences = [[point for point in sequence(beacon)] for beacon in beacons]
    return [i for i in zip(*all_sequences)]

"""
These three functions were stolen from stackoverflow. They calculate each possible
rotation of a set of beacons.
"""
def roll(v): return (v[0],v[2],-v[1])
def turn(v): return (-v[1],v[0],v[2])
def sequence(v):
    for cycle in range(2):
        for step in range(3):  # Yield RTTT 3 times
            v = roll(v)
            yield(v)           #    Yield R
            for i in range(3): #    Yield TTT
                v = turn(v)
                yield(v)
        v = roll(turn(roll(v)))  # Do RTR


def run_tests():

    test = """
    --- scanner 0 ---
    0,2,0
    4,1,0
    3,3,0

    --- scanner 1 ---
    -1,-1,0
    -5,0,0
    -2,1,0

    --- scanner 2 ---
    -1,1,-1
    0,5,-1
    1,2,-1
    3,5,77
    """.strip().split('\n')
    scanners = _parse_input(test)
    if not scanners[0].overlaps_with(scanners[1], threshold=3):
        raise Exception()

    if (result := scanners[1]._get_position_relative_to(scanners[0])) != (5,2,0):
        raise Exception(result)

    if not scanners[1].overlaps_with(scanners[2], threshold=3):
        raise Exception()

    if (result := scanners[2]._get_position_relative_to(scanners[0])) != (5,2,1):
        raise Exception(result)

    test = """
    --- scanner 0 ---
    0,2,0
    2,0,0
    0,0,2

    --- scanner 1 ---
    -1,2,0
    1,0,0
    -1,0,2
    """.strip().split('\n')
    scanners = _parse_input(test)
    if not scanners[0].overlaps_with(scanners[1], threshold=3):
        raise Exception()

    # test = """
    # --- scanner 0 ---
    # -1,-1,1
    # -2,-2,2
    # -2,-3,1
    # 5,6,-4
    # 8,0,7
    # """.strip().split('\n')
    # beacons = _parse_input(test)[0].beacons
    # print('\n'.join(str(i) for i in _find_all_rotations(beacons)))
    # import pdb; pdb.set_trace()

    test_inputs = """
    --- scanner 0 ---
    404,-588,-901
    528,-643,409
    -838,591,734
    390,-675,-793
    -537,-823,-458
    -485,-357,347
    -345,-311,381
    -661,-816,-575
    -876,649,763
    -618,-824,-621
    553,345,-567
    474,580,667
    -447,-329,318
    -584,868,-557
    544,-627,-890
    564,392,-477
    455,729,728
    -892,524,684
    -689,845,-530
    423,-701,434
    7,-33,-71
    630,319,-379
    443,580,662
    -789,900,-551
    459,-707,401

    --- scanner 1 ---
    686,422,578
    605,423,415
    515,917,-361
    -336,658,858
    95,138,22
    -476,619,847
    -340,-569,-846
    567,-361,727
    -460,603,-452
    669,-402,600
    729,430,532
    -500,-761,534
    -322,571,750
    -466,-666,-811
    -429,-592,574
    -355,545,-477
    703,-491,-529
    -328,-685,520
    413,935,-424
    -391,539,-444
    586,-435,557
    -364,-763,-893
    807,-499,-711
    755,-354,-619
    553,889,-390

    --- scanner 2 ---
    649,640,665
    682,-795,504
    -784,533,-524
    -644,584,-595
    -588,-843,648
    -30,6,44
    -674,560,763
    500,723,-460
    609,671,-379
    -555,-800,653
    -675,-892,-343
    697,-426,-610
    578,704,681
    493,664,-388
    -671,-858,530
    -667,343,800
    571,-461,-707
    -138,-166,112
    -889,563,-600
    646,-828,498
    640,759,510
    -630,509,768
    -681,-892,-333
    673,-379,-804
    -742,-814,-386
    577,-820,562

    --- scanner 3 ---
    -589,542,597
    605,-692,669
    -500,565,-823
    -660,373,557
    -458,-679,-417
    -488,449,543
    -626,468,-788
    338,-750,-386
    528,-832,-391
    562,-778,733
    -938,-730,414
    543,643,-506
    -524,371,-870
    407,773,750
    -104,29,83
    378,-903,-323
    -778,-728,485
    426,699,580
    -438,-605,-362
    -469,-447,-387
    509,732,623
    647,635,-688
    -868,-804,481
    614,-800,639
    595,780,-596

    --- scanner 4 ---
    727,592,562
    -293,-554,779
    441,611,-461
    -714,465,-776
    -743,427,-804
    -660,-479,-426
    832,-632,460
    927,-485,-438
    408,393,-506
    466,436,-512
    110,16,151
    -258,-428,682
    -393,719,612
    -211,-452,876
    808,-476,-593
    -575,615,604
    -485,667,467
    -680,325,-822
    -627,-443,-432
    872,-547,-609
    833,512,582
    807,604,487
    839,-516,451
    891,-625,532
    -652,-548,-490
    30,-46,-14
    """.strip().split('\n')

    scanners = _parse_input(test_inputs)

    if not scanners[0].overlaps_with(scanners[1]):
        raise Exception()

    if not scanners[4].overlaps_with(scanners[1]):
        raise Exception()

    if (result := scanners[1]._get_position_relative_to(scanners[0])) != (68,-1246,-43):
        raise Exception(result)

    result_1, result_2 = run(test_inputs)
    if result_1 != 79:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    if result_2 != 3621:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(19)

    result_1, result_2 = run(input)
    print(f"Finished 1 with result {result_1}")
    print(f"Finished 2 with result {result_2}")
