# Heuristic evaluation functions for AI (position scoring)
def get_position_score(board_instance, piece):
    board_data = board_instance.board
    score = 0
    center_col = COLUMNS // 2
    
    # 1. Center column bonus
    center_count = sum(1 for r in range(ROWS) if board_data[r][center_col] == piece)
    score += center_count * CENTER_WEIGHT

    # 2. Evaluate all windows (horizontal, vertical, diagonal)
    
    # Horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - CONNECT_N + 1):
            window = board_data[r][c:c + CONNECT_N]
            score += evaluate_window(window, piece)

    # Vertical
    for c in range(COLUMNS):
        for r in range(ROWS - CONNECT_N + 1):
            window = [board_data[r + i][c] for i in range(CONNECT_N)]
            score += evaluate_window(window, piece)
            
    # Diagonal ascending (/)
    for r in range(CONNECT_N - 1, ROWS):
        for c in range(COLUMNS - CONNECT_N + 1):
            window = [board_data[r - i][c + i] for i in range(CONNECT_N)]
            score += evaluate_window(window, piece)

    # Diagonal descending (\)
    for r in range(ROWS - CONNECT_N + 1):
        for c in range(COLUMNS - CONNECT_N + 1):
            window = [board_data[r + i][c + i] for i in range(CONNECT_N)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board):
    return (
        check_win(board, PLAYER_PIECE)
        or check_win(board, AI_PIECE)
        or board.is_full()
    )



# **********************************************   4
def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = board.get_valid_locations()

    # حالات التوقف
    if depth == 0 or is_terminal_node(board):
        if check_win(board, AI_PIECE):
            return None, SCORE_FOUR
        elif check_win(board, PLAYER_PIECE):
            return None, -SCORE_FOUR
        else: # تعادل أو انتهاء العمق
            return None, get_position_score(board, AI_PIECE)

    # المنطق الأساسي لـ Minimax مع Alpha-Beta Pruning
    best_col = random.choice(valid_locations) if valid_locations else None

    if maximizingPlayer:
        value = -INF
        for col in valid_locations:
            board.drop_piece(col, AI_PIECE)
            _, score = minimax(board, depth - 1, alpha, beta, False)
            board.remove_piece(col)

            if score > value:
                value = score
                best_col = col

            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value

    else: # Minimizing Player (PLAYER_PIECE)
        value = INF
        for col in valid_locations:
            board.drop_piece(col, PLAYER_PIECE)
            _, score = minimax(board, depth - 1, alpha, beta, True)
            board.remove_piece(col)

            if score < value:
                value = score
                best_col = col

            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value




