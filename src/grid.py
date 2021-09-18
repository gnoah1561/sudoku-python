import pygame
import requests

from cell import Cell
from solver import SudokuSolver

class Grid:
    """This class represents a grid (i.e. puzzle)."

    def __init__(self, mode, rows, cols, width, height):
        self.solver = SudokuSolver()
        self.response = requests.get(f'https://sugoku.herokuapp.com/board?difficulty={mode}')
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.original_cells = self.response.json()['board']
        self.cells = [[Cell(self.original_cells[i][j], i, j, width / 9, height / 9) for j in range(cols)] for i in range(rows)]
        self.model = None
        self.selected = None

    def update_model(self):
        self.model = [[self.cells[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, value):
        row, col = self.selected

        if self.cells[row][col].value == 0:
            self.cells[row][col].set_value(value)
            self.update_model()

            if self.solver.valid(self.model, value, (row, col)) and self.solver.solve(self.model):
                return True

            self.cells[row][col].set_value(0)
            self.cells[row][col].set_placeholder(0)
            self.update_model()

            return False

    def sketch(self, value):
        row, col = self.selected
        self.cells[row][col].set_placeholder(value)

    def draw(self, screen, font):
        # grid lines
        gap = self.width / 9

        for i in range(self.rows + 1):
            line_size = 4 if (i % 3 == 0 and i != 0) else 1

            pygame.draw.line(screen, (0, 0, 0), (0, i * gap), (self.width, i * gap), line_size)
            pygame.draw.line(screen, (0, 0, 0), (i * gap, 0), (i * gap, self.height), line_size)

        # cell values
        for i in range(self.rows):
            for j in range(self.cols):
                if self.original_cells[i][j] != 0:
                    self.cells[i][j].draw(screen, font, (255, 0, 0))
                else:
                    self.cells[i][j].draw(screen, font, (0, 0, 0))

    def instant_solve(self):
        self.update_model()
        empty_coord = self.solver.next_empty_coord(self.model)

        if not empty_coord:
            return True

        row, col = empty_coord

        for guess in range(1, 10):
            if self.solver.valid(self.model, guess, (row, col)):
                self.model[row][col] = guess
                self.cells[row][col].set_value(guess)
                self.update_model()

                if (self.instant_solve()):
                    return True

                self.model[row][col] = 0
                self.cells[row][col].set_value(0)
                self.update_model()

        return False

    def visual_solve(self, screen, font):
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                pygame.quit()

        self.update_model()
        empty_coord = self.solver.next_empty_coord(self.model)

        if not empty_coord:
            return True

        row, col = empty_coord

        for guess in range(1, 10):
            if self.solver.valid(self.model, guess, (row, col)):
                self.model[row][col] = guess
                self.cells[row][col].set_value(guess)
                self.update_model()
                self.cells[row][col].visual_solve_draw(screen, font)

                pygame.display.update()
                pygame.time.delay(50)

                if self.visual_solve(screen, font):
                    return True

                self.model[row][col] = 0
                self.cells[row][col].set_value(0)
                self.update_model()
                self.cells[row][col].visual_solve_draw(screen, font, False)

                pygame.display.update()
                pygame.time.delay(50)

        return False

    def clear_selected(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].selected = False

    def select(self, row, col):
        selected_value = self.cells[row][col].value

        # set all selected values of the selected number to true
        for i in range(self.rows):
            for j in range(self.cols):
                if selected_value != 0:
                    if self.cells[i][j].value == selected_value:
                        self.cells[i][j].selected = True
                    else:
                        self.cells[i][j].selected = False
                else:
                    self.clear_selected()
                    self.cells[row][col].selected = True
                    break

        self.selected = (row, col)

    def clear_sketch(self):
        row, col = self.selected

        if self.cells[row][col].value == 0:
            self.cells[row][col].set_placeholder(0)

    def click(self, position):
        if position[0] < self.width and position[1] < self.height:
            gap = self.width / 9
            x = position[0] // gap
            y = position[1] // gap

            return (int(y), int(x))

        return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cells[i][j].value == 0:
                    return False

        return True
