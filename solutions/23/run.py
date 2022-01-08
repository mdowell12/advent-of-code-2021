from abc import ABC, abstractmethod

from solutions.get_inputs import read_inputs

"""
Each turn, one of the eight amphipods must move, and each has max of three moves it can make
We can keep a tree of (energy spent this turn, all current positions) and for each turn evaluate
each leaf node and add new leaves for every possible move that could be made. Branches terminate
when either the cave is organized or no possible moves can be made.

# DONE model the cave - (x,y) coordinate system with bounds, or dict that maps coordinate to X, . or amphipod?
# DONE parse input
# DONE create the tree data structure. BFS with queue of still processing caves and add to "finished" list of organized caves that can each reference previous and calc total cost.
# DONE Function to determine all possible moves each amphipod can make with a given configuration
    - needs to take into account not stopping in front of room
    - needs to take into account that if in hallway and stops, is locked until it can move fully into its room
    - needs to filter valid moves when one results in amphipod in its destination room
    - needs to move amphipod in top of room to bottom if possible
# DONE Function to do the move
# DONE Function to determine if cave is organized

# OPTIMIZE:
  - DONE If game has finished, begin cutting off any other games that have higher score
"""

def run_1(inputs):
    cave = Cave1(_parse_inputs(inputs), None, None, None, cost_so_far=0)
    return _run(cave)


def run_2(inputs):
    cave = Cave2(_parse_inputs(inputs), None, None, None, cost_so_far=0)
    return _run(cave)


def _run(cave):
    caves = [cave]
    hash_to_score = {}
    lowest_cave = None
    lowest_score = None
    # stuck_caves = set()
    i = 0
    while caves:
        i+=1

        cave = caves.pop(0)
        next_caves = cave.get_next_caves()
        # import pdb; pdb.set_trace()
        # if cave.grid[(3,5)] == 'A' and cave.grid[(3,4)] == 'A' and cave.grid[(5,4)] == 'B' and cave.grid[(5,5)] == 'B':
        #     import pdb; pdb.set_trace()
        # if not next_caves:
        #     this_hash = cave.hash()
        #     stuck_caves.add(this_hash)

        for next_cave in next_caves:
            hash = next_cave.hash()

            # if hash in stuck_caves:
            #     print("stuck cave, skipping ")
            #     continue

            current_cost = next_cave.get_total_cost()
            if next_cave.is_organized():
                if lowest_score is None or current_cost < lowest_score:
                    lowest_score = current_cost
                    lowest_cave = next_cave
                continue

            if hashed_score := hash_to_score.get(hash):
                if current_cost >= hashed_score:
                    continue
                else:
                    hash_to_score[hash] = current_cost
            else:
                hash_to_score[hash] = current_cost

            caves.append(next_cave)

        if i % 100000 == 0:
            print(i, len(caves), lowest_score)

    lowest_cave.print_game()
    print(f'final {lowest_score}')
    return lowest_score


