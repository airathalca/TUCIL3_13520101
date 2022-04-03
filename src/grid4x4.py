from puzzle import *
from time import sleep
from tkinter import *
from tkinter import filedialog as fd

class gridFrame(Frame):
    def __init__(self, window, puzzle):
        super().__init__(window)
        self.puzzle = puzzle
        self.buttons = [None] * 16
        self.create_grid()
        self.pack(pady=5, padx=15, side=LEFT)

    def create_grid(self):
        for i in range(4):
            for j in range(4):
                self.create(4*i + j, i, j)

    def create(self, index, i, j):
        if (self.puzzle.matrix[i][j] == 16):
            txttoplace = ""
        else:
            txttoplace = str(self.puzzle.matrix[i][j])
        self.buttons[index] = Label(self,bg="dodger blue", borderwidth = 2, relief  = 'solid', text = txttoplace, justify = LEFT, font=("Comic Sans MS", "11"), width=7, height=3)
        self.buttons[index].grid(row=i, column=j)

    def change_button(self):
        x = 0
        for i in self.buttons:
            if (self.puzzle.matrix[x//4][x%4] == 16):
                txttoplace = ""
            else:
                txttoplace = str(self.puzzle.matrix[x//4][x%4])
            i.configure(text = txttoplace)
            x += 1
    
    def change(self, matrix):
        x = 0
        for i in self.buttons:
            if (matrix[x//4][x%4] == 16):
                txttoplace = ""
            else:
                txttoplace = str(matrix[x//4][x%4])
            i.configure(text = txttoplace)
            x += 1

    def path(self, solution, window):
        if(solution.parent is None):
            printMatrix(solution.matrix)
            print()
            return
        else:
            self.path(solution.parent, window)
            printMatrix(solution.matrix)
            print()
            self.change(solution.matrix)
            sleep(0.2)
            window.update()