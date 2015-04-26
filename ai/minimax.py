# http://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning


def minimax(game, player, depth, max_depth):
    if game.game_over() or depth > max_depth:
        return game.heuristic_value(player), []

    best_score = -float('inf') if game.current_player == player else float('inf')
    best_moves = []

    for move in list(game.valid_moves()):
        game.move(move)
        score, _ = minimax(game, player, depth+1, max_depth)
        game.undo_move()

        if game.current_player == player:
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)
        else:
            if score < best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

    return best_score, best_moves


def alphabeta(game, player, depth, max_depth, alpha, beta):
    """ Alpha beta minimax algorithm

    :param game: game object with game_over, heuristic_value, and valid_moves methods
    :param player: maximizing player
    :param depth: current depth in tree
    :param max_depth: maximum depth in tree to search
    :param alpha: minimum score maximizing player will get
    :param beta: maximum score minimizing player will get
    :return:  score, list of moves
    """
    # base case - game over or depth exceeded
    if game.game_over() or depth > max_depth:
        return game.heuristic_value(player, depth), []

    # init best score to worst possible
    best_score = -float('inf') if game.current_player == player else float('inf')
    best_moves = []

    # loop all moves
    for move in list(game.valid_moves()):
        # make move
        game.move(move)
        # recurse
        score, _ = alphabeta(game, player, depth+1, max_depth, alpha, beta)

        # undo moves
        game.undo_move()

        # save the best scores
        if game.current_player == player:
            alpha = max(alpha, score)
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)
        else:
            beta = min(beta, score)
            if score < best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

        # prune branch if the minimum score the max player gets exceeds the max score the min player gets
        if alpha >= beta:
            break

    return best_score, best_moves