# Import necessary modules
from tkinter import Button, Label
import random
import settings
import ast
import ctypes
import sys

# Class representing a MineSweeper cell


class Cell:
    all = []  # List to store all created Cell instances
    cell_count = settings.CELL_COUNT  # Initial cell count
    cell_count_label_object = None  # Label object for displaying cell count
    real_mines = 12  # Total number of mines
    green_mines = 0  # Number of correctly flagged mines
    red_mines = 0  # Number of revealed mines

    # Constructor for Cell class
    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.cell_btn_object = None
        self.x = x
        self.y = y
        self.is_revealed = False  # Initialize to False
        self.is_flagged = False  # Initialize to False
        Cell.all.append(self)  # Add current instance to the list

    # Method to create a Button object for the cell
    def create_btn_object(self, location):
        btn = Button(location, text=f'{self.x},{self.y}', width=12, height=5)
        btn.bind('<Button-1>', self.left_click_actions)
        btn.bind('<Button-3>', lambda event: self.right_click_actions(event))
        self.cell_btn_object = btn

    # Static method to create the cell count label
    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(location, bg='azure', fg='dark red', font=('', 15),
                    text=f'Cells Left:{settings.CELL_COUNT}', width=13, height=4)
        Cell.cell_count_label_object = lbl

    # Method to handle left-click actions on a cell
    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            self.show_cell(self.x, self.y)

    # Method to retrieve a cell based on its coordinates
    def get_cell_by_axis(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    # Static method to check for win condition
    @staticmethod
    def check_win(event):
        if Cell.red_mines + Cell.green_mines == Cell.real_mines:
            ctypes.windll.user32.MessageBoxW(
                0, f'Red mines = {Cell.red_mines}, Green mines = {Cell.green_mines}, Total mines = {Cell.real_mines}', 'Congratulation', 0)
        else:
            ctypes.windll.user32.MessageBoxW(
                0, f'Red mines = {Cell.red_mines}, Green mines = {Cell.green_mines}, Total mines = {Cell.real_mines}', 'Game Over', 0)

    # Method to reveal a cell and update count
    def show_cell(self, x, y):
        if self.cell_btn_object.cget("bg") == 'green':
            Cell.green_mines -= 1
        if self.cell_btn_object.cget("bg") != 'green' and self.cell_btn_object.cget("bg") != 'white':
            Cell.cell_count -= 1
        if self.is_valid_cell(x, y):
            around_mines = 0
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    if i == x and j == y:
                        continue
                    adjacent_cell = self.get_cell_by_axis(i, j)
                    if adjacent_cell and adjacent_cell.is_mine:
                        around_mines += 1
            self.text = str(around_mines)
            self.cell_btn_object.configure(text=self.text)
            self.is_flagged = True
            self.cell_btn_object.configure(bg='white')
            if around_mines == 0:
                for number1 in range(x - 1, x + 2):
                    for number2 in range(y - 1, y + 2):
                        adjacent_cell = self.get_cell_by_axis(number1, number2)
                        if adjacent_cell and adjacent_cell.is_valid_cell(number1, number2) and not adjacent_cell.is_flagged:
                            adjacent_cell.show_cell(number1, number2)
        if Cell.cell_count_label_object:
            Cell.cell_count_label_object.configure(
                text=f'Left Cells:{Cell.cell_count}')

    # Method to reveal a mine and handle game over
    def show_mine(self):
        if self.cell_btn_object.cget("bg") == 'green':
            Cell.green_mines -= 1
        else:
            if self.cell_btn_object.cget("bg") != 'red':
                Cell.cell_count -= 1
            Cell.cell_count_label_object.configure(
                text=f'Left Cells:{Cell.cell_count}')
        if self.cell_btn_object.cget("bg") != 'red':
            self.cell_btn_object.configure(bg='red')
            Cell.red_mines += 1
        ctypes.windll.user32.MessageBoxW(
            0, 'You clicked on a mine...', 'Mine Exploded', 0)

    # Method to handle right-click actions on a cell
    def right_click_actions(self, event):
        button = event.widget
        button_text = button.cget("text")
        if len(button_text) > 1:
            i, j = map(int, button_text.split(','))
            self.get_cell_by_axis(i, j)
            if button.cget("bg") == 'green' or button.cget("bg") == 'red':
                pass
            else:
                Cell.cell_count -= 1
                self.cell_btn_object.configure(bg='green')
                Cell.cell_count_label_object.configure(
                    text=f'Left Cells:{Cell.cell_count}')
                Cell.green_mines += 1

    # Method to check if a cell is flagged
    def is_flagged(self):
        return self.is_flagged

    # Method to check if a cell is within valid bounds
    def is_valid_cell(self, x, y):
        if x >= 0 and x < 9 and y < 5 and y >= 0:
            return True
        return False

    # Static method to randomize mine placement
    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(Cell.all, Cell.real_mines)
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    # String representation of the Cell instance
    def __repr__(self):
        return f'Cell({self.x}, {self.y})'
