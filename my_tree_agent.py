import numpy as np


def check_game_over(board: np.ndarray, in_a_row):
    """ Check if game over
    :param board: np.ndarray of the board [row, col]
    :param in_a_row: to win
    :return: 0 if no winner yet, else winner's mark 1 or 2
    """

    def test_lines(board):
        xdim, ydim = board.shape

        for x in range(xdim):
            n, old = 0, 0
            for y in range(ydim):
                current = board[x, y]
                if current != 0:
                    if old == 0:
                        n, old = 1, current
                    elif old == current:
                        n += 1
                        if n == in_a_row:
                            return current
                    else:
                        n, old = 0, current
                else:
                    n, old = 0, 0
        return 0

    r = test_lines(board)
    if r != 0:
        return r

    return test_lines(board.T)


def calculate_score_for_player(board: np.ndarray, player, in_a_row):
    def inner(board: np.ndarray, player, rotated=True):

        board = board.T if rotated else board
        rows, cols = board.shape
        normal = not rotated
        score = 0

        support_row = [True] * cols

        for row_index in reversed(range(rows)):
            row = board[row_index]

            for c in range(cols - in_a_row + 1):
                my, empty, supports = 0, 0, 0
                for k in range(c, in_a_row + c):
                    if row[k] == player:
                        my += 1
                    elif row[k] == 0:
                        empty += 1
                    else:
                        break
                    if support_row[k]:
                        supports += 1

                if my + empty == in_a_row:
                    delta = 10 ** (my - 1)
                    if normal and supports < in_a_row:
                        delta //= 2
                    score += delta

            support_row = row != 0

        return score

    return inner(board, player, rotated=False) + \
           inner(board, player, rotated=True)


def agent(observation, configuration):
    columns = configuration.columns
    rows = configuration.rows
    in_a_row = configuration.inarow
    board = observation.board

    # which player I am!
    mark = observation.mark

    current_board = np.array(observation['board'], dtype=np.uint8).reshape((rows, columns))

    # return a column to play: [0, configuration.columns)
    return 0


def test_game_over():
    board = np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 2],
        [2, 2, 0, 2, 0, 0, 2],
        [1, 0, 0, 2, 2, 2, 1],
        [1, 0, 1, 1, 1, 1, 0],
    ], dtype=np.uint8)

    print(check_game_over(board, 4))



def test_score():
    board = np.array([
        [0, 0, 0, 0, 0, 2, 0],
        [1, 1, 2, 1, 0, 1, 0],
        [2, 1, 1, 2, 1, 1, 0],
        [1, 2, 1, 1, 2, 1, 1],
    ], dtype=np.uint8)

    # print(make_score_not_my(board))
    print(calculate_score_for_player(board, 1, in_a_row=4))


test_score()
# test()
