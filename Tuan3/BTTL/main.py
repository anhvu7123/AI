import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O


def actions(board):
    return {(i, j)
            for i in range(3)
            for j in range(3)
            if board[i][j] is EMPTY}


def result(board, action):
    i, j = action
    if board[i][j] is not EMPTY:
        raise Exception("Invalid move")
    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    lines = []

    # Rows
    lines.extend(board)

    # Columns
    lines.extend([[board[r][c] for r in range(3)] for c in range(3)])

    # Diagonals
    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2 - i] for i in range(3)])

    for line in lines:
        if line[0] is not None and line.count(line[0]) == 3:
            return line[0]

    return None


def terminal(board):
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)


def utility(board):
    w = winner(board)
    if w == X:
        return 1
    elif w == O:
        return -1
    return 0


def max_value(state):
    if terminal(state):
        return utility(state)
    v = -math.inf
    for action in actions(state):
        v = max(v, min_value(result(state, action)))
    return v


def min_value(state):
    if terminal(state):
        return utility(state)
    v = math.inf
    for action in actions(state):
        v = min(v, max_value(result(state, action)))
    return v


def minimax(board):
    if terminal(board):
        return None

    turn = player(board)

    if turn == X:
        best_score = -math.inf
        best_move = None
        for action in actions(board):
            score = min_value(result(board, action))
            if score > best_score:
                best_score = score
                best_move = action
        return best_move
    else:
        best_score = math.inf
        best_move = None
        for action in actions(board):
            score = max_value(result(board, action))
            if score < best_score:
                best_score = score
                best_move = action
        return best_move


def print_board(board):
    for row in board:
        print([" " if cell is None else cell for cell in row])
    print()


if __name__ == "__main__":
    board = initial_state()

    user = input("Choose a player (X/O): ").upper()
    while user not in [X, O]:
        user = input("Invalid choice. Choose X or O: ").upper()

    ai = O if user == X else X

    print("\nBoard positions are indexed 0, 1, 2")
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
            except ValueError:
                print("Please enter valid numbers.")
                continue

            if (i, j) in actions(board):
                board = result(board, (i, j))
            else:
                print("Invalid move!")
                continue
        else:
            print("AI is thinking...")
            move = minimax(board)
            board = result(board, move)

        print_board(board)