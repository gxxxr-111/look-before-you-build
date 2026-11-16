"""Simple gomoku AI: scores every empty cell and plays the best one."""
SIZE = 15
WEIGHTS = {5: 100000, 4: 5000, 3: 800, 2: 60, 1: 5}  # tuned 5 times so far
DIRS = [(1, 0), (0, 1), (1, 1), (1, -1)]

def line_len(board, r, c, dr, dc, who):
    n = 1
    for s in (1, -1):
        rr, cc = r + dr * s, c + dc * s
        while 0 <= rr < SIZE and 0 <= cc < SIZE and board[rr][cc] == who:
            n += 1
            rr += dr * s
            cc += dc * s
    return n

def score_cell(board, r, c, me, opp):
    total = 0
    for dr, dc in DIRS:
        total += WEIGHTS.get(min(line_len(board, r, c, dr, dc, me), 5), 0)
        total += 0.9 * WEIGHTS.get(min(line_len(board, r, c, dr, dc, opp), 5), 0)
    return total

def best_move(board, me, opp):
    best, move = -1, None
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == 0:
                s = score_cell(board, r, c, me, opp)
                if s > best:
                    best, move = s, (r, c)
    return move
