import turtle
import random
from collections import deque

# Set up the screen
screen = turtle.Screen()
screen.title("Tetris")
screen.setup(600, 800)
screen.setworldcoordinates(-1.5, -1.5, 14.5, 20.5)
turtle.speed(0)
turtle.delay(0)

# Game constants
BOARD_WIDTH = 14
BOARD_HEIGHT = 20
BLOCK_SIZE = 30

# Colors for the blocks (RGB tuples)
COLORS = {
    0: (0, 0, 0),   # Empty cell
    1: (0, 0, 255), # I-block
    2: (0, 255, 0), # T-block
    3: (255, 0, 0), # S-block
    4: (255, 255, 0), # Z-block
    5: (255, 165, 0), # J-block
    6: (0, 255, 255), # L-block
    7: (255, 0, 255)  # O-block
}

# Tetromino shapes for each type (0-7)
SHAPES = {
    1: [[1, 1, 1, 1]],                       # I
    2: [[0, 1, 0], [1, 1, 1]],              # T
    3: [[0, 1], [1, 1], [1, 0]],            # S
    4: [[1, 1], [0, 1], [0, 0]],            # Z
    5: [[1, 0], [1, 0], [1, 1]],            # J
    6: [[0, 1], [0, 1], [1, 1]],            # L
    7: [[1, 1], [1, 1]]                     # O
}

# Initialize the game board
board = [[0 for _ in range(BOARD_WIDTH)] for __ in range(BOARD_HEIGHT)]
score = 0
speed = 30

def draw_block(x, y, color):
    """Draw a single block at (x, y) with given color."""
    turtle.penup()
    turtle.goto(x * BLOCK_SIZE + 1.5, y * BLOCK_SIZE + 1.5)
    if color != COLORS[0]:
        turtle.color(color)
        turtle.begin_fill()
    else:
        pass
    turtle.pendown()
    for _ in range(4):
        turtle.forward(BLOCK_SIZE - 2)
        turtle.left(90)
    if color != COLORS[0]:
        turtle.end_fill()

def draw():
    """Draw the entire game board and blocks."""
    global board

    # Clear screen
    turtle.clear()

    # Draw the board
    for y in range(len(board)):
        for x in range(len(board[y])):
            draw_block(x, len(board) - y - 1, COLORS[board[y][x]])

def create_piece(type):
    """Create a new piece of given type."""
    shape = SHAPES[type]
    return {
        'type': type,
        'shape': shape,
        'position': [random.randint(0, BOARD_WIDTH - len(shape[0])),
                    0], # Starting position (x, y)
        'color': COLORS[type]
    }

def get_collision(piece):
    """Check if the current piece has collided with the board or boundaries."""
    for y in range(len(piece['shape'])):
        for x in range(len(piece['shape'][y])):
            if piece['shape'][y][x]:
                px = piece['position'][0] + x
                py = piece['position'][1] + y

                # Check boundaries
                if px < 0 or px >= BOARD_WIDTH or py >= BOARD_HEIGHT:
                    return True
                if py < 0 and board[py][px] != 0:
                    return True

    return False

def lock_piece(piece):
    """Lock the piece in place on the board."""
    for y in range(len(piece['shape'])):
        for x in range(len(piece['shape'][y])):
            if piece['shape'][y][x]:
                px = piece['position'][0] + x
                py = piece['position'][1] + y
                board[py][px] = piece['type']

def clear_lines():
    """Clear any complete lines on the board."""
    global score, speed

    new_board = []
    lines_cleared = 0

    for row in board:
        if sum(row) == BOARD_WIDTH:
            lines_cleared += 1
        else:
            new_board.append(row)

    # Update score and speed
    score += [40 * (lines_cleared - 2 + i) ** 2 for i in range(lines_cleared)][-1]
    speed = max(5, speed - (speed // 10))

    # Rebuild the board without cleared lines
    while len(new_board) < BOARD_HEIGHT:
        new_board.append([0] * BOARD_WIDTH)

    board[:] = new_board

def rotate_piece(piece):
    """Rotate the piece 90 degrees clockwise."""
    if get_collision(piece): return  # No rotation if collision detected

    new_shape = []
    for y in range(len(piece['shape'][0])):
        new_row = []
        for x in reversed(range(len(piece['shape']))):

            new_row.append(piece['shape'][x][y])
        new_shape.append(new_row)

    old_shape = piece['shape']
    piece['shape'] = new_shape

def move_down(piece):
    """Move the current piece down one row."""
    if not get_collision(piece):
        piece['position'][1] += 1
        draw()

def move_left(piece):
    """Move the current piece left one column."""
    if not get_collision(piece):
        piece['position'][0] -= 1
        draw()

def move_right(piece):
    """Move the current piece right one column."""
    if not get_collision(piece):
        piece['position'][0] += 1
        draw()

current_piece = create_piece(random.randint(1, 7))
game_over = False

# Set up event handlers
turtle.listen()
turtle.onkey(lambda: move_left(current_piece), 'Left')
turtle.onkey(lambda: move_right(current_piece), 'Right')
turtle.onkey(lambda: rotate_piece(current_piece), 'Down')
turtle.onkey(lambda: move_down(current_piece), 'Up')



# Main game loop
while not game_over:
    draw()
    if get_collision(current_piece):
        lock_piece(current_piece)
        clear_lines()
        current_piece = create_piece(random.randint(1, 7))

        # Check for game over (if new piece can't be placed)
        if get_collision(current_piece):
            print("Game Over! Score: {}".format(score))
            break

    else:
        move_down(current_piece)

turtle.done()
