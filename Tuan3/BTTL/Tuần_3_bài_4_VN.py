import tkinter as tk
from tkinter import messagebox
import math

EMPTY = ' '
HUMAN = 'O'
AI = 'X'

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TicTacToe - Alpha Beta")
        self.board = [[EMPTY for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    root,
                    text=' ',
                    font=('Arial', 24),
                    width=5,
                    height=2,
                    command=lambda r=i, c=j: self.player_move(r, c)
                )
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

        reset_btn = tk.Button(root, text="Chơi lại", font=('Arial', 14), command=self.reset_game)
        reset_btn.grid(row=3, column=0, columnspan=3, sticky="nsew")

    def check_winner(self):
        b = self.board

        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] != EMPTY:
                return b[i][0]

        for j in range(3):
            if b[0][j] == b[1][j] == b[2][j] != EMPTY:
                return b[0][j]

        if b[0][0] == b[1][1] == b[2][2] != EMPTY:
            return b[0][0]

        if b[0][2] == b[1][1] == b[2][0] != EMPTY:
            return b[0][2]

        return None

    def is_full(self):
        return all(cell != EMPTY for row in self.board for cell in row)

    def alphabeta(self, alpha, beta, is_maximizing):
        winner = self.check_winner()

        if winner == AI:
            return 1
        elif winner == HUMAN:
            return -1
        elif self.is_full():
            return 0

        if is_maximizing:
            value = -math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == EMPTY:
                        self.board[i][j] = AI
                        value = max(value, self.alphabeta(alpha, beta, False))
                        self.board[i][j] = EMPTY
                        alpha = max(alpha, value)
                        if alpha >= beta:
                            return value
            return value
        else:
            value = math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == EMPTY:
                        self.board[i][j] = HUMAN
                        value = min(value, self.alphabeta(alpha, beta, True))
                        self.board[i][j] = EMPTY
                        beta = min(beta, value)
                        if alpha >= beta:
                            return value
            return value

    def best_move(self):
        best_score = -math.inf
        move = None

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == EMPTY:
                    self.board[i][j] = AI
                    score = self.alphabeta(-math.inf, math.inf, False)
                    self.board[i][j] = EMPTY

                    if score > best_score:
                        best_score = score
                        move = (i, j)

        return move

    def player_move(self, row, col):
        if self.board[row][col] != EMPTY:
            return

        self.board[row][col] = HUMAN
        self.buttons[row][col].config(text=HUMAN, state='disabled')

        if self.check_winner() == HUMAN:
            messagebox.showinfo("Kết quả", "Bạn thắng!")
            self.disable_all()
            return

        if self.is_full():
            messagebox.showinfo("Kết quả", "Hòa!")
            return

        move = self.best_move()
        if move:
            r, c = move
            self.board[r][c] = AI
            self.buttons[r][c].config(text=AI, state='disabled')

        if self.check_winner() == AI:
            messagebox.showinfo("Kết quả", "Máy thắng!")
            self.disable_all()
            return

        if self.is_full():
            messagebox.showinfo("Kết quả", "Hòa!")

    def disable_all(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state='disabled')

    def reset_game(self):
        self.board = [[EMPTY for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=' ', state='normal')

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()
