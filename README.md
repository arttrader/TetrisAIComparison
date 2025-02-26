# Tetris Implementation Comparison

This repository contains various implementations of the classic Tetris game, each created by different AI assistants. These implementations provide interesting insights into different coding styles and approaches to game development using Pygame. Some of them have bugs and don't necessarily run correctly, but I provided unmodified output for comparison purposes. Please keep in mind that these AI assistants are constantly evolving so your mileage may vary.

## Project Overview

The repository includes Tetris implementations from:
- ChatGPT 4o
- ChatGPT o1
- Claude 3.5
- DeepSeek
- DeepSeek 8B
- Gemini
- Grok 3

Each implementation offers a version of Tetris with slightly different features, UI designs, and code structures while maintaining the core Tetris gameplay mechanics.

## Game Features

Common features across implementations:
- Grid-based gameplay with falling tetromino pieces
- Different colored tetromino shapes (I, J, L, O, S, T, Z)
- Piece rotation and movement controls
- Line clearing mechanics
- Game over detection
- Scoring system

Additional features in some versions:
- Next piece preview
- Level progression
- Increasing difficulty
- Visual styling differences

## How to Play

1. Install Python and Pygame if not already installed:
   ```
   pip install pygame
   ```

2. Run any implementation using:
   ```
   python TetrisByX.py
   ```
   (where X is the name of the AI assistant)

### Controls
Most implementations use:
- Left/Right Arrow: Move piece horizontally
- Down Arrow: Move piece down faster
- Up Arrow: Rotate piece
- Space (in some versions): Hard drop

## Implementation Differences

### ChatGPT 4o
Simple implementation with a clean, minimalist design. Features next piece preview and basic scoring.

### ChatGPT o1
More structured code with detailed shape configurations and thorough documentation. Includes level progression and more detailed scoring.

### Claude 3.5
Object-oriented approach with a comprehensive class structure. Features more advanced UI with clear separation of game components.

### DeepSeek
Includes a side panel for displaying the next piece and features a simplified collision detection system.

### DeepSeek 8B
Unique implementation using Turtle graphics instead of Pygame, offering a different visual style and approach.

### Gemini
Features a compact design with a focus on clarity in the code structure and game mechanics.

### Grok 3
More extended UI with a larger display and clear visual boundaries for the play area.

## Learning Resources

These implementations can serve as excellent learning tools for:
- Game development using Pygame
- Different approaches to structuring game logic
- Tetris mechanics implementation
- AI code generation capabilities

## License

These implementations are provided for educational purposes.

---

Feel free to explore, modify, and learn from these different Tetris implementations!