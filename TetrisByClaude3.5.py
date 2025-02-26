import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 6)  # Extra space for score/next piece
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)  # I piece
BLUE = (0, 0, 255)  # J piece
ORANGE = (255, 165, 0)  # L piece
YELLOW = (255, 255, 0)  # O piece
GREEN = (0, 255, 0)  # S piece
PURPLE = (128, 0, 128)  # T piece
RED = (255, 0, 0)  # Z piece

# Tetromino shapes and their rotations
SHAPES = {
    'I': [[(0, 1), (1, 1), (2, 1), (3, 1)],
          [(2, 0), (2, 1), (2, 2), (2, 3)]],
    'J': [[(0, 0), (0, 1), (1, 1), (2, 1)],
          [(1, 0), (2, 0), (1, 1), (1, 2)],
          [(0, 1), (1, 1), (2, 1), (2, 2)],
          [(1, 0), (1, 1), (1, 2), (0, 2)]],
    'L': [[(2, 0), (0, 1), (1, 1), (2, 1)],
          [(1, 0), (1, 1), (1, 2), (2, 2)],
          [(0, 1), (1, 1), (2, 1), (0, 2)],
          [(0, 0), (1, 0), (1, 1), (1, 2)]],
    'O': [[(1, 0), (2, 0), (1, 1), (2, 1)]],
    'S': [[(1, 0), (2, 0), (0, 1), (1, 1)],
          [(1, 0), (1, 1), (2, 1), (2, 2)]],
    'T': [[(1, 0), (0, 1), (1, 1), (2, 1)],
          [(1, 0), (1, 1), (2, 1), (1, 2)],
          [(0, 1), (1, 1), (2, 1), (1, 2)],
          [(1, 0), (0, 1), (1, 1), (1, 2)]],
    'Z': [[(0, 0), (1, 0), (1, 1), (2, 1)],
          [(2, 0), (1, 1), (2, 1), (1, 2)]]
}

SHAPE_COLORS = {
    'I': CYAN,
    'J': BLUE,
    'L': ORANGE,
    'O': YELLOW,
    'S': GREEN,
    'T': PURPLE,
    'Z': RED
}


class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        self.fall_time = 0
        self.fall_speed = 500  # Start with 0.5 seconds per drop
        self.level = 1

    def new_piece(self):
        shape = random.choice(list(SHAPES.keys()))
        return {
            'shape': shape,
            'rotation': 0,
            'x': GRID_WIDTH // 2 - 2,
            'y': 0
        }

    def get_piece_positions(self, piece):
        shape_coords = SHAPES[piece['shape']][piece['rotation'] % len(SHAPES[piece['shape']])]
        return [(x + piece['x'], y + piece['y']) for x, y in shape_coords]

    def valid_move(self, piece):
        positions = self.get_piece_positions(piece)
        return all(0 <= x < GRID_WIDTH and y < GRID_HEIGHT and
                   (y < 0 or self.grid[y][x] == BLACK)
                   for x, y in positions)

    def merge_piece(self):
        positions = self.get_piece_positions(self.current_piece)
        for x, y in positions:
            if y >= 0:
                self.grid[y][x] = SHAPE_COLORS[self.current_piece['shape']]
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        if not self.valid_move(self.current_piece):
            self.game_over = True

    def clear_lines(self):
        lines_cleared = 0
        y = GRID_HEIGHT - 1
        while y >= 0:
            if all(self.grid[y][x] != BLACK for x in range(GRID_WIDTH)):
                lines_cleared += 1
                for y2 in range(y, 0, -1):
                    self.grid[y2] = self.grid[y2 - 1][:]
                self.grid[0] = [BLACK] * GRID_WIDTH
            else:
                y -= 1

        if lines_cleared > 0:
            self.score += (lines_cleared ** 2) * 100
            self.level = self.score // 1000 + 1
            self.fall_speed = max(100, 500 - (self.level - 1) * 50)  # Speed up as level increases

    def draw(self):
        self.screen.fill(BLACK)

        # Draw the grid
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(self.screen, self.grid[y][x],
                                 (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        # Draw current piece
        for x, y in self.get_piece_positions(self.current_piece):
            if y >= 0:
                pygame.draw.rect(self.screen, SHAPE_COLORS[self.current_piece['shape']],
                                 (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        # Draw next piece preview
        preview_x = GRID_WIDTH * BLOCK_SIZE + BLOCK_SIZE
        preview_y = 2 * BLOCK_SIZE
        pygame.draw.rect(self.screen, WHITE,
                         (preview_x, preview_y, 5 * BLOCK_SIZE, 5 * BLOCK_SIZE), 1)

        preview_piece = self.next_piece.copy()
        preview_piece['x'] = GRID_WIDTH + 2
        preview_piece['y'] = 3
        for x, y in self.get_piece_positions(preview_piece):
            pygame.draw.rect(self.screen, SHAPE_COLORS[preview_piece['shape']],
                             (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        # Draw score and level
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        level_text = self.font.render(f'Level: {self.level}', True, WHITE)
        self.screen.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 10, 8 * BLOCK_SIZE))
        self.screen.blit(level_text, (GRID_WIDTH * BLOCK_SIZE + 10, 9 * BLOCK_SIZE))

        if self.game_over:
            game_over_text = self.font.render('GAME OVER', True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)

        pygame.display.flip()

    def run(self):
        while True:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN and not self.game_over:
                    new_piece = self.current_piece.copy()

                    if event.key == pygame.K_LEFT:
                        new_piece['x'] -= 1
                    elif event.key == pygame.K_RIGHT:
                        new_piece['x'] += 1
                    elif event.key == pygame.K_UP:
                        new_piece['rotation'] = (new_piece['rotation'] + 1) % len(SHAPES[new_piece['shape']])
                    elif event.key == pygame.K_DOWN:
                        new_piece['y'] += 1
                    elif event.key == pygame.K_SPACE:
                        # Hard drop
                        while self.valid_move(new_piece):
                            self.current_piece = new_piece.copy()
                            new_piece['y'] += 1
                        self.merge_piece()
                        new_piece = self.current_piece

                    if self.valid_move(new_piece):
                        self.current_piece = new_piece

                elif event.type == pygame.KEYDOWN and self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()

            # Handle automatic falling
            if not self.game_over:
                if current_time - self.fall_time > self.fall_speed:
                    self.fall_time = current_time
                    new_piece = self.current_piece.copy()
                    new_piece['y'] += 1

                    if self.valid_move(new_piece):
                        self.current_piece = new_piece
                    else:
                        self.merge_piece()

            self.draw()
            self.clock.tick(60)


if __name__ == '__main__':
    game = Tetris()
    game.run()