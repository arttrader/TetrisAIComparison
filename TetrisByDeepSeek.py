import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400  # Increased width to accommodate next piece display
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  # Cyan (I)
    (255, 255, 0),  # Yellow (O)
    (255, 165, 0),  # Orange (L)
    (0, 0, 255),    # Blue (J)
    (0, 255, 0),    # Green (S)
    (255, 0, 0),    # Red (Z)
    (128, 0, 128)   # Purple (T)
]

# Shapes and their rotations
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1, 1], [0, 1, 0]]   # T
]

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Clock
clock = pygame.time.Clock()

# Grid
grid = [[0 for _ in range(10)] for _ in range(20)]  # 10x20 grid

def draw_grid():
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x]:
                pygame.draw.rect(screen, COLORS[grid[y][x] - 1], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def new_piece():
    shape_index = random.randint(0, len(SHAPES) - 1)
    shape = SHAPES[shape_index]
    color = shape_index + 1  # Assign color based on shape index
    piece = {
        'shape': shape,
        'color': color,
        'x': 5 - len(shape[0]) // 2,  # Center the piece
        'y': 0
    }
    return piece

def draw_piece(piece, offset_x=0, offset_y=0):
    for y, row in enumerate(piece['shape']):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, COLORS[piece['color'] - 1], ((piece['x'] + x + offset_x) * BLOCK_SIZE, (piece['y'] + y + offset_y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def check_collision(piece):
    for y, row in enumerate(piece['shape']):
        for x, cell in enumerate(row):
            if cell:
                if piece['y'] + y >= len(grid) or piece['x'] + x < 0 or piece['x'] + x >= len(grid[0]) or grid[piece['y'] + y][piece['x'] + x]:
                    return True
    return False

def merge_piece(piece):
    for y, row in enumerate(piece['shape']):
        for x, cell in enumerate(row):
            if cell:
                grid[piece['y'] + y][piece['x'] + x] = piece['color']

def clear_lines():
    lines_cleared = 0
    for y in range(len(grid) - 1, -1, -1):
        if all(grid[y]):
            del grid[y]
            grid.insert(0, [0 for _ in range(len(grid[0]))])
            lines_cleared += 1
    return lines_cleared

def game_over():
    font = pygame.font.SysFont('comicsans', 50)
    text = font.render('Game Over', True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(3000)

def drop_piece(piece):
    while not check_collision(piece):
        piece['y'] += 1
    piece['y'] -= 1  # Move back up one step after collision

def draw_next_piece(next_piece):
    font = pygame.font.SysFont('comicsans', 30)
    text = font.render('Next Piece:', True, WHITE)
    screen.blit(text, (320, 50))
    # Draw the next piece in the sidebar
    for y, row in enumerate(next_piece['shape']):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, COLORS[next_piece['color'] - 1], (320 + x * BLOCK_SIZE, 100 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def main():
    piece = new_piece()
    next_piece = new_piece()
    fall_time = 0
    fall_speed = 500
    running = True

    while running:
        screen.fill(BLACK)
        draw_grid()
        draw_piece(piece)
        draw_next_piece(next_piece)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    piece['x'] -= 1
                    if check_collision(piece):
                        piece['x'] += 1
                if event.key == pygame.K_RIGHT:
                    piece['x'] += 1
                    if check_collision(piece):
                        piece['x'] -= 1
                if event.key == pygame.K_DOWN:
                    piece['y'] += 1
                    if check_collision(piece):
                        piece['y'] -= 1
                if event.key == pygame.K_UP:
                    rotated_piece = list(zip(*reversed(piece['shape'])))
                    if not check_collision({'shape': rotated_piece, 'x': piece['x'], 'y': piece['y'], 'color': piece['color']}):
                        piece['shape'] = rotated_piece
                if event.key == pygame.K_SPACE:  # Drop the piece
                    drop_piece(piece)

        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time >= fall_speed:
            fall_time = 0
            piece['y'] += 1
            if check_collision(piece):
                piece['y'] -= 1
                merge_piece(piece)
                lines_cleared = clear_lines()
                if lines_cleared:
                    fall_speed = max(100, fall_speed - 10 * lines_cleared)
                piece = next_piece
                next_piece = new_piece()
                if check_collision(piece):
                    game_over()
                    running = False

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()