class Cave(ABC):

    AMPHIPOD_TO_MOVE_COST = {
        'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000,
    }

    AMPHIPODS = set(AMPHIPOD_TO_MOVE_COST.keys())

    def __init__(self,
                 grid,
                 previous_cave,
                 last_move,
                 cost_last_move,
                 cost_so_far=0):
        self.grid = grid
        self.previous_cave = previous_cave
        self.last_move = last_move
        self.cost_last_move = cost_last_move
        self.cost_so_far = cost_so_far

    @abstractmethod
    def is_organized(self):
        pass

    @abstractmethod
    def create_new_cave(self, new_grid, last_move, cost, cost_so_far):
        pass

    @abstractmethod
    def get_amphipod_to_room_coords(self):
        pass

    @abstractmethod
    def get_room_coords(self):
        return

    @abstractmethod
    def path_out_of_room_is_clear(self, position):
        """
        I am in another's room and want to get out. Return True if I am at the
        edge of the room or if I am deeper in the room but the path out is clear.
        """
        pass

    def get_next_caves(self):
        next_moves = self.get_next_moves()
        result = []
        for original_position, moves in next_moves.items():
            for next_position, amphipod_type, cost in moves:
                new_grid = {k: v for k, v in self.grid.items()}
                new_grid[original_position] = '.'
                new_grid[next_position] = amphipod_type
                last_move = (original_position, next_position, amphipod_type)
                cost_so_far = self.cost_so_far + cost
                new_cave = self.create_new_cave(new_grid, last_move, cost, cost_so_far)
                result.append(new_cave)
        return result

    def get_next_moves(self):
        """
        For each amphipod (position, type), determine all adjacent coordinates
        that are a valid move and return along with cost.
        :return: dict[original position] -> list[(next position, type, cost of move)]
        """
        amphipods = [tup for tup in self.grid.items() if tup[1] in self.AMPHIPODS]
        result = {}

        for position, amphipod_type in amphipods:
            valid_nexts = self._get_valid_nexts_for_amphipod(position, amphipod_type)
            if valid_nexts:
                result[position] = valid_nexts
        return result

    def get_total_cost(self):
        return self.cost_so_far

    def _room_occupied_by_stranger(self, amphipod_type):
        my_room_coords = self.get_amphipod_to_room_coords()[amphipod_type]
        return not all(self.grid[c] in {amphipod_type, '.'} for c in my_room_coords)

    def _amphipod_is_stopped(self, amphipod_type, current_position):
        """
        amphipod is stopped if the last move was made by another amphipod
        """
        return self.last_move[2] != amphipod_type or self.last_move[1] != current_position

    def _hallway_above_me_is_not_occupied(self, my_x):
        return self.grid[(my_x, 1)] == '.'

    def _is_backwards_move(self, amphipod_type, current_position, next_position):
        return self.last_move and \
            self.last_move[2] == amphipod_type and \
            self.last_move[0] == next_position and \
            self.last_move[1] == current_position

    def _get_valid_nexts_for_amphipod(self, position, amphipod_type):
        if position in self.get_room_coords():
            # I am in my room and there are no strangers here, so stay here
            if position in self.get_amphipod_to_room_coords()[amphipod_type] and not self._room_occupied_by_stranger(amphipod_type):
                return []
            # In another's room, try and move out of other home
            elif self.path_out_of_room_is_clear(position) and self._hallway_above_me_is_not_occupied(position[0]):
                return [((position[0], 1), amphipod_type, self.AMPHIPOD_TO_MOVE_COST[amphipod_type] * (position[1]-1))]
            # No moves
            else:
                return []

        else:
            valid_nexts = []
            adjacents = [
                (position[0]-1, position[1]),
                (position[0]+1, position[1]),
                (position[0], position[1]-1),
                (position[0], position[1]+1),
            ]

            # Prefer going to the room by filtering candidate next positions
            if not self._room_occupied_by_stranger(amphipod_type):
                if to_room := [a for a in adjacents if a in self.get_amphipod_to_room_coords()[amphipod_type]]:
                    adjacents = to_room

            for next_position in adjacents:
                if self._is_backwards_move(amphipod_type, position, next_position):
                    # Never go backwards
                    continue
                if valid_next := self._get_valid_next_position(next_position, amphipod_type, position):
                    resulting_position, cost = valid_next
                    valid_nexts.append((resulting_position, amphipod_type, cost))

            return valid_nexts

    def _get_valid_next_position(self, next_position, amphipod_type, current_position):
        char_at_next = self.grid.get(next_position, '-1')
        if char_at_next != '.':
            return None
        if next_position in self.get_room_coords():
            my_room_coords = self.get_amphipod_to_room_coords()[amphipod_type]
            if next_position not in my_room_coords:
                # Never go in someone else's room
                return None
            else:
                # This is my room and next position is unoccupied. Make sure room is empty or has my type.
                if not self._room_occupied_by_stranger(amphipod_type):
                    return self._move_into_room(amphipod_type)
                else:
                    return None
        elif next_position[1] == 1:
            # In hallway
            if self._amphipod_is_stopped(amphipod_type, current_position):
                # I am stopped, I will only move if there is a clear path to my destination
                if result := self._path_to_desination(next_position, amphipod_type):
                    return result
                else:
                    return None
            else:
                # Otherwise we just have a regular forward move
                return (next_position, self.AMPHIPOD_TO_MOVE_COST[amphipod_type])

        raise Exception(next_position)

    def _path_to_desination(self, next_position, amphipod_type):
        my_room_x = list(self.get_amphipod_to_room_coords()[amphipod_type])[0][0]
        all_x_between = list(range(next_position[0], my_room_x + 1)) if my_room_x >= next_position[0] else list(range(my_room_x, next_position[0] + 1))
        if not all(self.grid[(x, 1)] == '.' for x in all_x_between):
            # Someone is blocking the hallway
            return None
        elif self._room_occupied_by_stranger(amphipod_type):
            return None
        else:
            # Give path from here to the lowest point in our room
            top_of_my_room = (my_room_x, 2)
            my_room_coords = self.get_amphipod_to_room_coords()[amphipod_type]
            final_position, cost_from_room_boundary_to_final_position = self._move_into_room(amphipod_type)

            cost_to_room_boundary = self.AMPHIPOD_TO_MOVE_COST[amphipod_type]*len(all_x_between)

            total_cost = cost_to_room_boundary + cost_from_room_boundary_to_final_position

            return (final_position, total_cost)

    def _move_into_room(self, amphipod_type):
        """
        We are at the edge of our own room and it is not occupied by strangers,
        so let's move into the lowest unoccupied position of our room.
        """
        my_room_coords = self.get_amphipod_to_room_coords()[amphipod_type]
        my_room_coords_sorted_by_y_ascending = sorted(list(my_room_coords), key=lambda x: x[1], reverse=True)

        for coord in my_room_coords_sorted_by_y_ascending:
            if self.grid[coord] == '.':
                cost = (coord[1] - 1) * self.AMPHIPOD_TO_MOVE_COST[amphipod_type]
                return (coord, cost)
        raise Exception("Could not find coord in room to move to")

    def path_out_of_room_is_clear(self, position):
        """
        I am in another's room and want to get out. Return True if I am at the
        edge of the room or if I am deeper in the room but the path out is clear.
        """
        my_x, my_y = position
        return my_y == 2 or all(self.grid[(my_x, y)] == '.' for y in range(my_y-1, 1, -1))

    def __repr__(self):
        self.print()
        return ''

    def print(self, file=None):
        _print_cave(self.grid, file=file)

    def print_game(self):
        current = self
        caves = []
        while current.previous_cave is not None:
            caves.append(current)
            current = current.previous_cave
        caves.append(current)
        for cave in reversed(caves):
            import time
            time.sleep(1)
            print(f"cost_so_far={cave.cost_so_far} cost_last_move={cave.cost_last_move}")
            _print_cave(cave.grid)
            print()

    def hash(self):
        return ''.join(str(k) + str(v) for k,v in self.grid.items())


