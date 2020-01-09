import numpy as np
from collections import namedtuple


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


Tree = namedtuple('Tree', ('next', 'parent', 'score', 'board'))


def grow_tree(root: Tree, my_player, current_player, depth, max_depth=3, in_a_row=4):
    if depth >= max_depth:
        return

    board = root.board
    rows, cols = board.shape

    other_player = 2 if my_player == 1 else 1

    for choice in range(cols):
        # check choice-column for free space to drop a chip
        column = board[:, choice]
        best_row = -1
        for r in reversed(range(rows)):
            if column[r] == 0:
                best_row = r
                break

        if best_row == -1:
            continue  # no free scape

        new_board = board.copy()
        new_board[best_row, choice] = current_player

        winner = check_game_over(new_board, in_a_row)
        if winner == 0:
            score = (calculate_score_for_player(new_board, my_player, in_a_row) -
                     calculate_score_for_player(new_board, other_player, in_a_row))
        elif winner == my_player:
            score = +np.inf
        else:
            score = -np.inf

        new_node = Tree([], root, score, new_board)
        root.next.append(new_node)

        if winner == 0:
            grow_tree(new_node, my_player, 1 if current_player == 2 else 2,
                      depth + 1, max_depth, in_a_row)


def minmax(my_player, tree: Tree):
    if len(tree.next) == 0:
        return tree
    if my_player == 2:
        sorter = lambda x: minmax(1, x).score
    else:
        sorter = lambda x: -(minmax(2, x).score)
    return sorted(tree.next, key=sorter)[0]



def agent(observation, configuration):
    columns = configuration.columns
    rows = configuration.rows
    in_a_row = configuration.inarow
    board = observation.board

    # which player I am!
    mark = observation.mark

    current_board = np.array(observation['board'], dtype=np.uint8).reshape((rows, columns))

    tree = Tree([], None, 0, current_board)
    grow_tree(tree,
              current_player=mark,
              my_player=mark,
              depth=0, max_depth=4, in_a_row=in_a_row)

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
    print(calculate_score_for_player(board, 4, in_a_row=4))


def test_grow_tree():
    board = np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ], dtype=np.uint8)

    tree = Tree([], None, 0, board)
    grow_tree(tree,
              current_player=1,
              my_player=1,
              depth=0, max_depth=4, in_a_row=4)

    print(tree)

test_grow_tree()
# test_score()
# test()
