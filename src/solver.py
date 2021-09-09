from pprint import pprint
from timeit import default_timer as timer

def is_in_row(grid, number, coordinate):
    row, col = coordinate

    for j in range(9):
        if grid[row][j] == number and col != j:
            return True

    return False

def is_in_col(grid, number, coordinate):
    row, col = coordinate

    for i in range(9):
        if grid[i][col] == number and row != i:
            return True

    return False

def is_in_box(grid, number, coordinate):
    box_x = coordinate[1] // 3
    box_y = coordinate[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if grid[i][j] == number and (i, j) != coordinate:
                return True

    return False

def valid(grid, number, coordinate):
    in_row = is_in_row(grid, number, coordinate)
    in_col = is_in_col(grid, number, coordinate)
    in_box = is_in_box(grid, number, coordinate)

    return not in_row and not in_col and not in_box

def next_empty_coord(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i, j)

    return None

def solve(grid):
    empty_coord = next_empty_coord(grid)

    if not empty_coord:
        return True

    row, col = empty_coord

    for guess in range(1, 10):
        if valid(grid, guess, (row, col)):
            grid[row][col] = guess

            if solve(grid):
                return True

            grid[row][col] = 0

    return False

class SudokuSolver:

    # private
    def __is_in_row(self, grid, number, coordinate):
        row, col = coordinate

        for j in range(9):
            if grid[row][j] == number and col != j:
                return True

        return False

    def __is_in_col(self, grid, number, coordinate):
        row, col = coordinate

        for i in range(9):
            if grid[i][col] == number and row != i:
                return True

        return False

    def __is_in_box(self, grid, number, coordinate):
        box_x = coordinate[1] // 3
        box_y = coordinate[0] // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if grid[i][j] == number and (i, j) != coordinate:
                    return True

        return False

    # public
    def next_empty_coord(self, grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return (i, j)

        return None

    def valid(self, grid, number, coordinate):
        in_row = self.__is_in_row(grid, number, coordinate)
        in_col = self.__is_in_col(grid, number, coordinate)
        in_box = self.__is_in_box(grid, number, coordinate)

        return not in_row and not in_col and not in_box

    def solve(self, grid):
        empty_coord = next_empty_coord(grid)

        if not empty_coord:
            return True

        row, col = empty_coord

        for guess in range(1, 10):
            if valid(grid, guess, (row, col)):
                grid[row][col] = guess

                if solve(grid):
                    return True

                grid[row][col] = 0

        return False

if __name__ == '__main__':

    puzzle = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    solver = SudokuSolver()

    pprint(puzzle)

    start_time = timer()
    solved = solver.solve(puzzle)
    time_elapsed_in_seconds = timer() - start_time

    if (solved):
        print(f'\nThis puzzle was solved in {time_elapsed_in_seconds} seconds :)\n')
    else:
        print('\nThis puzzle is unsolvable... :(\n')

    pprint(puzzle)