class Cave1(Cave):

    AMPHIPOD_TO_ROOM_COORDS = {
        'A': {(3,2), (3,3)},
        'B': {(5,2), (5,3)},
        'C': {(7,2), (7,3)},
        'D': {(9,2), (9,3)},
    }

    ROOM_COORDS = set(c for i in AMPHIPOD_TO_ROOM_COORDS.values() for c in i)

    def __init__(self,
                 grid,
                 previous_cave,
                 last_move,
                 cost_last_move,
                 cost_so_far=0):
        Cave.__init__(self, grid, previous_cave, last_move, cost_last_move, cost_so_far=cost_so_far)

    def is_organized(self):
        return self.grid[(3, 3)] == self.grid[(3,2)] == 'A' \
            and self.grid[(5, 3)] == self.grid[(5,2)] == 'B' \
            and self.grid[(7, 3)] == self.grid[(7,2)] == 'C' \
            and self.grid[(9, 3)] == self.grid[(9,2)] == 'D'

    def create_new_cave(self, new_grid, last_move, cost, cost_so_far):
        return Cave1(new_grid, self, last_move, cost, cost_so_far=cost_so_far)

    def get_amphipod_to_room_coords(self):
        return self.AMPHIPOD_TO_ROOM_COORDS

    def get_room_coords(self):
        return self.ROOM_COORDS


