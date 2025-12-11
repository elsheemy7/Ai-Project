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
