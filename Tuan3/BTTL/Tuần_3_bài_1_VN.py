import math

EMPTY = '.'
AI = 'X'
HUMAN = 'O'

class TicTacToeNxN:
    def __init__(self, n=5, win_len=None):
        self.n = n
        self.win_len = win_len if win_len else n
        self.board = [[EMPTY for _ in range(n)] for _ in range(n)]

    def print_board(self):
        for row in self.board:
            print(" ".join(row))
        print()

    def is_full(self):
        return all(cell != EMPTY for row in self.board for cell in row)

    def get_valid_moves(self):
        return [(i, j) for i in range(self.n) for j in range(self.n) if self.board[i][j] == EMPTY]

    def check_winner(self):
        n = self.n
        k = self.win_len
        b = self.board
        directions = [(1,0), (0,1), (1,1), (1,-1)]

        for i in range(n):
            for j in range(n):
                if b[i][j] == EMPTY:
                    continue
                player = b[i][j]

                for dx, dy in directions:
                    count = 0
                    x, y = i, j
                    while 0 <= x < n and 0 <= y < n and b[x][y] == player:
                        count += 1
                        if count == k:
                            return player
                        x += dx
                        y += dy
        return None

    def evaluate_line(self, line):
        ai_count = line.count(AI)
        human_count = line.count(HUMAN)

        if ai_count > 0 and human_count > 0:
            return 0
        if ai_count == 0 and human_count == 0:
            return 0
        if ai_count > 0:
            return 10 ** ai_count
        if human_count > 0:
            return -(10 ** human_count)
        return 0

    def evaluate_board(self):
        winner = self.check_winner()
        if winner == AI:
            return 1000000
        elif winner == HUMAN:
            return -1000000

        score = 0
        n = self.n
        k = self.win_len
        b = self.board

        for i in range(n):
            for j in range(n - k + 1):
                score += self.evaluate_line([b[i][j+t] for t in range(k)])

        for j in range(n):
            for i in range(n - k + 1):
                score += self.evaluate_line([b[i+t][j] for t in range(k)])

        for i in range(n - k + 1):
            for j in range(n - k + 1):
                score += self.evaluate_line([b[i+t][j+t] for t in range(k)])

        for i in range(n - k + 1):
            for j in range(k - 1, n):
                score += self.evaluate_line([b[i+t][j-t] for t in range(k)])

        return score

    def alphabeta(self, depth, alpha, beta, is_maximizing):
        winner = self.check_winner()

        if winner == AI:
            return 1000000
        elif winner == HUMAN:
            return -1000000
        elif self.is_full() or depth == 0:
            return self.evaluate_board()

        if is_maximizing:
            value = -math.inf
            for i, j in self.get_valid_moves():
                self.board[i][j] = AI
                value = max(value, self.alphabeta(depth - 1, alpha, beta, False))
                self.board[i][j] = EMPTY
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = math.inf
            for i, j in self.get_valid_moves():
                self.board[i][j] = HUMAN
                value = min(value, self.alphabeta(depth - 1, alpha, beta, True))
                self.board[i][j] = EMPTY
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value

    def best_move(self, depth=3):
        best_score = -math.inf
        move = None

        for i, j in self.get_valid_moves():
            self.board[i][j] = AI
            score = self.alphabeta(depth - 1, -math.inf, math.inf, False)
            self.board[i][j] = EMPTY

            if score > best_score:
                best_score = score
                move = (i, j)

        return move


if __name__ == "__main__":
    game = TicTacToeNxN(n=5, win_len=4)
    game.print_board()

    while True:
        r = int(input("Nhập hàng: "))
        c = int(input("Nhập cột: "))

        if game.board[r][c] != EMPTY:
            print("Ô đã có quân.")
            continue

        game.board[r][c] = HUMAN
        game.print_board()

        if game.check_winner() == HUMAN:
            print("Bạn thắng!")
            break

        if game.is_full():
            print("Hòa!")
            break

        move = game.best_move(depth=3)
        if move:
            game.board[move[0]][move[1]] = AI

        game.print_board()

        if game.check_winner() == AI:
            print("Máy thắng!")
            break

        if game.is_full():
            print("Hòa!")
            break
