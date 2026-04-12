import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    return [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY]
    ]


def player(board):
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O


def actions(board):
    return {
        (i, j)
        for i in range(3)
        for j in range(3)
        if board[i][j] == EMPTY
    }


def result(board, action):
    i, j = action

    if board[i][j] != EMPTY:
        raise Exception("Invalid action!")

    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board


def get_horizontal_winner(board):
    for row in board:
        if row[0] is not None and row.count(row[0]) == 3:
            return row[0]
    return None


def get_vertical_winner(board):
    for col in range(3):
        if board[0][col] is not None and all(board[r][col] == board[0][col] for r in range(3)):
            return board[0][col]
    return None


def get_diagonal_winner(board):
    if board[0][0] is not None and all(board[i][i] == board[0][0] for i in range(3)):
        return board[0][0]

    if board[0][2] is not None and all(board[i][2 - i] == board[0][2] for i in range(3)):
        return board[0][2]

    return None


def winner(board):
    return (
        get_horizontal_winner(board)
        or get_vertical_winner(board)
        or get_diagonal_winner(board)
    )


def terminal(board):
    return winner(board) is not None or all(
        cell is not EMPTY for row in board for cell in row
    )


def utility(board):
    w = winner(board)
    if w == X:
        return 1
    elif w == O:
        return -1
    return 0


def maxValue(state, alpha, beta):
    if terminal(state):
        return utility(state)

    v = -math.inf
    for action in actions(state):
        v = max(v, minValue(result(state, action), alpha, beta))
        alpha = max(alpha, v)

        if alpha >= beta:
            break

    return v


def minValue(state, alpha, beta):
    if terminal(state):
        return utility(state)

    v = math.inf
    for action in actions(state):
        v = min(v, maxValue(result(state, action), alpha, beta))
        beta = min(beta, v)

        if alpha >= beta:
            break

    return v


def minimax(board):
    if terminal(board):
        return None

    turn = player(board)
    alpha = -math.inf
    beta = math.inf

    best_move = None

    if turn == X:
        best_score = -math.inf
        for action in actions(board):
            score = minValue(result(board, action), alpha, beta)
            if score > best_score:
                best_score = score
                best_move = action
            alpha = max(alpha, best_score)
    else:
        best_score = math.inf
        for action in actions(board):
            score = maxValue(result(board, action), alpha, beta)
            if score < best_score:
                best_score = score
                best_move = action
            beta = min(beta, best_score)

    return best_move


def print_board(board):
    for row in board:
        print([" " if cell is None else cell for cell in row])
    print()



if __name__ == "__main__":
    board = initial_state()

    user = input("Choose X or O: ").upper()
    while user not in [X, O]:
        user = input("Invalid. Choose X or O: ").upper()

    print("\nCoordinates:")
    print("(0,0) (0,1) (0,2)")
    print("(1,0) (1,1) (1,2)")
    print("(2,0) (2,1) (2,2)\n")

    print_board(board)

    while True:
        if terminal(board):
            w = winner(board)
            if w is None:
                print("Game Over: Tie.")
            else:
                print(f"Game Over: {w} wins.")
            break

        turn = player(board)

        if turn == user:
            print("Your move:")
            try:
                i = int(input("Row: "))
                j = int(input("Col: "))
            except:
                print("Invalid input!")
                continue

            if (i, j) in actions(board):
                board = result(board, (i, j))
            else:
                print("Invalid move!")
                continue

        else:
            print("AI thinking...")
            move = minimax(board)
            board = result(board, move)

        print_board(board)