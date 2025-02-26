import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
COLS, ROWS = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (128, 0, 128),  # Purple
    (0, 255, 255),  # Cyan
]

# Tetromino shapes
SHAPES = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 1, 1],
     [1, 1, 0]],

    [[1, 1, 0],
     [0, 1, 1]],

    [[1, 1, 1, 1]],

    [[1, 1],
     [1, 1]],

    [[1, 1, 1],
     [1, 0, 0]],

    [[1, 1, 1],
     [0, 0, 1]],
]

class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = COLS // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

def create_grid(locked_positions):
    grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]
    for (x, y), color in locked_positions.items():
        grid[y][x] = color
    return grid

def draw_grid(surface, grid):
    for y, row in enumerate(grid):
        for x, color in enumerate(row):
            pygame.draw.rect(surface, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    for x in range(COLS):
        pygame.draw.line(surface, WHITE, (x * GRID_SIZE, 0), (x * GRID_SIZE, HEIGHT))
    for y in range(ROWS):
        pygame.draw.line(surface, WHITE, (0, y * GRID_SIZE), (WIDTH, y * GRID_SIZE))

def valid_space(tetromino, grid):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                if (
                    tetromino.x + x < 0 or
                    tetromino.x + x >= COLS or
                    tetromino.y + y >= ROWS or
                    grid[tetromino.y + y][tetromino.x + x] != BLACK
                ):
                    return False
    return True

def clear_lines(grid, locked_positions):
    cleared = 0
    for y in range(ROWS - 1, -1, -1):
        if BLACK not in grid[y]:
            cleared += 1
            del grid[y]
            grid.insert(0, [BLACK for _ in range(COLS)])
            for x in range(COLS):
                if (x, y) in locked_positions:
                    del locked_positions[(x, y)]
    return cleared

def draw_next_tetromino(surface, tetromino):
    font = pygame.font.Font(None, 30)
    label = font.render("Next Shape", True, WHITE)
    surface.blit(label, (WIDTH + 10, 10))
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, tetromino.color, (WIDTH + 10 + x * GRID_SIZE, 50 + y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def main():
    screen = pygame.display.set_mode((WIDTH + 150, HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    locked_positions = {}
    grid = create_grid(locked_positions)

    current_piece = Tetromino(random.choice(SHAPES), random.choice(COLORS))
    next_piece = Tetromino(random.choice(SHAPES), random.choice(COLORS))

    fall_time = 0
    game_over = False

    while not game_over:
        grid = create_grid(locked_positions)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not valid_space(current_piece, grid):
                        for _ in range(3):
                            current_piece.rotate()

        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 > 0.5:
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
                for y, row in enumerate(current_piece.shape):
                    for x, cell in enumerate(row):
                        if cell:
                            locked_positions[(current_piece.x + x, current_piece.y + y)] = current_piece.color
                current_piece = next_piece
                next_piece = Tetromino(random.choice(SHAPES), random.choice(COLORS))
                if not valid_space(current_piece, grid):
                    game_over = True
            fall_time = 0

        clear_lines(grid, locked_positions)

        screen.fill(BLACK)
        draw_grid(screen, grid)
        draw_next_tetromino(screen, next_piece)
        for y, row in enumerate(current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, current_piece.color, ((current_piece.x + x) * GRID_SIZE, (current_piece.y + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
