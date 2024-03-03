import tkinter as tk
import random

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048")
        self.master.geometry("400x450")

        self.board = [[0]*4 for _ in range(4)]
        self.score = 0
        self.game_over = False

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell = tk.Label(self.frame, text="", width=5, height=2, font=('Arial', 20, 'bold'), bg="lightgray")
                cell.grid(row=i, column=j, padx=5, pady=5)
                row.append(cell)
            self.cells.append(row)

        self.score_label = tk.Label(self.master, text="Score: 0", font=('Arial', 14))
        self.score_label.pack()

        self.new_game_button = tk.Button(self.master, text="Nouvelle partie", command=self.new_game)
        self.new_game_button.pack()

        self.update_board()

        self.master.bind("<Key>", self.key_pressed)

    def update_board(self):
        for i in range(4):
            for j in range(4):
                value = self.board[i][j]
                if value == 0:
                    self.cells[i][j].config(text="", bg="lightgray")
                else:
                    self.cells[i][j].config(text=str(value), bg=self.get_color(value))
        self.score_label.config(text=f"Score: {self.score}")
        if self.is_game_over():
            self.game_over = True
            self.new_game_button.config(state=tk.NORMAL)
            for i in range(4):
                for j in range(4):
                    self.cells[i][j].config(text="Game Over", bg="red", fg="white", font=('Arial', 14, 'bold'))

    def get_color(self, value):
        colors = {
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e"
        }
        return colors.get(value, "#ff0000")

    def add_random_tile(self):
        empty_tiles = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.board[i][j] = 2 if random.random() < 0.9 else 4
            self.update_board()

    def key_pressed(self, event):
        if not self.game_over and event.keysym in ['Up', 'Down', 'Left', 'Right']:
            self.move_tiles(event.keysym)
            self.add_random_tile()
            if self.is_game_over():
                self.game_over = True
                self.new_game_button.config(state=tk.NORMAL)

    def is_game_over(self):
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    return False
                if j > 0 and self.board[i][j] == self.board[i][j-1]:
                    return False
                if i > 0 and self.board[i][j] == self.board[i-1][j]:
                    return False
        return True

    def move_tiles(self, direction):
        if direction == 'Up':
            self.board = self.transpose(self.board)
            self.board = self.move_left(self.board)
            self.board = self.transpose(self.board)
        elif direction == 'Down':
            self.board = self.transpose(self.board)
            self.board = self.reverse_rows(self.board)
            self.board = self.move_left(self.board)
            self.board = self.reverse_rows(self.board)
            self.board = self.transpose(self.board)
        elif direction == 'Left':
            self.board = self.move_left(self.board)
        elif direction == 'Right':
            self.board = self.reverse_rows(self.board)
            self.board = self.move_left(self.board)
            self.board = self.reverse_rows(self.board)
        self.update_board()

    def transpose(self, matrix):
        return [list(row) for row in zip(*matrix)]

    def reverse_rows(self, matrix):
        return [row[::-1] for row in matrix]

    def move_left(self, matrix):
        for i in range(4):
            matrix[i] = self.slide_row(matrix[i])
            matrix[i] = self.merge_row(matrix[i])
            matrix[i] = self.slide_row(matrix[i])
        return matrix

    def slide_row(self, row):
        return [value for value in row if value != 0] + [0] * row.count(0)

    def merge_row(self, row):
        for i in range(len(row)-1):
            if row[i] == row[i+1] and row[i] != 0:
                row[i] *= 2
                self.score += row[i]
                row[i+1] = 0
        return row

    def new_game(self):
        self.board = [[0]*4 for _ in range(4)]
        self.score = 0
        self.game_over = False
        self.update_board()
        self.new_game_button.config(state=tk.DISABLED)

root = tk.Tk()
game = Game2048(root)
root.mainloop()