import numpy as np
from collections import namedtuple
from dataclasses import dataclass
import random


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
                if supports[r, c]:
                    supported += 1
            elif cell == 0:
                empty += 1

            # b2[r, c] = 1

        if my + empty == in_a_row and my != 0:
            # plen = in_a_row - empty

            delta = 10 ** (in_a_row - empty - 1)
            if my > 1 and supported < in_a_row:
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



@dataclass
class Tree:
    next: list
    parent: 'Tree'
    score: float
    board: np.ndarray
    choice: int


# Tree = namedtuple('Tree', ('next', 'parent', 'score', 'board', 'choice'))


def grow_tree(root: Tree, my_player, current_player, depth, max_depth=3, in_a_row=4):
    if depth >= max_depth:
        return

    board = root.board
    rows, cols = board.shape

    other_player = 1 if current_player == 2 else 2
    opp_player = 1 if my_player == 2 else 2

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
                     calculate_score_for_player(new_board, opp_player, in_a_row))
        elif winner == my_player:
            score = +np.inf
        else:
            score = -np.inf

        new_node = Tree([], root, score, new_board, choice)
        root.next.append(new_node)

        if winner == 0:
            grow_tree(new_node, my_player, other_player,
                      depth + 1, max_depth, in_a_row)


def pick_best_move(tree: Tree):
    is_my_turn = True
    while tree.next:
        key = lambda n: n.score
        if is_my_turn:
            tree = max(tree.next, key=key)
        else:
            tree = min(tree.next, key=key)


def pick_best_move_2(tree: Tree, my_turn=True):
    if not tree.next:
        return tree
    else:
        k = 1 if my_turn else -1
        sort_key = lambda node: k * pick_best_move_2(node, not my_turn).score
        return sorted(tree.next, key=sort_key)[0]


def agent(observation, configuration):
    columns = configuration.columns
    rows = configuration.rows
    in_a_row = configuration.inarow
    board = observation.board

    # which player I am!
    mark = observation.mark
    opp = 1 if mark == 2 else 2

    current_board = np.array(board, dtype=np.uint8).reshape((rows, columns))

    # tree = Tree([], None, 0, current_board, -1)
    # grow_tree(tree,
    #           current_player=mark,
    #           my_player=mark,
    #           depth=0, max_depth=4, in_a_row=in_a_row)

    best_choice = -1
    best_score = -np.inf
    for choice in range(columns):
        # check choice-column for free space to drop a chip
        column = current_board[:, choice]
        top_row = -1
        for r in reversed(range(rows)):
            if column[r] == 0:
                top_row = r
                break

        if top_row == -1:
            continue  # no free space in the column

        new_board = current_board.copy()
        new_board[top_row, choice] = mark

        score = (calculate_score_for_player(new_board, mark, in_a_row) -
                 2 * calculate_score_for_player(new_board, opp, in_a_row))

        if score > best_score:
            best_score = score
            best_choice = choice
        elif score == best_score:
            best_choice = random.choice((choice, best_choice))

    # return a column to play: [0, configuration.columns)
    return best_choice


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


def tree_to_str(tree: Tree, depth=0):
    r = '--' * depth + f'Node(c={tree.choice}; sc={tree.score:0.1f})\n'
    for n in tree.next:
        r += tree_to_str(n, depth + 1)
    return r


def test_grow_tree():
    board = np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1],
        [2, 1, 1, 1, 0, 0, 1],
    ], dtype=np.uint8)

    tree = Tree([], None, 0, board, -1)
    grow_tree(tree,
              current_player=1,
              my_player=1,
              depth=0, max_depth=3, in_a_row=4)

    print(tree_to_str(tree, 0))

    leaf = pick_best_move_2(tree)

    print(leaf.choice)


def test_my_strat():
    board = np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1],
        [2, 1, 1, 1, 0, 0, 1],
    ], dtype=np.uint8)
    rows, columns = board.shape

    mark, opp = 1, 2
    in_a_row = 4

    best_choice = -1
    best_score = -np.inf
    for choice in range(columns):
        # check choice-column for free space to drop a chip
        column = board[:, choice]
        top_row = -1
        for r in reversed(range(rows)):
            if column[r] == 0:
                top_row = r
                break

        if top_row == -1:
            continue  # no free space in the column

        new_board = board.copy()
        new_board[top_row, choice] = mark

        score = (calculate_score_for_player(new_board, mark, in_a_row) -
                 calculate_score_for_player(new_board, opp, in_a_row))

        print('score = ', score, 'board = \n', new_board)

        if score > best_score:
            best_score = score
            best_choice = choice

    print(best_choice)


test_my_strat()

# test_grow_tree()


# import cProfile
# cProfile.run('test_grow_tree()')

# test_grow_tree()
# test_score()
# test()
