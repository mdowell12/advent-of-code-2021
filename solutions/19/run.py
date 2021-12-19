from itertools import combinations

from solutions.get_inputs import read_inputs

"""
first scanner = scanners.pop
all oriented scanners = []
while scanners remain:
    for remaining in remaining scanners:
        for each oriented scanner:
            if these scanners overlap:
                orient remaining and add to oriented list
                break out of loop
    if we oriented a scanner, take it out of remaining scanners
    else there is an error and we're in an infinite loop
now that all are oriented, we should be able to take the union of all beacon coordinates

Note that orient means we must change the scanner's beacon coordinates so that they
are relative to scanner[0] in distance and orientation

# TODO shore up function for identifying overlaps
# TODO scanners should have a location relative to the zero scanner (0,0,0)
# TODO calculate scanner position relative to zero after match is made
# TODO calculate scanner's beacon positions relative to zero after match is made
"""

def run_1(inputs):
    scanners = _parse_input(inputs)


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


def run_2(inputs):
    pass

'''
scanner can store set of all manhattan distances between its beacons
(we probably want to store the beacon points associated with each distance for later)
to check for matches between two scanners, look at size of intersection of distance set
    if at least min-required, then the scanners are a match. we can orient them later
'''

class Scanner:

    def __init__(self, name, lines, location=None):
        self.name = name
        self.beacons = self._parse_beacons(lines)
        self.location = location
        self.distances = self._find_distances(self.beacons)
        self.distance_to_points = {v: k for k, v in self.distances.items()}
        if len(self.distances) != len(self.distance_to_points):
            raise Exception("There are duplicate distances")
        self.distance_set = set(self.distances.values())

    def overlaps_with(self, other_scanner, threshold=12):
        # import pdb; pdb.set_trace()
        return len(self._manhattan_distance_set().intersection(other_scanner._manhattan_distance_set())) >= threshold

    def get_overlapping_points(self, other_scanner):
        overlapping_distances = self.distance_set.intersection(other_scanner.distance_set)
        result = {}
        result[self.name] = [self.distance_to_points[i] for i in overlapping_distances]
        result[other_scanner.name] = [other_scanner.distance_to_points[i] for i in overlapping_distances]

        for scanner in [self, other_scanner]:
            points = [self.distance_to_points[i] for i in overlapping_distances]
            result[self.name] = set(i for pair in points for i in pair)
        # import pdb; pdb.set_trace()
        return result

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
            b1, b2 = pair
            result[pair] = (abs(b1[0]-b2[0]), abs(b1[1]-b2[1]), abs(b1[2]-b2[2]))
        return result

    def _print_beacons(self):
        print('\n'.join(str(b) for b in self.beacons))

    def __repr__(self):
        return f"{self.name} at {self.location} beacons: {self.beacons}"


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
    """.strip().split('\n')
    scanners = _parse_input(test)
    if not scanners[0].overlaps_with(scanners[1], threshold=3):
        raise Exception()
    overlapping = scanners[0].get_overlapping_points(scanners[1])
    expected_overlap_from_zero = set(scanners[0].beacons)
    if not overlapping[scanners[0].name] == expected_overlap_from_zero:
        raise Exception()

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
    overlapping = scanners[0].get_overlapping_points(scanners[1])
    expected_overlap_from_zero = {
        (-618,-824,-621),
        (-537,-823,-458),
        (-447,-329,318),
        (404,-588,-901),
        (544,-627,-890),
        (528,-643,409),
        (-661,-816,-575),
        (390,-675,-793),
        (423,-701,434),
        (-345,-311,381),
        (459,-707,401),
        (-485,-357,347)
    }
    if not overlapping[scanners[0].name] == expected_overlap_from_zero:
        raise Exception(overlapping[scanners[0].name])

    if not scanners[4].overlaps_with(scanners[1]):
        raise Exception()

    result_1 = run_1(test_inputs)
    if result_1 != 79:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    # result_2 = run_2(test_inputs)
    # if result_2 != 0:
    #     raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(19)

    # result_1 = run_1(input)
    # print(f"Finished 1 with result {result_1}")

    # result_2 = run_2(input)
    # print(f"Finished 2 with result {result_2}")
