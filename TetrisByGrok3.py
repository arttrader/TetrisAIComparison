import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
PLAY_WIDTH = 300  # 10 blocks wide (30px each)
PLAY_HEIGHT = 600  # 20 blocks tall (30px each)
BLOCK_SIZE = 30

# Positioning the play area in the center
TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - PLAY_HEIGHT - 50

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Tetromino shapes (each is a list of rotations)
SHAPES = [
    [['.....', '.....', '.000.', '.....', '.....'], ['..0..', '..0..', '..0..', '..0..', '.....']],  # I
    [['.....', '.....', '.00..', '.00..', '.....']],  # O
    [['.....', '.....', '.000.', '..0..', '.....'], ['..0..', '..0..', '.00..', '.....', '.....']],  # T
    [['.....', '.....', '.000.', '.0...', '.....'], ['..0..', '..00.', '..0..', '.....', '.....']],  # L
    [['.....', '.....', '.000.', '...0.', '.....'], ['..0..', '.00..', '..0..', '.....', '.....']],  # J
    [['.....', '.....', '..00.', '.00..', '.....'], ['..0..', '..00.', '...0.', '.....', '.....']],  # S
    [['.....', '.....', '.00..', '..00.', '.....'], ['...0.', '..00.', '..0..', '.....', '.....']]   # Z
]

SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, GREEN, RED]

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris by Grok")
clock = pygame.time.Clock()

class Piece:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = random.choice(SHAPES)
        self.color = SHAPE_COLORS[SHAPES.index(self.shape)]
        self.rotation = 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(10)] for _ in range(20)]
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]
    return grid

def valid_space(piece, grid):
    accepted_pos = [[(x, y) for x in range(10) if grid[y][x] == BLACK] for y in range(20)]
    accepted_pos = [pos for sublist in accepted_pos for pos in sublist]

    formatted = convert_shape_format(piece)
    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:  # Ignore positions above the grid during initial spawn
                return False
    return True

def convert_shape_format(piece):
    positions = []
    shape = piece.shape[piece.rotation]
    for i, line in enumerate(shape):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j - 2, piece.y + i - 4))  # Offset for centering
    return positions

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 0:  # Top of the screen
            return True
    return False

def clear_rows(grid, locked):
    rows_cleared = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            rows_cleared += 1
            for j in range(len(row)):
                del locked[(j, i)]
            # Shift rows down
            for y in range(i-1, -1, -1):
                for x in range(len(grid[y])):
                    if (x, y) in locked:
                        color = locked[(x, y)]
                        del locked[(x, y)]
                        locked[(x, y + 1)] = color
    return rows_cleared

def draw_grid(surface, grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x],
                           (TOP_LEFT_X + x * BLOCK_SIZE, TOP_LEFT_Y + y * BLOCK_SIZE,
                            BLOCK_SIZE, BLOCK_SIZE), 0)
            pygame.draw.rect(surface, GRAY,
                           (TOP_LEFT_X + x * BLOCK_SIZE, TOP_LEFT_Y + y * BLOCK_SIZE,
                            BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_window(surface, grid, score):
    surface.fill(BLACK)
    # Draw title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, WHITE)
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH / 2 - label.get_width() / 2, 20))
    # Draw score
    font = pygame.font.SysFont('comicsans', 30)
    score_label = font.render(f'Score: {score}', 1, WHITE)
    surface.blit(score_label, (TOP_LEFT_X - 150, TOP_LEFT_Y + 200))
    # Draw play area
    draw_grid(surface, grid)
    pygame.draw.rect(surface, RED, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)

def main():
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = Piece(5, 0)
    next_piece = Piece(5, 0)
    fall_time = 0
    fall_speed = 0.5  # Seconds
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        # Piece falling logic
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.move(0, 1)
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.move(0, -1)
                change_piece = True

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.move(-1, 0)
                    if not valid_space(current_piece, grid):
                        current_piece.move(1, 0)
                if event.key == pygame.K_RIGHT:
                    current_piece.move(1, 0)
                    if not valid_space(current_piece, grid):
                        current_piece.move(-1, 0)
                if event.key == pygame.K_DOWN:
                    current_piece.move(0, 1)
                    if not valid_space(current_piece, grid):
                        current_piece.move(0, -1)
                if event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not valid_space(current_piece, grid):
                        current_piece.rotate()  # Rotate back if invalid
                        current_piece.rotate()
                        current_piece.rotate()

        # Add piece to grid when it lands
        if change_piece:
            for pos in convert_shape_format(current_piece):
                locked_positions[pos] = current_piece.color
            current_piece = next_piece
            next_piece = Piece(5, 0)
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        # Draw current piece
        for pos in convert_shape_format(current_piece):
            x, y = pos
            if y >= 0:
                grid[y][x] = current_piece.color

        draw_window(screen, grid, score)

        # Check game over
        if check_lost(locked_positions):
            run = False

        pygame.display.update()

    # Game over screen
    font = pygame.font.SysFont('comicsans', 50)
    label = font.render('Game Over', 1, WHITE)
    screen.blit(label, (TOP_LEFT_X + PLAY_WIDTH / 2 - label.get_width() / 2,
                       TOP_LEFT_Y + PLAY_HEIGHT / 2 - label.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()

if __name__ == "__main__":
    main()