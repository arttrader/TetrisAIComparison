import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# --------------------------
#         SETTINGS
# --------------------------
# Grid size
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30  # Pixel size of each block

# Screen dimensions
SCREEN_WIDTH = BLOCK_SIZE * GRID_WIDTH
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT
FPS = 60

# Colors (R, G, B)
BLACK   = (0,   0,   0)
WHITE   = (255, 255, 255)
GRAY    = (128, 128, 128)
RED     = (255, 0,   0)
GREEN   = (0,   255, 0)
BLUE    = (0,   0,   255)
CYAN    = (0,   255, 255)
MAGENTA = (255, 0,   255)
YELLOW  = (255, 255, 0)
ORANGE  = (255, 165, 0)

# Shape configurations (Tetriminoes).
# Each shape is defined by a list of lists of coordinates (x, y).
# The center (pivot for rotation) is generally the top-left or near the middle of the shape grid.
SHAPES = [
    # S
    [['.....',
      '.....',
      '..XX.',
      '.XX..',
      '.....'],
     ['.....',
      '..X..',
      '..XX.',
      '...X.',
      '.....']],
    # Z
    [['.....',
      '.....',
      '.XX..',
      '..XX.',
      '.....'],
     ['.....',
      '...X.',
      '..XX.',
      '..X..',
      '.....']],
    # I
    [['..X..',
      '..X..',
      '..X..',
      '..X..',
      '.....'],
     ['.....',
      '.....',
      'XXXX.',
      '.....',
      '.....']],
    # O
    [['.....',
      '.....',
      '.XX..',
      '.XX..',
      '.....']],
    # J
    [['.....',
      '.X...',
      '.XXX.',
      '.....',
      '.....'],
     ['.....',
      '..XX.',
      '..X..',
      '..X..',
      '.....'],
     ['.....',
      '.....',
      '.XXX.',
      '...X.',
      '.....'],
     ['.....',
      '..X..',
      '..X..',
      '.XX..',
      '.....']],
    # L
    [['.....',
      '...X.',
      '.XXX.',
      '.....',
      '.....'],
     ['.....',
      '..X..',
      '..X..',
      '..XX.',
      '.....'],
     ['.....',
      '.....',
      '.XXX.',
      '.X...',
      '.....'],
     ['.....',
      '.XX..',
      '..X..',
      '..X..',
      '.....']],
    # T
    [['.....',
      '..X..',
      '.XXX.',
      '.....',
      '.....'],
     ['.....',
      '..X..',
      '..XX.',
      '..X..',
      '.....'],
     ['.....',
      '.....',
      '.XXX.',
      '..X..',
      '.....'],
     ['.....',
      '..X..',
      '.XX..',
      '..X..',
      '.....']]
]

# Associated colors for each shape
SHAPE_COLORS = [GREEN, RED, CYAN, YELLOW, ORANGE, BLUE, MAGENTA]

# --------------------------
#     DATA STRUCTURES
# --------------------------

class Piece:
    """Represents a Tetris piece with shape, rotation index, color, and position."""
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0  # index into the shape's rotation list

# --------------------------
#    HELPER FUNCTIONS
# --------------------------

def create_grid(locked_positions=None):
    """Returns a 2D list of colors, representing the Tetris grid."""
    if locked_positions is None:
        locked_positions = {}

    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for (col, row), color in locked_positions.items():
        if row >= 0:
            grid[row][col] = color
    return grid

def convert_shape_format(piece):
    """Convert the shape string array into a list of (x,y) positions relative to the piece's top-left."""
    positions = []
    shape_format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == 'X':
                positions.append((piece.x + j, piece.y + i))

    # Remove any empty rows
    return positions

def valid_space(piece, grid):
    """Check if the piece is within the valid area and not colliding with existing blocks."""
    accepted_positions = [[(j, i) for j in range(GRID_WIDTH) if grid[i][j] == BLACK] for i in range(GRID_HEIGHT)]
    accepted_positions = [pos for row in accepted_positions for pos in row]

    formatted = convert_shape_format(piece)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:  # ignore positions above the top
                return False
    return True

