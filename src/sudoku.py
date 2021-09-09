import pygame
import time

from grid import Grid

class Sudoku:

    SCREEN_WIDTH = 540
    SCREEN_HEIGHT = 600
    GRID_WIDTH = 540
    GRID_HEIGHT = 540
    GRID_SIZE = 9

    def __init__(self, mode='easy'):
        self.caption = pygame.display.set_caption('SUDOKU W/ PYTHON')
        self.screen = pygame.display.set_mode((Sudoku.SCREEN_WIDTH, Sudoku.SCREEN_HEIGHT))
        self.grid = Grid(mode, Sudoku.GRID_SIZE, Sudoku.GRID_SIZE, Sudoku.GRID_WIDTH, Sudoku.GRID_HEIGHT)
        self.display_font = pygame.font.SysFont('Ubuntu Mono', 20, bold=True)
        self.message_font = pygame.font.SysFont('Ubuntu Mono', 15, bold=True)
        self.cell_font = pygame.font.SysFont('Ubuntu Mono', 20, bold=True)
        self.wrong_guesses = 0
        self.key = None
        self.clock = None
        self.start_time = None
        self.total_time = None
        self.running = True
        self.game_loop()

    def handle_k_return(self):
        row, col = self.grid.selected

        if self.grid.cells[row][col].placeholder != 0:
            if self.grid.place(self.grid.cells[row][col].placeholder):
                row, col = self.grid.selected
                self.grid.select(row, col)
            else:
                self.wrong_guesses += 1
                self.key = None

    def handle_key_down(self, event):
        if event.key == pygame.K_1:
            self.key = 1
        if event.key == pygame.K_2:
            self.key = 2
        if event.key == pygame.K_3:
            self.key = 3
        if event.key == pygame.K_4:
            self.key = 4
        if event.key == pygame.K_5:
            self.key = 5
        if event.key == pygame.K_6:
            self.key = 6
        if event.key == pygame.K_7:
            self.key = 7
        if event.key == pygame.K_8:
            self.key = 8
        if event.key == pygame.K_9:
            self.key = 9
        if event.key == pygame.K_RETURN:
            self.handle_k_return()
        if event.key == pygame.K_BACKSPACE:
            self.grid.clear_sketch()
            self.key = None
        if event.key == pygame.K_s:
            # instantly solve the puzzle
            self.grid.clear_selected()
            self.grid.instant_solve()
            self.draw()
        if event.key == pygame.K_v:
            # visually solve the puzzle
            self.grid.clear_selected()
            self.draw()
            self.grid.visual_solve(self.screen, self.cell_font)

    def handle_mouse_button_down(self):
        position = pygame.mouse.get_pos()
        clicked = self.grid.click(position)

        if clicked:
            self.grid.select(clicked[0], clicked[1])
            self.key = None

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            self.handle_key_down(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_button_down()

    def format_time(self):
        secs = self.total_time % 60
        mins = self.total_time // 60
        hrs = mins // 60

        secs = f'0{secs}' if secs < 10 else secs
        mins = f'0{mins}' if mins < 10 else mins
        hrs = f'0{hrs}' if hrs < 10 else hrs

        return f'{hrs}:{mins}:{secs}'

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.grid.draw(self.screen, self.cell_font)
        self.screen.blit(self.display_font.render('X ' * self.wrong_guesses, 1, (255, 0, 0)), (Sudoku.SCREEN_WIDTH - 520, Sudoku.SCREEN_HEIGHT - 40))
        self.screen.blit(self.message_font.render("'v' for visual solve", 1, (0, 0, 0)), (Sudoku.SCREEN_WIDTH - 354, Sudoku.SCREEN_HEIGHT - 50))
        self.screen.blit(self.message_font.render("'s' for instant solve", 1, (0, 0, 0)), (Sudoku.SCREEN_WIDTH - 354, Sudoku.SCREEN_HEIGHT - 26))
        self.screen.blit(self.display_font.render(self.format_time(), 1, (0, 0, 0)), (Sudoku.SCREEN_WIDTH - 130, Sudoku.SCREEN_HEIGHT - 40))

    def game_loop(self):
        self.clock = pygame.time.Clock()
        self.start_time = time.time()

        while self.running:
            self.clock.tick(60)

            if not self.grid.is_finished():
                self.total_time = round(time.time() - self.start_time)

            for event in pygame.event.get():
                self.handle_event(event)

            if self.grid.selected and self.key != None:
                self.grid.sketch(self.key)

            self.draw()

            pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    Sudoku()
    pygame.quit()
