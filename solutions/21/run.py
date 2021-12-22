from collections import defaultdict

from solutions.get_inputs import read_inputs


roll_to_num_universes = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1,
}

def run_1(inputs):
    p1_x, p2_x = _parse_input(inputs)
    p1_score, p2_score = 0, 0
    dice = Dice()
    max_score = 1000

    is_p1_turn = True
    while p1_score < max_score and p2_score < max_score:
        roll = dice.next_sum()
        if is_p1_turn:
            p1_x = _get_next_position(p1_x, roll)
            p1_score += p1_x
        else:
            p2_x = _get_next_position(p2_x, roll)
            p2_score += p2_x
        is_p1_turn = False if is_p1_turn else True
        # print(f'num_rolls={dice.total_rolls} p1_x={p1_x} p1_score={p1_score} p2_x={p2_x} p2_score={p2_score}')

    loser_score = p1_score if p1_score < 1000 else p2_score

    return loser_score * dice.total_rolls


def run_2(inputs):
    p1_x, p2_x = _parse_input(inputs)

    position_to_score_to_count_p1 = defaultdict(lambda: defaultdict(lambda: 0))
    position_to_score_to_count_p1[p1_x][0] = 1

    position_to_score_to_count_p2 = defaultdict(lambda: defaultdict(lambda: 0))
    position_to_score_to_count_p2[p2_x][0] = 1

    p1_win_count = 0
    p2_win_count = 0
    is_p1_turn = True
    i = 0
    while position_to_score_to_count_p1 and position_to_score_to_count_p2:
        i += 1
        print(i, p1_win_count, p2_win_count, len(position_to_score_to_count_p1), len(position_to_score_to_count_p2))
        # print(sum([j for i in position_to_score_to_count_p1.values() for j in i.values()]))
        # print(sum([j for i in position_to_score_to_count_p2.values() for j in i.values()]))
        print(max([j for i in position_to_score_to_count_p1.values() for j in i.keys()]))
        print(max([j for i in position_to_score_to_count_p2.values() for j in i.keys()]))
        if is_p1_turn:
            # new_dict = defaultdict(lambda: defaultdict(lambda: 0))
            # for position, score_to_count in position_to_score_to_count_p1.items():
            #     for score, count in score_to_count.items():
            #         for roll in range(3, 10):
            #             num_new_universes = roll_to_num_universes[roll]
            #             new_x = _get_next_position(position, roll)
            #             new_score = score + new_x
            #             if new_score >= 21:
            #                 p1_win_counter += num_new_universes
            #             else:
            #                 new_dict[new_x][new_score] += num_new_universes
            #
            #
            # position_to_score_to_count_p1 = new_dict
            new_dict, num_new_wins = _play_turn(position_to_score_to_count_p1)
            position_to_score_to_count_p1 = new_dict
            p1_win_count += num_new_wins
        else:
            new_dict, num_new_wins = _play_turn(position_to_score_to_count_p2)
            position_to_score_to_count_p2 = new_dict
            p2_win_count += num_new_wins

        is_p1_turn = False if is_p1_turn else True
        # import pdb; pdb.set_trace()
    return max(p1_win_count, p2_win_count)


def _play_turn(position_to_score_to_count):
    # import pdb; pdb.set_trace()
    num_new_wins = 0
    new_dict = defaultdict(lambda: defaultdict(lambda: 0))
    for position, score_to_count in position_to_score_to_count.items():
        for score, count in score_to_count.items():
            # for roll in range(3, 10):
                for i in range(3):
                    for j in range(3):
                        for k in range(3):
                            roll = i + j + k
                            # num_new_universes = roll_to_num_universes[roll]
                            new_x = _get_next_position(position, roll)
                            new_score = score + new_x
                            # num_universes = count + num_new_universes * count
                            num_universes = count
                            if new_score >= 21:
                                num_new_wins += num_universes
                            else:
                                new_dict[new_x][new_score] += num_universes
    return new_dict, num_new_wins


