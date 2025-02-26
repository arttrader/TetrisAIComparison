import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 300
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define shapes
shapes = [
    [  # I
        ['.....',
         '0000',
         '.....',
         '.....'],
        ['..0..',
         '..0..',
         '..0..',
         '..0..']
    ],
    [  # J
        ['.....',
         '.0...',
         '.000',
         '.....'],
        ['..00',
         '..0..',
         '..0..',
         '.....'],
        ['.....',
         '000.',
         '...0',
         '.....'],
        ['..0..',
         '..0..',
         '00...',
         '.....']
    ],
    [  # L
        ['.....',
         '...0',
         '000.',
         '.....'],
        ['..0..',
         '..0..',
         '..00',
         '.....'],
        ['.....',
         '.000',
         '.0...',
         '.....'],
        ['.00..',
         '..0..',
         '..0..',
         '.....']
    ],
    [  # O
        ['.....',
         '.00.',
         '.00.',
         '.....']
    ],
    [  # S
        ['.....',
         '..00',
         '.00.',
         '.....'],
        ['..0..',
         '..00',
         '...0',
         '.....']
    ],
    [  # T
        ['.....',
         '.000',
         '..0..',
         '.....'],
        ['..0..',
         '.00.',
         '..0..',
         '.....'],
        ['.....',
         '..0..',
         '.000',
         '.....'],
        ['..0..',
         '.00..',
         '..0..',
         '.....']
    ],
    [  # Z
        ['.....',
         '.00.',
         '..00',
         '.....'],
        ['...0',
         '..00',
         '..0..',
         '.....']
    ]
]

# Define shape colors
shape_colors = [CYAN, BLUE, MAGENTA, YELLOW, GREEN, RED, WHITE]

# Define grid size
grid_width = 10
grid_height = 20
block_size = 30

# Calculate play area position
top_left_x = (screen_width - grid_width * block_size) // 2
top_left_y = screen_height - grid_height * block_size - 50

# Create the grid
grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]


class Tetromino:
    """
    Represents a single Tetromino piece.

    Attributes:
        x (int): X-coordinate of the tetromino's top-left corner.
        y (int): Y-coordinate of the tetromino's top-left corner.
    """

    def __init__(self):
        """Initialize a new random Tetromino."""
        self.shape = random.choice(shapes)
        self.color = shape_colors[shapes.index(self.shape)]
        self.x = grid_width // 2 - len(self.shape[0]) // 2
        self.y = 0
        self.rotation = 0

    def move(self, dx, dy):
        """
        Move the tetromino if the move is valid.

        Args:
            dx (int): Change in x-coordinate.
            dy (int): Change in y-coordinate.
        """
        if self.valid_move(dx, dy, self.rotation):
            self.x += dx
            self.y += dy

    def rotate(self):
        """Rotate the tetromino clockwise."""
        new_rotation = (self.rotation + 1) % len(self.shape)
        if self.valid_move(0, 0, new_rotation):
            self.rotation = new_rotation

    def valid_move(self, dx, dy, new_rotation):
        """
        Check if the tetromino can move to the given position.

        Args:
            dx (int): Change in x-coordinate.
            dy (int): Change in y-coordinate.
            new_rotation (int): New rotation index.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        for i, row in enumerate(self.shape[new_rotation]):
            for j, cell in enumerate(row):
                if cell == '0':
                    new_x = self.x + j + dx
                    new_y = self.y + i + dy
                    if (new_x < 0 or new_x >= grid_width or
                            new_y >= grid_height or (new_y >= 0 and grid[new_y][new_x])):
                        return False
        return True


def draw_grid():
    """Draw the game grid on the screen."""
    for i in range(grid_height):
        for j in range(grid_width):
            pygame.draw.rect(screen, WHITE,
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 1)


def draw_tetromino(tetromino):
    """Draw the tetromino on the screen."""
    for i, row in enumerate(tetromino.shape[tetromino.rotation]):
        for j, cell in enumerate(row):
            if cell == '0':
                pygame.draw.rect(screen, tetromino.color,
                                 (top_left_x + (tetromino.x + j) * block_size,
                                  top_left_y + (tetromino.y + i) * block_size,
                                  block_size, block_size))


def clear_lines():
    """Clear any completed lines and return the number of lines cleared."""
    lines_cleared = 0
    for i in range(grid_height):
        if all(grid[i]):
            lines_cleared += 1
            del grid[i]
            grid.insert(0, [0 for _ in range(grid_width)])
    return lines_cleared


def game_over():
    """Display the game over message."""
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Game Over', 1, WHITE)
    screen.blit(label, (top_left_x + grid_width * block_size / 2 - label.get_width() / 2,
                        top_left_y + grid_height * block_size / 2 - label.get_height() / 2))


# Game loop
clock = pygame.time.Clock()
fall_speed = 0.27
fall_time = 0
current_piece = Tetromino()
game_over_flag = False
score = 0

while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_piece.move(-1, 0)
            if event.key == pygame.K_RIGHT:
                current_piece.move(1, 0)
            if event.key == pygame.K_DOWN:
                fall_speed = 0.05
            if event.key == pygame.K_UP:
                current_piece.rotate()

    if not game_over_flag:
        # Move the piece down
        fall_time += clock.get_rawtime()
        clock.tick()
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.move(0, 1)
            if not current_piece.valid_move(0, 1, current_piece.rotation):
                # Lock the piece in place
                for i, row in enumerate(current_piece.shape[current_piece.rotation]):
                    for j, cell in enumerate(row):
                        if cell == '0':
                            grid[current_piece.y + i][current_piece.x + j] = current_piece.color
                # Clear lines and update score
                score += clear_lines() * 100
                # Create a new piece
                current_piece = Tetromino()
                # Check if game over
                if not current_piece.valid_move(0, 0, current_piece.rotation):
                    game_over_flag = True

    # Draw everything
    screen.fill(BLACK)
    draw_grid()
    draw_tetromino(current_piece)
    if game_over_flag:
        game_over()

    # Display the score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, WHITE)
    screen.blit(label, (top_left_x + grid_width * block_size / 2 - label.get_width() / 2, 30))

    pygame.display.flip()