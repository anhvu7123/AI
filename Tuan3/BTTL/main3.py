import math

EMPTY = '.'
AI = 'X'
PLAYER = 'O'

# ==============================
# Khởi tạo bàn cờ
# ==============================
def create_board(N):
    return [[EMPTY for _ in range(N)] for _ in range(N)]

# ==============================
# In bàn cờ
# ==============================
def print_board(board):
    for row in board:
        print(' '.join(row))
    print()

# ==============================
# Kiểm tra đầy
# ==============================
def is_full(board):
    return all(cell != EMPTY for row in board for cell in row)

# ==============================
# Kiểm tra thắng (K liên tiếp)
# ==============================
def check_winner(board, N, K):
    directions = [(1,0),(0,1),(1,1),(1,-1)]

    for i in range(N):
        for j in range(N):
            if board[i][j] == EMPTY:
                continue
            for dx, dy in directions:
                count = 0
                for k in range(K):
                    x = i + dx*k
                    y = j + dy*k
                    if 0 <= x < N and 0 <= y < N and board[x][y] == board[i][j]:
                        count += 1
                    else:
                        break
                if count == K:
                    return board[i][j]
    return None

# ==============================
# Kiểm tra ô có hàng xóm
# ==============================
def has_neighbor(board, x, y):
    N = len(board)
    for dx in [-1,0,1]:
        for dy in [-1,0,1]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < N and 0 <= ny < N:
                if board[nx][ny] != EMPTY:
                    return True
    return False

# ==============================
# Sinh nước đi (tối ưu)
# ==============================
def get_moves(board):
    N = len(board)
    moves = []
    for i in range(N):
        for j in range(N):
            if board[i][j] == EMPTY:
                if has_neighbor(board, i, j):
                    moves.append((i, j))

    # nếu bàn trống -> đi giữa
    if not moves:
        return [(N//2, N//2)]

    return moves

# ==============================
# Heuristic evaluation
# ==============================
def evaluate(board, N, K):
    score = 0

    def evaluate_line(line):
        if line.count(AI) > 0 and line.count(PLAYER) > 0:
            return 0
        if line.count(AI) == 0 and line.count(PLAYER) == 0:
            return 0

        count_ai = line.count(AI)
        count_pl = line.count(PLAYER)

        if count_ai > 0:
            return 10 ** count_ai
        if count_pl > 0:
            return -(10 ** count_pl)

    # check all possible lines
    for i in range(N):
        for j in range(N):
            # horizontal
            if j + K <= N:
                line = [board[i][j+k] for k in range(K)]
                score += evaluate_line(line)

            # vertical
            if i + K <= N:
                line = [board[i+k][j] for k in range(K)]
                score += evaluate_line(line)

            # diagonal
            if i + K <= N and j + K <= N:
                line = [board[i+k][j+k] for k in range(K)]
                score += evaluate_line(line)

            # anti-diagonal
            if i + K <= N and j - K + 1 >= 0:
                line = [board[i+k][j-k] for k in range(K)]
                score += evaluate_line(line)

    return score

# ==============================
# Minimax + Alpha-Beta
# ==============================
def minimax(board, depth, max_depth, alpha, beta, is_max, N, K):
    winner = check_winner(board, N, K)

    if winner == AI:
        return 100000 - depth
    elif winner == PLAYER:
        return -100000 + depth
    elif is_full(board):
        return 0

    if depth == max_depth:
        return evaluate(board, N, K)

    moves = get_moves(board)

    if is_max:
        best = -math.inf
        for (i, j) in moves:
            board[i][j] = AI
            val = minimax(board, depth+1, max_depth, alpha, beta, False, N, K)
            board[i][j] = EMPTY

            best = max(best, val)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = math.inf
        for (i, j) in moves:
            board[i][j] = PLAYER
            val = minimax(board, depth+1, max_depth, alpha, beta, True, N, K)
            board[i][j] = EMPTY

            best = min(best, val)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best

# ==============================
# Tìm nước đi tốt nhất
# ==============================
def best_move(board, N, K, max_depth):
    best_val = -math.inf
    move = None

    for (i, j) in get_moves(board):
        board[i][j] = AI
        val = minimax(board, 0, max_depth, -math.inf, math.inf, False, N, K)
        board[i][j] = EMPTY

        if val > best_val:
            best_val = val
            move = (i, j)

    return move

# ==============================
# Game loop
# ==============================
def play_game(N=5, K=4, depth=3):
    board = create_board(N)

    while True:
        print_board(board)

        # Player move
        x, y = map(int, input("Your move (row col): ").split())
        if board[x][y] != EMPTY:
            print("Invalid move!")
            continue
        board[x][y] = PLAYER

        if check_winner(board, N, K) == PLAYER:
            print_board(board)
            print("You win!")
            break

        # AI move
        print("AI thinking...")
        move = best_move(board, N, K, depth)
        if move:
            board[move[0]][move[1]] = AI

        if check_winner(board, N, K) == AI:
            print_board(board)
            print("AI wins!")
            break

        if is_full(board):
            print_board(board)
            print("Draw!")
            break


# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    play_game(N=5, K=4, depth=3)