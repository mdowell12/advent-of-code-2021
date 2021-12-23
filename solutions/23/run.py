from solutions.get_inputs import read_inputs

"""
Each turn, one of the eight amphipods must move, and each has max of three moves it can make
We can keep a tree of (energy spent this turn, all current positions) and for each turn evaluate
each leaf node and add new leaves for every possible move that could be made. Branches terminate
when either the cave is organized or no possible moves can be made.

# DONE model the cave - (x,y) coordinate system with bounds, or dict that maps coordinate to X, . or amphipod?
# DONE parse input
# TODO create the tree data structure. BFS with queue of still processing caves and add to "finished" list of organized caves that can each reference previous and calc total cost.
# TODO figure out how to keep state across moves so we can do things like "do not stop in front of room"
# WIP Function to determine all possible moves each amphipod can make with a given configuration
    - needs to take into account not stopping in front of room
    - needs to take into account that if in hallway and stops, is locked until it can move fully into its room
    - needs to filter valid moves when one results in amphipod in its destination room
    - needs to move amphipod in top of room to bottom if possible
# TODO Function to do the move
# DONE Function to determine if cave is organized
"""

def run_1(inputs):
    cave = Cave(_parse_inputs(inputs), None, None, None)
    cave.print()
    caves = [cave]
    finished = []
    while caves:
        cave = caves.pop(0)
        next_caves = cave.get_next_caves()
        for next_cave in next_caves:
            if next_cave.is_organized():
                import pdb; pdb.set_trace()
                finished.append(next_cave)
            else:
                caves.append(next_cave)
        else:
            cave.print()
        print('iterated')

    costs = [c.get_total_cost() for c in finished]
    return min(costs)


def run_2(inputs):
    pass


