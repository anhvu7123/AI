import chess
import math

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}


def evaluate(board):
    if board.is_checkmate():
        return -100000 if board.turn == chess.WHITE else 100000

    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    score = 0
    for piece_type, value in PIECE_VALUES.items():
        score += len(board.pieces(piece_type, chess.WHITE)) * value
        score -= len(board.pieces(piece_type, chess.BLACK)) * value

    temp = board.copy(stack=False)
    temp.turn = chess.WHITE
    white_mobility = temp.legal_moves.count()
    temp.turn = chess.BLACK
    black_mobility = temp.legal_moves.count()

    score += 5 * (white_mobility - black_mobility)
    return score


def order_moves(board):
    moves = list(board.legal_moves)

    def move_score(move):
        score = 0

        if board.is_capture(move):
            captured = board.piece_at(move.to_square)
            if captured:
                score += 10 * PIECE_VALUES.get(captured.piece_type, 0)

        if move.promotion:
            score += 800

        if board.gives_check(move):
            score += 50

        return score

    moves.sort(key=move_score, reverse=True)
    return moves


def alphabeta(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate(board)

    moves = order_moves(board)

    if maximizing_player:
        value = -math.inf
        for move in moves:
            board.push(move)
            value = max(value, alphabeta(board, depth - 1, alpha, beta, False))
            board.pop()

            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = math.inf
        for move in moves:
            board.push(move)
            value = min(value, alphabeta(board, depth - 1, alpha, beta, True))
            board.pop()

            beta = min(beta, value)
            if alpha >= beta:
                break
        return value


def best_move(board, depth=3):
    maximizing = board.turn == chess.WHITE
    best = None

    if maximizing:
        best_value = -math.inf
        for move in order_moves(board):
            board.push(move)
            value = alphabeta(board, depth - 1, -math.inf, math.inf, False)
            board.pop()

            if value > best_value:
                best_value = value
                best = move
    else:
        best_value = math.inf
        for move in order_moves(board):
            board.push(move)
            value = alphabeta(board, depth - 1, -math.inf, math.inf, True)
            board.pop()

            if value < best_value:
                best_value = value
                best = move

    return best


def play():
    board = chess.Board()

    print("=== CO VUA - ALPHA BETA ===")
    print("Ban la TRANG")
    print("Nhap nuoc theo UCI, vi du: e2e4")

    while not board.is_game_over():
        print("\n", board)
        print("FEN:", board.fen())

        if board.turn == chess.WHITE:
            move_str = input("Nuoc cua ban: ").strip()

            try:
                move = chess.Move.from_uci(move_str)
                if move not in board.legal_moves:
                    print("Nuoc di khong hop le.")
                    continue
                board.push(move)
            except:
                print("Sai dinh dang. Vi du: e2e4")
                continue
        else:
            ai_move = best_move(board, depth=3)
            print("AI di:", ai_move)
            board.push(ai_move)

    print("\n", board)
    print("Ket qua:", board.result())


if __name__ == "__main__":
    play()