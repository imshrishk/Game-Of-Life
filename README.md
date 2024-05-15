# Conway's Game of Life with Presets, Pattern Rotation, and Scrollable Menu

An interactive implementation of Conway's Game of Life in Python using Pygame. This project features an extensive collection of pattern presets, pattern rotation, and a scrollable menu for easy access. It includes keyboard shortcuts and mouse controls for a fully customizable experience.

## Features

- **Pattern Presets:**
  - Glider
  - Blinker
  - Glider Gun
  - Glider Stopper
  - Toad
  - Beacon
  - Pulsar
  - Spaceship
  - LWSS (Lightweight Spaceship)
  - MWSS (Mediumweight Spaceship)
  - HWSS (Heavyweight Spaceship)
  - Diehard
  - Acorn
  - R-pentomino

- **Pattern Rotation:** Change the direction of patterns using the "Change Direction" button.

- **Scrollable Menu:** Access all patterns and controls using a scrollable menu.

- **Pattern Drawing Mode:** Toggle drawing mode to draw patterns directly on the grid.

## Installation

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/conways-game-of-life.git
    ```
2. **Navigate to the Project Directory:**
    ```bash
    cd conways-game-of-life
    ```
3. **Install Dependencies:**
    Make sure you have Python and Pygame installed:
    ```bash
    pip install pygame
    ```
4. **Run the Project:**
    ```bash
    python game_of_life.py
    ```

- **Mouse Controls:**
  - **Left-click:** Toggle a cell's state
  - **Right-click (drawing mode):** Draw patterns directly on the grid
  - **Scroll Wheel:** Scroll through the menu

- **Keyboard Shortcuts:**
  - `s`: Start simulation
  - `p`: Toggle between play and pause
  - `c`: Clear grid
  - `r`: Randomize grid
  - `l`: Load grid
  - `d`: Increase FPS
  - `a`: Decrease FPS

### Menu Options:

- **Start/Pause:** Start or pause the simulation
- **Clear:** Clear the grid
- **Presets:** Select from various pattern presets
- **Randomize:** Randomly populate the grid
- **Save/Load:** Save or load the current grid state
- **Speed Adjustment:** Increase or decrease the simulation speed
- **Change Direction:** Toggle the pattern direction (right, down, left, up)

## Contributing

Feel free to fork the repository and submit pull requests. Contributions and suggestions are always welcome!

1. Fork the project
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## Credits

- **Pygame** - [Pygame Library](https://www.pygame.org/)
- **Conway's Game of Life** - [Wikipedia](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)

## Acknowledgments

- **John Conway** for creating the Game of Life.
- **Pygame Community** for the excellent Python gaming library.