def check_lost(positions):
    """Check if any locked block is above the top of the grid, indicating game over."""
    for (x, y) in positions:
        if y < 0:
            return True
    return False

def get_shape():
    """Return a new random piece from SHAPES."""
    return SHAPES[random.randint(0, len(SHAPES)-1)]

def draw_text_middle(text, size, color, surface):
    """Draw text in the middle of the given surface."""
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface_width = surface.get_width()
    surface_height = surface.get_height()

    label_x = (surface_width - label.get_width()) // 2
    label_y = (surface_height - label.get_height()) // 2

    surface.blit(label, (label_x, label_y))

def draw_grid(surface, grid):
    """Draw the grid lines on the surface."""
    for i in range(GRID_HEIGHT):
        # horizontal lines
        pygame.draw.line(surface, GRAY, (0, i*BLOCK_SIZE), (SCREEN_WIDTH, i*BLOCK_SIZE))
    for j in range(GRID_WIDTH):
        # vertical lines
        pygame.draw.line(surface, GRAY, (j*BLOCK_SIZE, 0), (j*BLOCK_SIZE, SCREEN_HEIGHT))

def clear_rows(grid, locked):
    """
    Clear completed rows from the grid and update locked positions.
    Returns the number of cleared lines.
    """
    lines_cleared = 0
    # Go bottom-up so that when we remove a row, we shift everything down
    for i in range(GRID_HEIGHT-1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            # This row is full, remove it
            lines_cleared += 1
            # Remove all locked blocks in that row
            for j in range(GRID_WIDTH):
                try:
                    del locked[(j, i)]
                except KeyError:
                    pass
            # Shift rows above down
            for key in sorted(list(locked), key=lambda x: x[1]):
                x, y = key
                if y < i:
                    newKey = (x, y + 1)
                    locked[newKey] = locked.pop(key)
    return lines_cleared

def draw_window(surface, grid, score=0):
    """Draw the main game window, including the grid and the current score."""
    surface.fill(BLACK)

    # Title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, WHITE)
    surface.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, 10))

    # Draw the blocks in the grid
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            pygame.draw.rect(surface, grid[i][j],
                             (j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    # Draw the grid lines
    draw_grid(surface, grid)

    # Score
    font = pygame.font.SysFont('comicsans', 30)
    score_label = font.render(f'Score: {score}', 1, WHITE)
    surface.blit(score_label, (10, 10 + label.get_height()))

    pygame.display.update()

# --------------------------
#         MAIN GAME
# --------------------------

def main_game(surface):
    locked_positions = {}  # (x,y):(color)
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = Piece(GRID_WIDTH // 2 - 2, 0, get_shape())
    next_piece = Piece(GRID_WIDTH // 2 - 2, 0, get_shape())
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5  # lower = faster piece
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick(FPS)

        # Increase speed every 10 seconds
        if level_time/1000 > 10:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        # Piece falling logic
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                # lock the piece
                for pos in convert_shape_format(current_piece):
                    locked_positions[(pos[0], pos[1])] = current_piece.color
                change_piece = True

        # Check Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                elif event.key == pygame.K_DOWN:
                    # move piece down
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                elif event.key == pygame.K_UP:
                    # rotate piece
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)

        piece_pos = convert_shape_format(current_piece)
        # Draw current piece on the grid
        for x, y in piece_pos:
            if y >= 0:
                grid[y][x] = current_piece.color

        # If piece is locked, generate a new piece
        if change_piece:
            lines_cleared = clear_rows(grid, locked_positions)
            score += lines_cleared * 10
            current_piece = next_piece
            next_piece = Piece(GRID_WIDTH // 2 - 2, 0, get_shape())
            change_piece = False

            # Check if game over
            if check_lost(locked_positions):
                run = False

        draw_window(surface, grid, score=score)

    # Display "You Lost"
    surface.fill(BLACK)
    draw_text_middle("YOU LOST", 60, WHITE, surface)
    pygame.display.update()
    pygame.time.delay(2000)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')
    main_game(screen)

if __name__ == '__main__':
    main()
