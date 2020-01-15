import os
import numpy as np
import tempfile
from unittest.mock import MagicMock as Bunch


def show_html(html):
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', delete=False, suffix='.html') as f:
        f.write(html)
        os.system(f'open {f.name}')


def print_board(board):
    rows, cols = board.shape
    s = ''
    for r in range(rows):
        for c in range(cols):
            x = board[r, c]
            if x == 2:
                s += 'o'
            elif x == 1:
                s += 'x'
            else:
                s += '.'
        s += '\n'
    print(s)


def conf_observation_from_board(board, me=1, in_a_row=4):
    rows, cols = board.shape

    flat_board = board.reshape((rows * cols)).tolist()

    config = Bunch(columns=cols, rows=rows, inarow=in_a_row)
    observ = Bunch(mark=me, board=flat_board)

    return config, observ


def board_reshape(board, rows, columns):
    return np.array(board, dtype=np.uint8).reshape((rows, columns))
