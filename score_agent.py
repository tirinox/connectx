import numpy as np


def calculate_score_for_player(board: np.ndarray, player, in_a_row):
    rows, cols = board.shape

    score = 0

    non_empty = board != 0
    bottom_support = np.ones((cols,), dtype=np.bool)
    supports = np.vstack((non_empty[1:, :], bottom_support))


    def score_for_line(start_col, start_row, dx, dy, steps):
        score = 0
        for step in range(steps):
            my, empty, supported = 0, 0, 0
            for elem in range(in_a_row):
                c = start_col + (elem + step) * dx
                r = start_row + (elem + step) * dy
                cell = board[r, c]
                if cell == player:
                    my += 1
                    if supports[r, c]:
                        supported += 1
                elif cell == 0:
                    empty += 1
            if my + empty == in_a_row and my != 0:
                plen = in_a_row - empty
                print(f'plen = {plen}')

                delta = 10 ** (in_a_row - empty - 1)
                if supported < in_a_row:
                    delta //= 2
                score += delta

        return score

    for col in range(cols):
        for row in range(rows):
            steps_left = cols - in_a_row - col + 1
            steps_right = col - in_a_row + 2
            steps_down = rows - in_a_row - row + 1

            print(f'col = {col}; row = {row}; left = {steps_left}; down = {steps_down}; right = {steps_right}')

            score += score_for_line(col, row, 1, 0, steps_left)
            score += score_for_line(col, row, 0, 1, steps_down)

            # diagonal left+down
            score += score_for_line(col, row, 1, 1, min(steps_left, steps_down))

            # diagonal right+down
            score += score_for_line(col, row, -1, 1, min(steps_right, steps_down))

    return score


def test_score():
    board = np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 2, 0, 2, 0],
        [0, 0, 2, 1, 1, 1, 2],
        [0, 0, 2, 1, 2, 1, 1],
    ], dtype=np.uint8)

    # board = np.array([
    #     [0, 0, 0],
    #     [0, 0, 2],
    #     [0, 1, 1],
    # ], dtype=np.uint8)

    board = np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 2, 1, 0, 0, 0, 0],
        [0, 2, 2, 1, 2, 0, 0],
        [0, 1, 2, 2, 1, 2, 0],
    ], dtype=np.uint8)

    rows, cols = board.shape
    print(f'total rows = {rows}; cols = {cols}')

    # print(make_score_not_my(board))
    print(calculate_score_for_player(board, 1, in_a_row=4))


if __name__ == '__main__':
    test_score()
