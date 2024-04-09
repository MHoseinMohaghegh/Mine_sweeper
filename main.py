# Import necessary modules
from tkinter import *
from cell import Cell  # Assuming 'cell' module contains the Cell class
import settings  # Settings module containing constants
import calculator  # Calculator module for utility functions

# Create the main Tkinter window
root = Tk()
root.configure(bg='black')
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
root.title('MineSweeper')
root.resizable(False, False)

# Top frame for additional controls or information
top_frame = Frame(root, bg='brown', width=settings.WIDTH,
                  height=calculator.height_prct(20))
top_frame.place(x=0, y=0)

# Left frame for additional controls or information
left_frame = Frame(root, bg='silver', width=calculator.width_prct(
    15), height=calculator.height_prct(80))
left_frame.place(x=0, y=calculator.height_prct(20))

# Center frame for the MineSweeper grid
center_frame = Frame(root, bg='black', width=calculator.width_prct(
    85), height=calculator.height_prct(80))
center_frame.place(x=calculator.width_prct(15), y=calculator.height_prct(20))

# Create MineSweeper grid using Cell objects
for x in range(9):
    for y in range(5):
        c = Cell(x, y)
        c.create_btn_object(center_frame)
        c.cell_btn_object.grid(column=x, row=y)

# 'End' button for ending the game
end_button = Button(top_frame, text='End', width=20,
                    height=3, bg='teal', font=12)
end_button.place(x=427, y=14)
end_button.bind('<Button-1>', Cell.check_win)

# Create and place MineSweeper cell count label
Cell.create_cell_count_label(left_frame)
Cell.cell_count_label_object.place(x=0, y=0)

# Randomize mine placement on the MineSweeper grid
Cell.randomize_mines()

# Run the Tkinter window
root.mainloop()
