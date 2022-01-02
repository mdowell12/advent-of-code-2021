from solutions.get_inputs import read_inputs

"""
Each turn, one of the eight amphipods must move, and each has max of three moves it can make
We can keep a tree of (energy spent this turn, all current positions) and for each turn evaluate
each leaf node and add new leaves for every possible move that could be made. Branches terminate
when either the cave is organized or no possible moves can be made.

# DONE model the cave - (x,y) coordinate system with bounds, or dict that maps coordinate to X, . or amphipod?
# DONE parse input
# DONE create the tree data structure. BFS with queue of still processing caves and add to "finished" list of organized caves that can each reference previous and calc total cost.
# WIP Function to determine all possible moves each amphipod can make with a given configuration
    - needs to take into account not stopping in front of room
    - needs to take into account that if in hallway and stops, is locked until it can move fully into its room
    - needs to filter valid moves when one results in amphipod in its destination room
    - needs to move amphipod in top of room to bottom if possible
# DONE Function to do the move
# DONE Function to determine if cave is organized

# OPTIMIZE:
  - TODO If game has finished, begin cutting off any other games that have higher score
"""

def run_1(inputs):
    cave = Cave(_parse_inputs(inputs), None, None, None, cost_so_far=0)
    caves = [cave]
    lowest_cave = None
    hash_to_score = {}
    lowest_score = None
    i = 0
    while caves:
        i+=1

        cave = caves.pop(0)
        # cave_cost = cave.get_total_cost()

        # if lowest_score is not None and cave_cost >= lowest_score:
        #     # print(f"Skipped cave because cave cost {cave_cost} is bigger than lowest score {lowest_score}")
        #     continue

        # hash = cave.hash()
        # hashed_score = hash_to_score.get(hash)
        # if hashed_score is None or cave_cost < hashed_score:
        #     hash_to_score[hash] = cave_cost
        # else:
        #     continue

        next_caves = cave.get_next_caves()
        for next_cave in next_caves:
            hash = next_cave.hash()
            current_cost = next_cave.get_total_cost()
            # if lowest_score is not None and current_cost >= lowest_score:
            #     print(f"Skipped cave because current cost {current_cost} is bigger than lowest score {lowest_score}")
            #     continue
            if next_cave.is_organized():
                # import pdb; pdb.set_trace()
                # print(f'cave finished with score {next_cave.get_total_cost()}')
                if lowest_score is None or current_cost < lowest_score:
                    lowest_score = current_cost
                    lowest_cave = next_cave
                    # print(f'before {len(caves)}')
                    # caves = [c for c in caves if c.get_total_cost() < lowest_score]
                    # print(f'after {len(caves)}')
                continue
                # finished.append(next_cave)
            if hashed_score := hash_to_score.get(hash):
                if current_cost >= hashed_score:
                    continue
                else:
                    hash_to_score[hash] = current_cost
            else:
                hash_to_score[hash] = current_cost
            # print(current_cost)

            caves.append(next_cave)

        if i % 100000 == 0:
            # cave.print_game()
            # cave.print()
            print(i, len(caves), lowest_score)
    # import pdb; pdb.set_trace()
    # lowest_cave.to_file()
    print(f'final {lowest_score}')
    return lowest_score


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

    AMPHIPODS = set(AMPHIPOD_TO_ROOM_COORDS.keys())

    ROOM_COORDS = set(c for i in AMPHIPOD_TO_ROOM_COORDS.values() for c in i)

    OUTSIDE_ROOM_TO_TYPE = {
        (3,1): 'A',
        (5,1): 'B',
        (7,1): 'C',
        (9,1): 'D',
    }

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
                last_move = (original_position, next_position, amphipod_type)
                cost_so_far = self.cost_so_far + cost
                result.append(Cave(new_grid, self, last_move, cost, cost_so_far=cost_so_far))
        return result

    def get_next_moves(self):
        """
        For each amphipod (position, type), determine all adjacent coordinates
        that are a valid move and return along with cost.
        :return: dict[original position] -> list[(next position, type, cost of move)]
        """
        amphipods = [tup for tup in self.grid.items() if tup[1] in self.AMPHIPOD_TO_MOVE_COST.keys()]
        result = {}

        for position, amphipod_type in amphipods:
            valid_nexts = self._get_valid_nexts_for_amphipod(position, amphipod_type)
            if valid_nexts:
                result[position] = valid_nexts
        return result

    def get_total_cost(self):
        # cost = 0
        # current = self
        # while current.cost_last_move is not None:
        #     cost += current.cost_last_move
        #     current = current.previous_cave
        # if current.cost_last_move:
        #     cost += current.cost_last_move
        # assert self.cost_so_far == cost
        return self.cost_so_far

    def _get_valid_nexts_for_amphipod(self, position, amphipod_type):
        # if amphipod_type == 'D': import pdb; pdb.set_trace()
        if position in self.ROOM_COORDS:
            if position in self.AMPHIPOD_TO_ROOM_COORDS[amphipod_type] and not self._room_occupied_by_stranger(amphipod_type):
                return []
            # Move out of other home
            elif (position[1] == 2 or self.grid[(position[0], position[1] - 1)] == '.')  and self.grid[(position[0], 1)] == '.':
                return [((position[0], 1), amphipod_type, self.AMPHIPOD_TO_MOVE_COST[amphipod_type] * (position[1]-1))]
            # No moves
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
        if not self._room_occupied_by_stranger(amphipod_type):
            if to_room := [a for a in adjacents if a in self.AMPHIPOD_TO_ROOM_COORDS[amphipod_type]]:
                adjacents = to_room

        for next_position in adjacents:
            # if self.last_move: import pdb; pdb.set_trace()
            if self.last_move and self.last_move[0] == next_position:
                # Never go backwards
                continue
            if valid_next := self._get_valid_next_position(next_position, amphipod_type, position):
                resulting_position, cost = valid_next
                valid_nexts.append((resulting_position, amphipod_type, cost))
        # if self.grid[(9,1)] == 'D' and self.grid[(1,1)] == 'D' and amphipod_type == 'D':
        #     import pdb; pdb.set_trace()

        return valid_nexts

    def _get_valid_next_position(self, next_position, amphipod_type, current_position):
        # TODO may need to make this return list of all possible resulting positions from next_position
        char_at_next = self.grid.get(next_position, '-1')
        if char_at_next != '.':
            return None
        if next_position in self.ROOM_COORDS:
            my_room_coords = self.AMPHIPOD_TO_ROOM_COORDS[amphipod_type]
            if next_position not in my_room_coords:
                # Never go in someone elses room
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
            if self._amphipod_is_stopped(amphipod_type, current_position):
                # # I just came out of another persons room so allow move
                # if self.last_move[0][1] in {2,3}:
                #     return (next_position, self.AMPHIPOD_TO_MOVE_COST[amphipod_type])
                # I am stopped, I will only move if there is a clear path to my destination
                if result := self._path_to_desination(next_position, amphipod_type):
                    return result
                else:
                    return None
            else:
                return (next_position, self.AMPHIPOD_TO_MOVE_COST[amphipod_type])

        raise Exception(next_position)
        # return (next_position, self.AMPHIPOD_TO_MOVE_COST[amphipod_type])

    def _amphipod_is_stopped(self, amphipod_type, current_position):
        """
        amphipod is stopped if the last move was made by another amphipod
        """
        # import pdb; pdb.set_trace()
        return self.last_move[2] != amphipod_type or self.last_move[1] != current_position

    # def _path_to_desination_unblocked(self, next_position, amphipod_type):
    #     my_room_x = list(self.AMPHIPOD_TO_ROOM_COORDS[amphipod_type])[0][0]
    #     all_x_between = list(range(next_position[0], my_room_x + 1)) if my_room_x >= next_position[0] else list(range(my_room_x, next_position[0] + 1))
    #     if not all(self.grid[(x, 1)] == '.' for x in all_x_between):
    #         return False
    #     elif self._room_occupied_by_stranger(amphipod_type):
    #         return False
    #     else:
    #         return True

    def _path_to_desination(self, next_position, amphipod_type):
        my_room_x = list(self.AMPHIPOD_TO_ROOM_COORDS[amphipod_type])[0][0]
        all_x_between = list(range(next_position[0], my_room_x + 1)) if my_room_x >= next_position[0] else list(range(my_room_x, next_position[0] + 1))
        if not all(self.grid[(x, 1)] == '.' for x in all_x_between):
            return None
        elif self._room_occupied_by_stranger(amphipod_type):
            return None
        else:
            bottom_occupied = self.grid[(my_room_x, 3)] != '.'
            final_position = (my_room_x, 2) if bottom_occupied else (my_room_x, 3)
            to_room_multiplier = 1 if bottom_occupied else 2
            total_cost = self.AMPHIPOD_TO_MOVE_COST[amphipod_type]*len(all_x_between) + self.AMPHIPOD_TO_MOVE_COST[amphipod_type]*to_room_multiplier
            return (final_position, total_cost)

    def _room_occupied_by_stranger(self, amphipod_type):
        my_room_coords = self.AMPHIPOD_TO_ROOM_COORDS[amphipod_type]
        return not all(self.grid[c] in {amphipod_type, '.'} for c in my_room_coords)

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
        for i, cave in enumerate(reversed(caves)):
            _print_cave(cave.grid, i=i)

    def to_file(self):
        current = self
        caves = []
        while current.previous_cave is not None:
            caves.append(current)
            current = current.previous_cave
        caves.append(current)
        with open('/tmp/aoc_24_debug.txt', 'w') as f:
            f.write('last_move  last_score  current_score')
            for i, cave in enumerate(reversed(caves)):
                # cave.print(file=f)
                f.write(f'{cave.last_move} {cave.cost_last_move} {cave.cost_so_far}')
                f.write('\n')

    def hash(self):
        # return ''.join(str(k) + str(v) for k,v in self.grid.items() if v in self.AMPHIPODS) + str(self.last_move)
        return ''.join(str(k) + str(v) for k,v in self.grid.items())


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
            # if val == 0:
            #     print('\033[1;31m' + str(val), end=' ')
            # else:
            #     print("\033[0;0m" + str(val), end=' ')
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

    # # False because C is in the room
    # if (result := cave._path_to_desination_unblocked((4,1), 'B')) != False:
    #     raise Exception(result)
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
    cave = Cave(_parse_inputs(test_inputs), None, None, None)
    if (result := cave._get_valid_nexts_for_amphipod((7,1), 'B')) != []:
        raise Exception(result)

    # if (result := cave._path_to_desination_unblocked((5,1), 'C')) != False:
    #     raise Exception(result)
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
    cave = Cave(_parse_inputs(test_inputs), None, None, None)
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
    #D.......D..#
    ###.#B#C#.###
      #A#B#C#A#
      #########
    """.strip().split('\n')
    cave = Cave(_parse_inputs(test_inputs), None, ((7,2), (7,1), 'D'), None)
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

    # result_2 = run_2(test_inputs)
    # if result_2 != 0:
    #     raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(23)

    # 16312 too high
    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    # result_2 = run_2(input)
    # print(f"Finished 2 with result {result_2}")
