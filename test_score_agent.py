import numpy as np
from score_agent import calculate_score_for_player, agent
from util import conf_observation_from_board


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
    print(calculate_score_for_player(board, 2, in_a_row=4))


def test_score_a2():
    board = np.array([
        [2, 1, 1, 2, 0, 1, 2],
        [1, 2, 2, 1, 1, 2, 1],
        [2, 1, 1, 2, 2, 1, 2],
        [1, 2, 2, 1, 1, 2, 1],
        [2, 1, 1, 2, 2, 1, 2],
        [1, 2, 2, 1, 1, 2, 1],
    ], dtype=np.uint8)

    a = agent(*conf_observation_from_board(board))

    print(a)



if __name__ == '__main__':
    test_score_a2()
