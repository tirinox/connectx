def my_agent(observation, configuration, max_depth):
    import numpy as np

    def check_win(bord):
        for y in range(bord.shape[0]):
            for x in range(bord.shape[1]):
                if x + 3 < bord.shape[1] and bord[y, x] != 0:
                    if bord[y, x] == bord[y, x + 1] and \
                            bord[y, x + 1] == bord[y, x + 2] and \
                            bord[y, x + 2] == bord[y, x + 3]:
                        return bord[y, x]
                if y + 3 < bord.shape[0] and bord[y, x] != 0:
                    if bord[y, x] == bord[y + 1, x] and \
                            bord[y + 1, x] == bord[y + 2, x] and \
                            bord[y + 2, x] == bord[y + 3, x]:
                        return bord[y, x]
                if x + 3 < bord.shape[1] and y + 3 < bord.shape[0] and bord[y, x] != 0:
                    if bord[y, x] == bord[y + 1, x + 1] and \
                            bord[y + 1, x + 1] == bord[y + 2, x + 2] and \
                            bord[y + 2, x + 2] == bord[y + 3, x + 3]:
                        return bord[y, x]
                if x + 3 < bord.shape[1] and y + 3 < bord.shape[0] and bord[y + 3, x] != 0:
                    if bord[y + 3, x] == bord[y + 2, x + 1] and \
                            bord[y + 2, x + 1] == bord[y + 1, x + 2] and \
                            bord[y + 1, x + 2] == bord[y, x + 3]:
                        return bord[y + 3, x]
        return 0

    def make_score(bord):
        """
        If the game does not advance to the conclusion even after calculating up to max_depth,
        a score is obtained from the board. Here, the score is simply set to be advantageous
        to the side where the stones are gathered.
        """
        d = np.where(bord == 1)
        s = -np.std(d[1])
        if d[0].shape[0] > 0:
            mx, my = np.mean(d[0]), np.mean(d[1])
            s -= np.std([np.sqrt(((x - mx) * (x - mx)) + ((y - my) * (y - my))) for x, y in zip(d[0], d[1])])
        d = np.where(bord == 2)
        s += np.std(d[1])
        if d[0].shape[0] > 0:
            mx, my = np.mean(d[0]), np.mean(d[1])
            s += np.std([np.sqrt(((x - mx) * (x - mx)) + ((y - my) * (y - my))) for x, y in zip(d[0], d[1])])
        return s

    def drop_one(c, b, stack_bord):
        nonlocal configuration
        bord = stack_bord.copy()
        d = np.where(bord[:, c] != 0)[0]
        p = bord.shape[0] if d.shape[0] == 0 else min(d)
        if p == 0:
            return None
        else:
            bord[p - 1, c] = b
            return bord

    def grow_tree(selection, tree, depth, current_bord, b):
        nonlocal configuration, max_depth
        if depth >= max_depth:
            return
        w = check_win(current_bord)
        if w != 0:
            s = np.inf if b == 2 else -np.inf
        else:
            s = make_score(current_bord)
        leaf = {'root': tree, 'selection': selection, 'bord': current_bord, 'score': s, 'next': []}
        tree['next'].append(leaf)
        if w != 0:
            return
        k = 1 if b == 2 else 2
        for i in range(configuration.columns):
            i = configuration.columns - i - 1
            t = drop_one(i, b, current_bord)
            if t is not None:
                grow_tree(i, leaf, depth + 1, t, k)

    game_tree = {'next': []}
    current_bord = np.array(observation['board'], dtype=np.uint8).reshape((6, 7))
    if observation.mark == 2:
        # Decide that I am 1
        current_bord[current_bord == 2] = 255
        current_bord[current_bord == 1] = 2
        current_bord[current_bord == 255] = 1
    grow_tree(0, game_tree, 0, current_bord, 1)
    game_tree = game_tree['next'][0]

    print(current_bord)

    def minmax(b, tree):
        nonlocal configuration, max_depth
        if len(tree['next']) == 0:
            return tree
        if b == 2:
            return sorted(tree['next'], key=lambda x: minmax(1, x)['score'])[0]
        else:
            return sorted(tree['next'], key=lambda x: -(minmax(2, x)['score']))[0]

    r = minmax(1, game_tree)
    while r['root'] != game_tree:
        r = r['root']
    return r['selection']