# def run_2(inputs):
#     p1_x, p2_x = _parse_input(inputs)
#     p1_won, p2_won = False, False
#
#     # p1_x, p1_score, p2_x, p2_score, is_p1_turn
#     first_game = (p1_x, 0, p2_x, 0, True)
#
#     # universes = 1
#
#     games = [first_game]
#     p1_win_counter = 0
#     p2_win_counter = 0
#     while games:
#         new_games = []
#         for game in games:
#             p1_x, p1_score, p2_x, p2_score, is_p1_turn = game
#             for roll in range(3, 10):
#                 num_new_universes = roll_to_num_universes[roll]
#                 # universes += num_new_universes
#                 p1_x, p1_score, p2_x, p2_score, is_p1_turn = game
#                 if is_p1_turn:
#                     p1_x = _get_next_position(p1_x, roll)
#                     p1_score += p1_x
#                     if p1_score >= 21:
#                         p1_win_counter += 1
#                     else:
#                         new_games += [(p1_x, p1_score, p2_x, p2_score, False)] * num_new_universes
#                 else:
#                     p2_x = _get_next_position(p2_x, roll)
#                     p2_score += p2_x
#                     if p2_score >= 21:
#                         p2_win_counter += 1
#                     else:
#                         new_games += [(p1_x, p1_score, p2_x, p2_score, True)] * num_new_universes
#         games = new_games
#         print(p1_win_counter, p2_win_counter, len(games))
#     return max(p1_win_count, p2_win_counter)


# def run_2(inputs):
#     p1_x, p2_x = _parse_input(inputs)
#     p1_won, p2_won = False, False
#
#     # p1_x, p1_score, p2_x, p2_score, is_p1_turn
#     first_game = (p1_x, 0, p2_x, 0, True)
#
#     universes = 1
#
#     games = [first_game]
#     p1_win_counter = 0
#     p2_win_counter = 0
#     while games:
#         new_games = []
#         for game in games:
#             p1_x, p1_score, p2_x, p2_score, is_p1_turn = game
#             for roll_1 in range(1, 4):
#                 universes += 1
#                 for roll_2 in range(1, 4):
#                     universes += 1
#                     for roll_3 in range(1, 4):
#                         universes += 1
#                         p1_x, p1_score, p2_x, p2_score, is_p1_turn = game
#                         roll = roll_1 + roll_2 + roll_3
#                         if is_p1_turn:
#                             p1_x = _get_next_position(p1_x, roll)
#                             p1_score += p1_x
#                             if p1_score >= 21:
#                                 # p1_won = True
#                                 p1_win_counter += 1
#                             else:
#                                 new_games.append((p1_x, p1_score, p2_x, p2_score, False))
#                         else:
#                             p2_x = _get_next_position(p2_x, roll)
#                             p2_score += p2_x
#                             if p2_score >= 21:
#                                 # p2_won = True
#                                 p2_win_counter += 1
#                             else:
#                                 new_games.append((p1_x, p1_score, p2_x, p2_score, True))
#                         # if p1_won and p2_won:
#                         #     # return universes + len(new_games)
#                         #     return universes
#         games = new_games
#         # universes *= len(games)
#         # max_1 = max(g[1] for g in games)
#         # max_2 = max(g[3] for g in games)
#         # print(f'{len(games)} universes max_1={max_1} max_2={max_2}')
#         # print(f'{universes} universes max_1={max_1} max_2={max_2}')
#         print(universes)
#     return max(p1_win_counter, p2_win_counter)


def _get_next_position(current_x, roll, board_size=10):
    next = (current_x + roll) % board_size
    return board_size if next == 0 else next


class Dice:

    def __init__(self):
        self.current_value = 0
        self.total_rolls = 0

    def next_sum(self):
        val = 0
        for _ in range(3):
            next_roll = self.next()
            val += next_roll
        return val

    def next(self):
        if self.current_value < 100:
            self.current_value += 1
        else:
            self.current_value = 1
        self.total_rolls += 1
        return self.current_value

    def __repr__(self):
        return f'value={self.current_value}'


def _parse_input(inputs):
    p1_x = int(inputs[0].split('position: ')[-1].strip())
    p2_x = int(inputs[1].split('position: ')[-1].strip())
    return p1_x, p2_x


def run_tests():
    if (result := _get_next_position(7, 5)) != 2:
        raise Exception(result)

    if (result := _get_next_position(2, 5)) != 7:
        raise Exception(result)

    if (result := _get_next_position(7, 10)) != 7:
        raise Exception(result)

    if (result := _get_next_position(7, 21)) != 8:
        raise Exception(result)

    if (result := _get_next_position(7, 25)) != 2:
        raise Exception(result)

    if (result := _get_next_position(7, 3)) != 10:
        raise Exception(result)

    if (result := _get_next_position(8, 15)) != 3:
        raise Exception(result)

    test_inputs = """
    Player 1 starting position: 4
    Player 2 starting position: 8
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 739785:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 444356092776315:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(21)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
