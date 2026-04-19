import math

EMPTY = '.'

PIECE_VALUE = {
    'K': 10000,   # Tướng
    'A': 20,      # Sĩ
    'E': 20,      # Tượng
    'H': 90,      # Mã
    'R': 500,     # Xe
    'C': 250,     # Pháo
    'P': 70       # Tốt
}


class Xiangqi:
    def __init__(self):
        self.board = [
            list("rheakaehr"),
            list("........."),
            list(".c.....c."),
            list("p.p.p.p.p"),
            list("........."),
            list("........."),
            list("P.P.P.P.P"),
            list(".C.....C."),
            list("........."),
            list("RHEAKAEHR")
        ]
        self.turn = 'r'   # r = Red, b = Black

    def inside(self, r, c):
        return 0 <= r < 10 and 0 <= c < 9

    def piece_color(self, p):
        if p == EMPTY:
            return None
        return 'r' if p.isupper() else 'b'

    def opponent(self, turn):
        return 'b' if turn == 'r' else 'r'

    def same_side(self, p1, p2):
        if p1 == EMPTY or p2 == EMPTY:
            return False
        return self.piece_color(p1) == self.piece_color(p2)

    def in_palace(self, turn, r, c):
        if turn == 'r':
            return 7 <= r <= 9 and 3 <= c <= 5
        return 0 <= r <= 2 and 3 <= c <= 5

    def crossed_river(self, turn, r):
        if turn == 'r':
            return r <= 4
        return r >= 5

    def locate_general(self, turn):
        target = 'K' if turn == 'r' else 'k'
        for r in range(10):
            for c in range(9):
                if self.board[r][c] == target:
                    return (r, c)
        return None

    def print_board(self):
        print("   0 1 2 3 4 5 6 7 8")
        for i, row in enumerate(self.board):
            print(f"{i:2} " + " ".join(row))
        print()

    def make_move(self, move):
        r1, c1, r2, c2 = move
        captured = self.board[r2][c2]
        self.board[r2][c2] = self.board[r1][c1]
        self.board[r1][c1] = EMPTY
        return captured

    def undo_move(self, move, captured):
        r1, c1, r2, c2 = move
        self.board[r1][c1] = self.board[r2][c2]
        self.board[r2][c2] = captured

    def generate_pseudo_moves(self, turn):
        moves = []

        for r in range(10):
            for c in range(9):
                piece = self.board[r][c]
                if piece == EMPTY or self.piece_color(piece) != turn:
                    continue

                up = piece.upper()

                # Xe
                if up == 'R':
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = r + dr, c + dc
                        while self.inside(nr, nc):
                            target = self.board[nr][nc]
                            if target == EMPTY:
                                moves.append((r, c, nr, nc))
                            else:
                                if not self.same_side(piece, target):
                                    moves.append((r, c, nr, nc))
                                break
                            nr += dr
                            nc += dc

                # Pháo
                elif up == 'C':
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = r + dr, c + dc

                        # đi thường
                        while self.inside(nr, nc) and self.board[nr][nc] == EMPTY:
                            moves.append((r, c, nr, nc))
                            nr += dr
                            nc += dc

                        # nhảy qua 1 quân rồi bắt
                        nr += dr
                        nc += dc
                        while self.inside(nr, nc):
                            if self.board[nr][nc] != EMPTY:
                                if not self.same_side(piece, self.board[nr][nc]):
                                    moves.append((r, c, nr, nc))
                                break
                            nr += dr
                            nc += dc

                # Mã
                elif up == 'H':
                    patterns = [
                        ((-1, 0), (-2, -1)), ((-1, 0), (-2, 1)),
                        ((1, 0), (2, -1)), ((1, 0), (2, 1)),
                        ((0, -1), (-1, -2)), ((0, -1), (1, -2)),
                        ((0, 1), (-1, 2)), ((0, 1), (1, 2)),
                    ]
                    for leg, jump in patterns:
                        lr, lc = r + leg[0], c + leg[1]
                        nr, nc = r + jump[0], c + jump[1]
                        if self.inside(lr, lc) and self.board[lr][lc] == EMPTY and self.inside(nr, nc):
                            target = self.board[nr][nc]
                            if target == EMPTY or not self.same_side(piece, target):
                                moves.append((r, c, nr, nc))

                # Tượng
                elif up == 'E':
                    for dr, dc in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
                        nr, nc = r + dr, c + dc
                        eye_r, eye_c = r + dr // 2, c + dc // 2
                        if not self.inside(nr, nc):
                            continue
                        if self.board[eye_r][eye_c] != EMPTY:
                            continue

                        if turn == 'r' and nr < 5:
                            continue
                        if turn == 'b' and nr > 4:
                            continue

                        target = self.board[nr][nc]
                        if target == EMPTY or not self.same_side(piece, target):
                            moves.append((r, c, nr, nc))

                # Sĩ
                elif up == 'A':
                    for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        nr, nc = r + dr, c + dc
                        if self.inside(nr, nc) and self.in_palace(turn, nr, nc):
                            target = self.board[nr][nc]
                            if target == EMPTY or not self.same_side(piece, target):
                                moves.append((r, c, nr, nc))

                # Tướng
                elif up == 'K':
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = r + dr, c + dc
                        if self.inside(nr, nc) and self.in_palace(turn, nr, nc):
                            target = self.board[nr][nc]
                            if target == EMPTY or not self.same_side(piece, target):
                                moves.append((r, c, nr, nc))

                    # Tướng đối mặt
                    step = -1 if turn == 'r' else 1
                    nr = r + step
                    while self.inside(nr, c):
                        if self.board[nr][c] != EMPTY:
                            if self.board[nr][c] == ('k' if turn == 'r' else 'K'):
                                moves.append((r, c, nr, c))
                            break
                        nr += step

                # Tốt
                elif up == 'P':
                    if turn == 'r':
                        dirs = [(-1, 0)]
                        if self.crossed_river(turn, r):
                            dirs += [(0, -1), (0, 1)]
                    else:
                        dirs = [(1, 0)]
                        if self.crossed_river(turn, r):
                            dirs += [(0, -1), (0, 1)]

                    for dr, dc in dirs:
                        nr, nc = r + dr, c + dc
                        if self.inside(nr, nc):
                            target = self.board[nr][nc]
                            if target == EMPTY or not self.same_side(piece, target):
                                moves.append((r, c, nr, nc))

        return moves

    def is_in_check(self, turn):
        general_pos = self.locate_general(turn)
        if general_pos is None:
            return True

        enemy = self.opponent(turn)
        enemy_moves = self.generate_pseudo_moves(enemy)

        for move in enemy_moves:
            _, _, r2, c2 = move
            if (r2, c2) == general_pos:
                return True
        return False

    def generate_legal_moves(self, turn):
        legal = []
        for move in self.generate_pseudo_moves(turn):
            captured = self.make_move(move)
            if not self.is_in_check(turn):
                legal.append(move)
            self.undo_move(move, captured)
        return legal

    def evaluate(self):
        score = 0

        for r in range(10):
            for c in range(9):
                p = self.board[r][c]
                if p == EMPTY:
                    continue

                value = PIECE_VALUE[p.upper()]

                # bonus cho Tốt tiến sâu
                if p.upper() == 'P':
                    if p.isupper():
                        value += max(0, 6 - r) * 8
                    else:
                        value += max(0, r - 3) * 8

                if p.isupper():
                    score += value
                else:
                    score -= value

        return score

    def order_moves(self, moves):
        def score_move(move):
            _, _, r2, c2 = move
            target = self.board[r2][c2]
            if target == EMPTY:
                return 0
            val = PIECE_VALUE[target.upper()]
            if target.upper() == 'K':
                val += 100000
            return val

        moves.sort(key=score_move, reverse=True)
        return moves

    def alphabeta(self, depth, alpha, beta, turn):
        red_general = self.locate_general('r')
        black_general = self.locate_general('b')

        if red_general is None:
            return -1000000
        if black_general is None:
            return 1000000

        legal_moves = self.generate_legal_moves(turn)

        if not legal_moves:
            return -1000000 if turn == 'r' else 1000000

        if depth == 0:
            return self.evaluate()

        legal_moves = self.order_moves(legal_moves)

        if turn == 'r':
            value = -math.inf
            for move in legal_moves:
                captured = self.make_move(move)
                value = max(value, self.alphabeta(depth - 1, alpha, beta, 'b'))
                self.undo_move(move, captured)

                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = math.inf
            for move in legal_moves:
                captured = self.make_move(move)
                value = min(value, self.alphabeta(depth - 1, alpha, beta, 'r'))
                self.undo_move(move, captured)

                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value

    def best_move(self, depth=3):
        legal_moves = self.generate_legal_moves(self.turn)
        if not legal_moves:
            return None

        legal_moves = self.order_moves(legal_moves)
        best = None

        if self.turn == 'r':
            best_value = -math.inf
            for move in legal_moves:
                captured = self.make_move(move)
                value = self.alphabeta(depth - 1, -math.inf, math.inf, 'b')
                self.undo_move(move, captured)

                if value > best_value:
                    best_value = value
                    best = move
        else:
            best_value = math.inf
            for move in legal_moves:
                captured = self.make_move(move)
                value = self.alphabeta(depth - 1, -math.inf, math.inf, 'r')
                self.undo_move(move, captured)

                if value < best_value:
                    best_value = value
                    best = move

        return best

    def winner(self):
        if self.locate_general('r') is None:
            return 'b'
        if self.locate_general('b') is None:
            return 'r'

        legal = self.generate_legal_moves(self.turn)
        if not legal:
            return self.opponent(self.turn)

        return None

    def play(self):
        print("=== CO TUONG - ALPHA BETA ===")
        print("Ban la DO (chu HOA), AI la DEN (chu thuong)")
        print("Nhap: r1 c1 r2 c2  | vi du: 9 0 8 0")

        while True:
            self.print_board()

            win = self.winner()
            if win:
                if win == 'r':
                    print("DO thang!")
                else:
                    print("DEN thang!")
                break

            if self.turn == 'r':
                cmd = input("Nuoc cua ban: ").strip()
                try:
                    r1, c1, r2, c2 = map(int, cmd.split())
                    move = (r1, c1, r2, c2)
                except:
                    print("Nhap sai dinh dang.")
                    continue

                legal_moves = self.generate_legal_moves('r')
                if move not in legal_moves:
                    print("Nuoc di khong hop le.")
                    continue

                self.make_move(move)
                self.turn = 'b'
            else:
                move = self.best_move(depth=3)
                if move is None:
                    print("AI khong con nuoc di.")
                    break

                print("AI di:", move)
                self.make_move(move)
                self.turn = 'r'


if __name__ == "__main__":
    game = Xiangqi()
    game.play()