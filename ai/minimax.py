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
    if game.game_over() or depth > max_depth:
        return game.heuristic_value(player, depth), []

    best_score = -float('inf') if game.current_player == player else float('inf')
    best_moves = []

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

        # prune branch
        if alpha >= beta:
            break

    return best_score, best_moves