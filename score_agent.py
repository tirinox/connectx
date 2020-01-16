import numpy as np
import random

# from util import print_board


def calculate_score_for_player(board: np.ndarray, player, in_a_row):
    rows, cols = board.shape

    score = 0

    non_empty = board != 0
    bottom_support = np.ones((cols,), dtype=np.bool)
    supports = np.vstack((non_empty[1:, :], bottom_support))

    def score_for_line(start_col, start_row, dx, dy, steps):
        if steps <= 0:
            return 0

        nonlocal score
        my, empty, supported = 0, 0, 0

        # b2 = np.zeros_like(board)
        # if start_col == 1 and start_row == 2 and dx == 1 and dy == 1:
        #     print_board(b2)

        for elem in range(in_a_row):
            c = start_col + elem * dx
            r = start_row + elem * dy
            cell = board[r, c]
            if cell == player:
                my += 1
            elif cell == 0:
                empty += 1
                if supports[r, c]:
                    supported += 1

            # b2[r, c] = 1

        if my + empty == in_a_row and my != 0:
            if my == in_a_row:
                score += 100000
            else:
                delta = 10 ** (in_a_row - empty - 1)
                if my > 1 and supported < empty:
                    delta //= 2
                score += delta

    for col in range(cols):
        for row in range(rows):
            steps_left = cols - in_a_row - col + 1
            steps_right = col - in_a_row + 2
            steps_down = rows - in_a_row - row + 1

            score_for_line(col, row, 1, 0, steps_left)
            score_for_line(col, row, 0, 1, steps_down)

            # diagonal left+down
            score_for_line(col, row, 1, 1, min(steps_left, steps_down))

            # diagonal right+down
            score_for_line(col, row, -1, 1, min(steps_right, steps_down))

    return score


def drop_a_checker(board, column_no, player):
    # check choice-column for free space to drop a chip
    column = board[:, column_no]
    top_row = -1
    for r in reversed(range(board.shape[0])):
        if column[r] == 0:
            top_row = r
            break

    if top_row == -1:
        return None  # no free space in the column

    new_board = board.copy()
    new_board[top_row, column_no] = player
    return new_board


def agent(observation, configuration):
    columns = configuration.columns
    rows = configuration.rows
    in_a_row = configuration.inarow
    board = observation.board

    # which player I am!
    mark = observation.mark
    opp = 1 if mark == 2 else 2

    current_board = np.array(board, dtype=np.uint8).reshape((rows, columns))

    # print('-' * 100)
    # print_board(current_board)

    best_choice = -1
    best_score = -np.inf
    for choice in range(columns):
        new_board_my = drop_a_checker(current_board, choice, mark)
        if new_board_my is None:
            continue

        if np.all(new_board_my != 0):  # this is last cell
            return choice

        # print('-----')

        my_score = calculate_score_for_player(new_board_my, mark, in_a_row)

        for opp_choice in range(columns):
            new_board_opp = drop_a_checker(new_board_my, opp_choice, opp)
            if new_board_opp is None:
                continue

            opp_score = calculate_score_for_player(new_board_opp, opp, in_a_row)
            score = my_score - 3 * opp_score

            # print(f'[ch={choice}/{opp_choice}] my score = {my_score}; opp score = {opp_score}; score = {score} of best {best_score}')

            if score > best_score:
                best_score = score
                best_choice = choice
            elif score == best_score:
                best_choice = random.choice((choice, best_choice))

    # return a column to play: [0, configuration.columns)
    return best_choice
