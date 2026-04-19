import math

SIZE = 5
EMPTY = '.'
HUMAN = 'B'   # Den
AI = 'W'      # Trang


class MiniGo:
    def __init__(self, size=5):
        self.size = size
        self.board = [[EMPTY for _ in range(size)] for _ in range(size)]

    def inside(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size

    def print_board(self):
        print("  " + " ".join(str(c) for c in range(self.size)))
        for r in range(self.size):
            print(f"{r} " + " ".join(self.board[r]))
        print()

    def neighbors(self, r, c):
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if self.inside(nr, nc):
                yield nr, nc

    def copy_board(self, board):
        return [row[:] for row in board]

    def get_group(self, board, r, c):
        color = board[r][c]
        stack = [(r, c)]
        seen = {(r, c)}
        group = []

        while stack:
            cr, cc = stack.pop()
            group.append((cr, cc))

            for nr, nc in self.neighbors(cr, cc):
                if (nr, nc) not in seen and board[nr][nc] == color:
                    seen.add((nr, nc))
                    stack.append((nr, nc))

        return group

    def liberties(self, board, group):
        libs = set()
        for r, c in group:
            for nr, nc in self.neighbors(r, c):
                if board[nr][nc] == EMPTY:
                    libs.add((nr, nc))
        return libs

    def remove_group(self, board, group):
        for r, c in group:
            board[r][c] = EMPTY

    def apply_move(self, board, move, color):
        if move is None:
            return self.copy_board(board)

        r, c = move
        if board[r][c] != EMPTY:
            return None

        new_board = self.copy_board(board)
        new_board[r][c] = color
        opponent = HUMAN if color == AI else AI

        # bat nhom doi thu neu het khi
        for nr, nc in self.neighbors(r, c):
            if new_board[nr][nc] == opponent:
                group = self.get_group(new_board, nr, nc)
                if len(self.liberties(new_board, group)) == 0:
                    self.remove_group(new_board, group)

        # nuoc tu sat la khong hop le
        own_group = self.get_group(new_board, r, c)
        if len(self.liberties(new_board, own_group)) == 0:
            return None

        return new_board

    def valid_moves(self, board, color):
        moves = []
        for r in range(self.size):
            for c in range(self.size):
                if board[r][c] == EMPTY and self.apply_move(board, (r, c), color) is not None:
                    moves.append((r, c))
        moves.append(None)  # pass
        return moves

    def evaluate(self, board):
        white_stones = sum(cell == AI for row in board for cell in row)
        black_stones = sum(cell == HUMAN for row in board for cell in row)

        white_libs = 0
        black_libs = 0
        counted = set()

        for r in range(self.size):
            for c in range(self.size):
                if board[r][c] in (AI, HUMAN) and (r, c) not in counted:
                    group = self.get_group(board, r, c)
                    counted.update(group)
                    libs = len(self.liberties(board, group))

                    if board[r][c] == AI:
                        white_libs += libs
                    else:
                        black_libs += libs

        return 10 * (white_stones - black_stones) + (white_libs - black_libs)

    def board_full(self, board):
        return all(cell != EMPTY for row in board for cell in row)

    def order_moves(self, board, color, moves):
        scored = []

        for move in moves:
            if move is None:
                scored.append((-999, move))
                continue

            r, c = move
            score = 0
            for nr, nc in self.neighbors(r, c):
                if board[nr][nc] != EMPTY and board[nr][nc] != color:
                    score += 5
                elif board[nr][nc] == color:
                    score += 2

            scored.append((score, move))

        reverse = (color == AI)
        scored.sort(key=lambda x: x[0], reverse=reverse)
        return [m for _, m in scored]

    def alphabeta(self, board, depth, alpha, beta, turn, consecutive_passes):
        if depth == 0 or consecutive_passes >= 2 or self.board_full(board):
            return self.evaluate(board)

        moves = self.order_moves(board, turn, self.valid_moves(board, turn))

        if turn == AI:
            value = -math.inf
            for move in moves:
                next_board = self.apply_move(board, move, turn)
                if next_board is None:
                    continue

                next_passes = consecutive_passes + 1 if move is None else 0
                value = max(
                    value,
                    self.alphabeta(next_board, depth - 1, alpha, beta, HUMAN, next_passes)
                )
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = math.inf
            for move in moves:
                next_board = self.apply_move(board, move, turn)
                if next_board is None:
                    continue

                next_passes = consecutive_passes + 1 if move is None else 0
                value = min(
                    value,
                    self.alphabeta(next_board, depth - 1, alpha, beta, AI, next_passes)
                )
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value

    def best_move(self, depth=2):
        best_value = -math.inf
        best = None

        for move in self.order_moves(self.board, AI, self.valid_moves(self.board, AI)):
            next_board = self.apply_move(self.board, move, AI)
            if next_board is None:
                continue

            next_passes = 1 if move is None else 0
            value = self.alphabeta(next_board, depth - 1, -math.inf, math.inf, HUMAN, next_passes)

            if value > best_value:
                best_value = value
                best = move

        return best

    def final_score(self):
        black_stones = sum(cell == HUMAN for row in self.board for cell in row)
        white_stones = sum(cell == AI for row in self.board for cell in row)
        return black_stones, white_stones

    def play(self):
        consecutive_passes = 0

        print("=== CO VAY 5x5 - ALPHA BETA ===")
        print("Ban la Den (B), AI la Trang (W)")
        print("Nhap: row col  | vi du: 2 3")
        print("Hoac nhap: pass")
        print("Luat rut gon: co bat quan, co pass, KHONG co ko/superko, KHONG tinh dat chuan.")

        while True:
            self.print_board()

            if consecutive_passes >= 2 or self.board_full(self.board):
                b, w = self.final_score()
                print(f"Ket thuc. Den={b}, Trang={w}")
                if b > w:
                    print("Ban thang!")
                elif w > b:
                    print("AI thang!")
                else:
                    print("Hoa!")
                break

            cmd = input("Nuoc cua ban: ").strip().lower()

            if cmd == "pass":
                consecutive_passes += 1
            else:
                try:
                    r, c = map(int, cmd.split())
                    new_board = self.apply_move(self.board, (r, c), HUMAN)
                    if new_board is None:
                        print("Nuoc di khong hop le.")
                        continue
                    self.board = new_board
                    consecutive_passes = 0
                except:
                    print("Nhap sai. Vi du: 2 3 hoac pass")
                    continue

            if consecutive_passes >= 2 or self.board_full(self.board):
                continue

            ai_move = self.best_move(depth=2)
            if ai_move is None:
                print("AI pass")
                consecutive_passes += 1
            else:
                print("AI di:", ai_move)
                self.board = self.apply_move(self.board, ai_move, AI)
                consecutive_passes = 0


if __name__ == "__main__":
    game = MiniGo(5)
    game.play()