class Cave:

    AMPHIPOD_TO_MOVE_COST = {
        'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000,
    }

    AMPHIPOD_TO_ROOM_COORDS = {
        'A': {(3,2), (3,3)},
        'B': {(5,2), (5,3)},
        'C': {(7,2), (7,3)},
        'D': {(9,2), (9,3)},
    }

    ROOM_COORDS = set(c for i in AMPHIPOD_TO_ROOM_COORDS.values() for c in i)

    OUTSIDE_ROOM_TO_TYPE = {
        (3,1): 'A',
        (5,1): 'B',
        (7,1): 'C',
        (9,1): 'D',
    }

    def __init__(self, grid, previous_cave, last_move, cost_last_move):
        self.grid = grid
        self.previous_cave = previous_cave
        self.last_move = last_move
        self.cost_last_move = cost_last_move

    def is_organized(self):
        return self.grid[(3, 3)] == self.grid[(3,2)] == 'A' \
            and self.grid[(5, 3)] == self.grid[(5,2)] == 'B' \
            and self.grid[(7, 3)] == self.grid[(7,2)] == 'C' \
            and self.grid[(9, 3)] == self.grid[(9,2)] == 'D'

    def get_next_caves(self):
        next_moves = self.get_next_moves()
        result = []
        for original_position, moves in next_moves.items():
            for next_position, amphipod_type, cost in moves:
                new_grid = {k: v for k, v in self.grid.items()}
                new_grid[original_position] = '.'
                new_grid[next_position] = amphipod_type
                last_move = (next_position, amphipod_type)
                result.append(Cave(new_grid, self, last_move, cost))
        return result

    def get_next_moves(self):
        """
        For each amphipod (position, type), determine all adjacent coordinates
        that are a valid move and return along with cost.
        :return: dict[original position] -> list[(next position, type, cost of move)]
        """
        amphipods = [tup for tup in self.grid.items() if tup[1] in self.AMPHIPOD_TO_MOVE_COST.keys()]
        result = {}
        # import pdb; pdb.set_trace()
        for position, amphipod_type in amphipods:
            valid_nexts = self._get_valid_nexts_for_amphipod(position, amphipod_type)
            if valid_nexts:
                result[position] = valid_nexts
        return result

    def get_total_cost(self):
        cost = 0
        current = self
        while current.cost_last_move is not None:
            cost += current.cost_last_move
            current = current.previous_cave
        cost += current.cost_last_move
        return cost

    def _get_valid_nexts_for_amphipod(self, position, amphipod_type):
        if position in self.ROOM_COORDS:
            if position in self.AMPHIPOD_TO_ROOM_COORDS[amphipod_type]:
                return []
            elif self.grid[(position[0], 1)] == '.':
                return [((position[0], 1), amphipod_type, self.AMPHIPOD_TO_MOVE_COST[amphipod_type] * (position[1]-1))]
            else:
                return []

        valid_nexts = []
        adjacents = [
            (position[0]-1, position[1]),
            (position[0]+1, position[1]),
            (position[0], position[1]-1),
            (position[0], position[1]+1),
        ]

        # Prefer going to the room
        if to_room := [a for a in adjacents if a in self.AMPHIPOD_TO_ROOM_COORDS[amphipod_type]]:
            adjacents = to_room

        for next_position in adjacents:
            if (next_position, amphipod_type) == self.last_move:
                # Never go backwards
                continue
            if valid_next := self._get_valid_next_position(next_position, amphipod_type):
                resulting_position, cost = valid_next
                valid_nexts.append((resulting_position, amphipod_type, cost))
        return valid_nexts

    def _get_valid_next_position(self, next_position, amphipod_type):
        # TODO may need to make this return list of all possible resulting positions from next_position
        char_at_next = self.grid.get(next_position, '-1')
        if char_at_next != '.':
            return None
        if next_position in self.ROOM_COORDS:
            my_room_coords = self.AMPHIPOD_TO_ROOM_COORDS[amphipod_type]
            if next_position not in my_room_coords:
                return None
            else:
                # This is my room and next position is unoccupied. Make sure room is empty or has my type.
                if not self._room_occupied_by_stranger(amphipod_type):
                    if all(self.grid[c] == '.' for c in my_room_coords):
                        # Move to bottom
                        x,y = next_position
                        return ((x, y+1), 2*self.AMPHIPOD_TO_MOVE_COST[amphipod_type])
                    else:
                        return (next_position, self.AMPHIPOD_TO_MOVE_COST[amphipod_type])
                else:
                    return None
        elif next_position[1] == 1:
            # In hallway
            if self.last_move[1] != amphipod_type:
                # I am stopped, I will only move if there is a clear path to my destination
                if self._path_to_desination_unblocked(next_position, amphipod_type):
                    return (next_position, self.AMPHIPOD_TO_MOVE_COST[amphipod_type])
                else:
                    return None

        return (next_position, self.AMPHIPOD_TO_MOVE_COST[amphipod_type])

        # raise Exception(f'{self, next_position, amphipod_type}')
        # return (next_position, self.AMPHIPOD_TO_MOVE_COST[amphipod_type])

    def _path_to_desination_unblocked(self, next_position, amphipod_type):
        my_room_x = list(self.AMPHIPOD_TO_ROOM_COORDS[amphipod_type])[0][0]
        all_x_between = list(range(next_position[0], my_room_x + 1)) if my_room_x >= next_position[0] else list(range(my_room_x, next_position[0] + 1))
        if not all(self.grid[(x, 1)] == '.' for x in all_x_between):
            return False
        elif self._room_occupied_by_stranger(amphipod_type):
            return False
        else:
            return True

    def _room_occupied_by_stranger(self, amphipod_type):
        my_room_coords = self.AMPHIPOD_TO_ROOM_COORDS[amphipod_type]
        return not all(self.grid[c] in {amphipod_type, '.'} for c in my_room_coords)

    def __repr__(self):
        return self.grid

    def print(self):
        _print_cave(self.grid)

    def print_game(self):
        current = self
        while current.previous_cave is not None:
            _print_cave(current)
            print(current.cost_last_move)
            current = current.previous_cave
        _print_cave(current)
        print(current.cost_last_move)


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


