from collections import defaultdict

from solutions.get_inputs import read_inputs


def run_1(inputs):
    game = Game(inputs)
    return game.play()


def run_2(inputs):
    game = Game(inputs)
    return game.play_to_lose()


class Game:

    def __init__(self, inputs):
        self.draws = [int(i) for i in inputs[0].strip().split(',')]
        self.boards = self._parse_boards(inputs)

    def play(self):
        while not any(b.has_won() for b in self.boards):
            number = self.draws.pop(0)
            print(f"Played number {number}")
            for b in self.boards:
                b.play(number)
        winner = [b for b in self.boards if b.has_won()][0]
        return number * winner.sum_unmarked()

    def play_to_lose(self):
        winners = []
        while self.boards:
            number = self.draws.pop(0)
            print(f"Played number {number}")
            for b in self.boards:
                b.play(number)
                if b.has_won():
                    winners.append(b)
            self.boards = [b for b in self.boards if not b.has_won()]
            print(f"{len(self.boards)} boards remain")
        final = winners[-1]
        return number * final.sum_unmarked()

    def _parse_boards(self, inputs):
        copy = [i for i in inputs[2:]]
        boards = []
        current_board = []
        while copy:
            line = [i for i in copy.pop(0).strip().split(' ') if i]
            if line:
                current_board.append([int(i) for i in line])
            else:
                boards.append(Board(current_board))
                current_board = []

        if current_board:
            boards.append(Board(current_board))
        return boards


class Board:

    def __init__(self, lines):
        self.points = defaultdict(lambda: [])
        for x, line in enumerate(lines):
            for y, num in enumerate(line):
                self.points[num].append([x, y, False])
        self.row_counters = [0] * 5
        self.col_counters = [0] * 5

    def play(self, number):
        for point in self.points.get(number, []):
            point[2] = True
            self.row_counters[point[0]] += 1
            self.col_counters[point[1]] += 1

    def has_won(self):
        return max(self.row_counters) == 5 or max(self.col_counters) == 5

    def sum_unmarked(self):
        total = 0
        for num, points in self.points.items():
            for point in points:
                if not point[2]:
                    total += num
        return total

    def __repr__(self):
        lines = [['X']*5 for i in range(5)]
        for num, points in self.points.items():
            for point in points:
                if not point[2]:
                    lines[point[1]][point[0]] = str(num)
        return '\n'.join(' '.join(l) for l in lines)


def run_tests():
    test_inputs = """
    7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

    22 13 17 11  0
     8  2 23  4 24
    21  9 14 16  7
     6 10  3 18  5
     1 12 20 15 19

     3 15  0  2 22
     9 18 13 17  5
    19  8  7 25 23
    20 11 10 24  4
    14 21 16 12  6

    14 21 17 24  4
    10 16 15  9 19
    18  8 23 26 20
    22 11 13  6  5
     2  0 12  3  7
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 4512:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 1924:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(4)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