class Cave2(Cave):

    AMPHIPOD_TO_ROOM_COORDS = {
        'A': {(3,2), (3,3), (3,4), (3,5)},
        'B': {(5,2), (5,3), (5,4), (5,5)},
        'C': {(7,2), (7,3), (7,4), (7,5)},
        'D': {(9,2), (9,3), (9,4), (9,5)},
    }

    ROOM_COORDS = set(c for i in AMPHIPOD_TO_ROOM_COORDS.values() for c in i)

    def __init__(self,
                 grid,
                 previous_cave,
                 last_move,
                 cost_last_move,
                 cost_so_far=0):
        Cave.__init__(self, grid, previous_cave, last_move, cost_last_move, cost_so_far=cost_so_far)
        if previous_cave is None:
            print("Inserting lines to grid for part 2")
            self._insert_lines_to_grid()

    def _insert_lines_to_grid(self):
        """
        Adding these lines to the grid per the instructions:

        #D#C#B#A#
        #D#B#A#C#
        """
        # Copy rows 3 and 4 to their new homes, 5 and 6
        for x, y in [c for c in self.grid]:
            if y == 3:
                self.grid[(x, 5)] = self.grid[(x, y)]
            if y == 4:
                self.grid[(x, 6)] = self.grid[(x, y)]
        # Add new row 3 and new row 4
        for x, char in enumerate(list('  #D#C#B#A#')):
            self.grid[(x, 3)] = char
        for x, char in enumerate(list('  #D#B#A#C#')):
            self.grid[(x, 4)] = char

    def is_organized(self):
        return all(self.grid[(3, y)] == 'A' for y in range(2, 6)) \
            and all(self.grid[(5, y)] == 'B' for y in range(2, 6)) \
            and all(self.grid[(7, y)] == 'C' for y in range(2, 6)) \
            and all(self.grid[(9, y)] == 'D' for y in range(2, 6))

    def create_new_cave(self, new_grid, last_move, cost, cost_so_far):
        return Cave2(new_grid, self, last_move, cost, cost_so_far=cost_so_far)

    def get_amphipod_to_room_coords(self):
        return self.AMPHIPOD_TO_ROOM_COORDS

    def get_room_coords(self):
        return self.ROOM_COORDS


def _parse_inputs(inputs):
    start = inputs[0].find('#')
    cave = {}
    for y, line in enumerate(inputs):
        x = start
        while x < len(line):
            if line[x]:
                cave[(x,y)] = line[x]
            x += 1
    return cave


def _print_cave(grid, i=0, file=None):
    if file is None:
        import sys
        file = sys.stdout
    max_x = max(i[0] for i in grid.keys())
    max_y = max(i[1] for i in grid.keys())
    buffer = '\t' * i
    for y in range(max_y + 1):
        print(buffer, end='', file=file)
        for x in range(max_x + 1):
            val = grid.get((x,y), ' ')
            print(str(val), end='', file=file)
        print()