def _print_cave(grid):
    max_x = max(i[0] for i in grid.keys())
    max_y = max(i[1] for i in grid.keys())
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            val = grid.get((x,y), ' ')
            # if val == 0:
            #     print('\033[1;31m' + str(val), end=' ')
            # else:
            #     print("\033[0;0m" + str(val), end=' ')
            print(str(val), end='')
        print()


def run_tests():
    test_inputs = """
#############
#...........#
###A#C#B#D###
  #A#C#B#D#
  #########
    """.strip().split('\n')

    cave = Cave(_parse_inputs(test_inputs), None, None, None)
    if (result := cave.is_organized()) != False:
        raise Exception(result)

    test_inputs = """
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
    """.strip().split('\n')

    cave = Cave(_parse_inputs(test_inputs), None, None, None)
    if (result := cave.is_organized()) != True:
        raise Exception(result)

    test_inputs = """
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
    """.strip().split('\n')

    cave = Cave(_parse_inputs(test_inputs), None, None, None)
    if (result := cave.is_organized()) != False:
        raise Exception(result)

    if (result := cave._get_valid_nexts_for_amphipod((7,3), 'C')) != []:
        raise Exception(result)

#     test_inputs = """
# #############
# #.B....BC...#
# ###A#.#.#D###
#   #A#C#.#D#
#   #########
#     """.strip().split('\n')
#     cave = Cave(_parse_inputs(test_inputs), None, None, None)
#     if (result := cave._get_valid_nexts_for_amphipod((5,3), 'C')) != [((6,1), 'C', 300)]:
#         raise Exception(result)

    test_inputs = """
#############
#.B....BC...#
###A#.#.#D###
  #A#C#.#D#
  #########
    """.strip().split('\n')
    cave = Cave(_parse_inputs(test_inputs), None, None, None)
    if (result := cave._get_valid_nexts_for_amphipod((5,3), 'C')) != [((5,1), 'C', 200)]:
        raise Exception(result)

    # False because C is in the room
    if (result := cave._path_to_desination_unblocked((4,1), 'B')) != False:
        raise Exception(result)

    test_inputs = """
#############
#.B...CBC...#
###A#.#.#D###
  #A#C#.#D#
  #########
    """.strip().split('\n')
    # Cannot move into non-destination room
    cave = Cave(_parse_inputs(test_inputs), None, None, None)
    if (result := cave._get_valid_nexts_for_amphipod((7,1), 'B')) != []:
        raise Exception(result)

    if (result := cave._path_to_desination_unblocked((5,1), 'C')) != False:
        raise Exception(result)

    test_inputs = """
#############
#..C..BCB...#
###A#.#.#D###
  #A#.#.#D#
  #########
    """.strip().split('\n')
    # Can move into room
    cave = Cave(_parse_inputs(test_inputs), None, None, None)
    if (result := cave._get_valid_nexts_for_amphipod((7,1), 'C')) != [((7,3), 'C', 200)]:
        raise Exception(result)

    if (result := cave._path_to_desination_unblocked((5,1), 'B')) != True:
        raise Exception(result)

    test_inputs = """
#############
#.....BCB...#
###A#.#.#D###
  #A#.#C#D#
  #########
    """.strip().split('\n')
    # Can move into room
    cave = Cave(_parse_inputs(test_inputs), None, None, None)
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
    cave = Cave(_parse_inputs(test_inputs), None, None, None)
    if (result := cave._get_valid_nexts_for_amphipod((7,1), 'B')) != []:
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

    # result_2 = run_2(test_inputs)
    # if result_2 != 0:
    #     raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(23)

    # result_1 = run_1(input)
    # print(f"Finished 1 with result {result_1}")

    # result_2 = run_2(input)
    # print(f"Finished 2 with result {result_2}")