def run_tests():
    test_inputs = """
#############
#...........#
###A#C#B#D###
  #A#C#B#D#
  #########
    """.strip().split('\n')

    cave = Cave1(_parse_inputs(test_inputs), None, None, None)
    if (result := cave.is_organized()) != False:
        raise Exception(result)

    test_inputs = """
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
    """.strip().split('\n')

    cave = Cave1(_parse_inputs(test_inputs), None, None, None)
    if (result := cave.is_organized()) != True:
        raise Exception(result)

    test_inputs = """
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########
    """.strip().split('\n')

    cave = Cave2(_parse_inputs(test_inputs), -1, None, None)
    if (result := cave.is_organized()) != True:
        raise Exception(result)

    test_inputs = """
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
    """.strip().split('\n')

    cave = Cave1(_parse_inputs(test_inputs), None, None, None)
    if (result := cave.is_organized()) != False:
        raise Exception(result)

    if (result := cave._get_valid_nexts_for_amphipod((7,3), 'C')) != []:
        raise Exception(result)

    test_inputs = """
#############
#.B....BC...#
###A#.#.#D###
  #A#C#.#D#
  #########
    """.strip().split('\n')
    cave = Cave1(_parse_inputs(test_inputs), None, None, None)
    if (result := cave._get_valid_nexts_for_amphipod((5,3), 'C')) != [((5,1), 'C', 200)]:
        raise Exception(result)

    # False because C is in the room
    if (result := cave._path_to_desination((4,1), 'B')) != None:
        raise Exception(result)

    test_inputs = """
#############
#.B...CBC...#
###A#.#.#D###
  #A#C#.#D#
  #########
    """.strip().split('\n')
    # Cannot move into non-destination room
    cave = Cave1(_parse_inputs(test_inputs), None, None, None)
    if (result := cave._get_valid_nexts_for_amphipod((7,1), 'B')) != []:
        raise Exception(result)

    if (result := cave._path_to_desination((5,1), 'C')) != None:
        raise Exception(result)

    test_inputs = """
#############
#..C..BCB...#
###A#.#.#D###
  #A#.#.#D#
  #########
    """.strip().split('\n')
    # Can move into room
    cave = Cave1(_parse_inputs(test_inputs), None, None, None)
    if (result := cave._get_valid_nexts_for_amphipod((7,1), 'C')) != [((7,3), 'C', 200)]:
        raise Exception(result)

    test_inputs = """
#############
#.....BCB...#
###A#.#.#D###
  #A#.#C#D#
  #########
    """.strip().split('\n')
    # Can move into room
    cave = Cave1(_parse_inputs(test_inputs), None, None, None)
    if (result := cave._get_valid_nexts_for_amphipod((7,1), 'C')) != [((7,2), 'C', 100)]:
        raise Exception(result)

    test_inputs = """
#############
#.....CCB...#
###A#.#.#D###
  #A#C#B#D#
  #########
    """.strip().split('\n')
    # Cannot move into room with wrong type in it
    cave = Cave1(_parse_inputs(test_inputs), None, None, None)
    if (result := cave._get_valid_nexts_for_amphipod((7,1), 'B')) != []:
        raise Exception(result)

    test_inputs = """
#############
#AAD......AA#
###.#B#C#.###
  #.#B#C#.#
  #.#B#C#D#
  #D#B#C#D#
  #########
  """.strip().split('\n')
    # D should go to its home
    cave = Cave2(_parse_inputs(test_inputs), -1, ((4, 1), (9, 4), 'D'), None)
    if (result := cave._get_valid_nexts_for_amphipod((3,1), 'D')) != [((9, 3), 'D', 8000)]:
        raise Exception(result)

    test_inputs = """
    #############
    #D.......D..#
    ###.#B#C#.###
      #A#B#C#A#
      #########
    """.strip().split('\n')
    cave = Cave1(_parse_inputs(test_inputs), None, ((7,2), (7,1), 'D'), None)
    if (result := cave._get_valid_nexts_for_amphipod((7,1), 'D')) != [((6, 1), 'D', 1000), ((8, 1), 'D', 1000)]:
        raise Exception(result)

    test_inputs = """
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 12521:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 44169:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(23)

    # result_1 = run_1(input)
    # print(f"Finished 1 with result {result_1}")

    # import pdb; pdb.set_trace()
    # 56256 too high
    # 52696 too high
    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
