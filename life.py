import pygame
import sys
import random
import pickle

# Constants
WIDTH, HEIGHT = 1300, 750
MENU_WIDTH = 300
CELL_SIZE = 10
GRID_WIDTH, GRID_HEIGHT = (WIDTH - MENU_WIDTH) // CELL_SIZE, HEIGHT // CELL_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# Initial grid setup
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
running = False
dragging_preset = None
draw_mode = False
current_fps = FPS
scroll_offset = 0

# Directions
DIRECTIONS = ["right", "down", "left", "up"]
current_direction = "right"

# Presets
PRESETS = {
    'glider': [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)],
    'blinker': [(0, 1), (1, 1), (2, 1)],
    'glider_gun': [
        (24, 0), (22, 1), (24, 1), (12, 2), (13, 2), (20, 2), (21, 2),
        (34, 2), (35, 2), (11, 3), (15, 3), (20, 3), (21, 3), (34, 3),
        (35, 3), (0, 4), (1, 4), (10, 4), (16, 4), (20, 4), (21, 4),
        (0, 5), (1, 5), (10, 5), (14, 5), (16, 5), (17, 5), (22, 5),
        (24, 5), (10, 6), (16, 6), (24, 6), (11, 7), (15, 7), (12, 8), (13, 8)
    ],
    'glider_stopper': [
        (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
        (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6),
        (6, 5), (6, 4), (6, 3), (6, 2), (6, 1), (6, 0)
    ],
    'toad': [(1, 1), (2, 1), (3, 1), (0, 2), (1, 2), (2, 2)],
    'beacon': [(0, 0), (1, 0), (0, 1), (1, 1), (2, 2), (3, 2), (2, 3), (3, 3)],
    'pulsar': [
        (2, 0), (3, 0), (4, 0), (8, 0), (9, 0), (10, 0),
        (0, 2), (5, 2), (7, 2), (12, 2),
        (0, 3), (5, 3), (7, 3), (12, 3),
        (0, 4), (5, 4), (7, 4), (12, 4),
        (2, 5), (3, 5), (4, 5), (8, 5), (9, 5), (10, 5),
        (2, 7), (3, 7), (4, 7), (8, 7), (9, 7), (10, 7),
        (0, 8), (5, 8), (7, 8), (12, 8),
        (0, 9), (5, 9), (7, 9), (12, 9),
        (0, 10), (5, 10), (7, 10), (12, 10),
        (2, 12), (3, 12), (4, 12), (8, 12), (9, 12), (10, 12)
    ],
    'spaceship': [
        (1, 0), (2, 0), (3, 0), (0, 1), (3, 1), (3, 2),
        (0, 3), (2, 3)
    ],
    'lwss': [
        (1, 0), (4, 0), (0, 1), (0, 2), (4, 2), (0, 3), (1, 3), (2, 3), (3, 3)
    ],
    'mwss': [
        (2, 0), (3, 0), (4, 0), (5, 0), (1, 1), (0, 2), (0, 3), (5, 3),
        (0, 4), (1, 4), (2, 4), (3, 4), (4, 4)
    ],
    'hwss': [
        (3, 0), (4, 0), (5, 0), (6, 0), (2, 1), (1, 2), (1, 3), (6, 3),
        (1, 4), (2, 4), (3, 4), (4, 4), (5, 4)
    ],
    'diehard': [
        (0, 1), (1, 1), (1, 2), (5, 0), (6, 0), (7, 0), (6, 2)
    ],
    'acorn': [
        (1, 0), (3, 1), (0, 2), (1, 2), (4, 2), (5, 2), (6, 2)
    ],
    'r_pentomino': [
        (1, 0), (2, 0), (0, 1), (1, 1), (1, 2)
    ]
}

# Utility Functions
def draw_cells():
    #Draws the live cells in the grid.
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 1:
                pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_menu():
    #Draws the right-side menu with various buttons and labels.
    pygame.draw.rect(screen, BLACK, (WIDTH - MENU_WIDTH, 0, MENU_WIDTH, HEIGHT - 150))

    buttons = [
        ('Start', 50), ('Pause', 100), ('Clear', 150),
        ('Glider', 200), ('Blinker', 250), ('Glider Gun', 300),
        ('Glider Stopper', 350), ('Toad', 400), ('Beacon', 450),
        ('Pulsar', 500), ('Spaceship', 550), ('LWSS', 600),
        ('MWSS', 650), ('HWSS', 700), ('Diehard', 750),
        ('Acorn', 800), ('R-pentomino', 850), ('Randomize', 900),
        ('Save', 950), ('Load', 1000), ('Speed+', 1050), ('Speed-', 1100)
    ]
    for label, ypos in buttons:
        ypos += scroll_offset  # Apply scrolling
        if 0 <= ypos <= HEIGHT - 150:  # Only draw if within the screen
            text = font.render(label, True, WHITE)
            screen.blit(text, (WIDTH - MENU_WIDTH + 20, ypos))

    # Draw the current speed and direction
    speed_text = font.render(f"Speed: {current_fps} FPS", True, WHITE)
    screen.blit(speed_text, (WIDTH - MENU_WIDTH + 20, HEIGHT - 120))

    direction_text = font.render(f"Direction: {current_direction.upper()}", True, WHITE)
    screen.blit(direction_text, (WIDTH - MENU_WIDTH + 20, HEIGHT - 80))

    drawing_text = font.render(f"Drawing Mode: {'ON' if draw_mode else 'OFF'}", True, WHITE)
    screen.blit(drawing_text, (WIDTH - MENU_WIDTH + 20, HEIGHT - 40))

def handle_menu_click(pos):
    #Handles clicks within the menu area.
    x, y = pos
    if WIDTH - MENU_WIDTH <= x <= WIDTH:
        y = y - scroll_offset  # Adjust for scrolling
        if 50 <= y <= 100:
            return 'start'
        elif 100 <= y <= 150:
            return 'pause'
        elif 150 <= y <= 200:
            return 'clear'
        elif 200 <= y <= 250:
            return 'glider'
        elif 250 <= y <= 300:
            return 'blinker'
        elif 300 <= y <= 350:
            return 'glider_gun'
        elif 350 <= y <= 400:
            return 'glider_stopper'
        elif 400 <= y <= 450:
            return 'toad'
        elif 450 <= y <= 500:
            return 'beacon'
        elif 500 <= y <= 550:
            return 'pulsar'
        elif 550 <= y <= 600:
            return 'spaceship'
        elif 600 <= y <= 650:
            return 'lwss'
        elif 650 <= y <= 700:
            return 'mwss'
        elif 700 <= y <= 750:
            return 'hwss'
        elif 750 <= y <= 800:
            return 'diehard'
        elif 800 <= y <= 850:
            return 'acorn'
        elif 850 <= y <= 900:
            return 'r_pentomino'
        elif 900 <= y <= 950:
            return 'randomize'
        elif 950 <= y <= 1000:
            return 'save'
        elif 1000 <= y <= 1050:
            return 'load'
        elif 1050 <= y <= 1100:
            return 'speed+'
        elif 1100 <= y <= 1150:
            return 'speed-'
    return None

def toggle_direction(pos):
    #Changes the direction of patterns when the direction text is clicked.
    x, y = pos
    if WIDTH - MENU_WIDTH + 20 <= x <= WIDTH and HEIGHT - 80 <= y <= HEIGHT - 40:
        global current_direction
        current_direction = DIRECTIONS[(DIRECTIONS.index(current_direction) + 1) % 4]

def rotate_pattern(pattern, direction):
    #Rotates a pattern based on the specified direction.
    if direction == "right":
        return pattern
    elif direction == "down":
        return [(y, -x) for x, y in pattern]
    elif direction == "left":
        return [(-x, -y) for x, y in pattern]
    elif direction == "up":
        return [(-y, x) for x, y in pattern]

def get_neighbors(x, y):
    #Counts the number of live neighbors around a given cell.
    neighbors = 0
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dy == 0 and dx == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                neighbors += grid[ny][nx]
    return neighbors

def update_grid():
    #Applies Conway's Game of Life rules to update the grid.
    global grid
    new_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            neighbors = get_neighbors(x, y)
            if grid[y][x] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[y][x] = 0
                else:
                    new_grid[y][x] = 1
            else:
                if neighbors == 3:
                    new_grid[y][x] = 1
    grid = new_grid

def handle_mouse_click(pos):
    #Toggles the state of a cell based on a mouse click position.
    x, y = pos
    grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
    if grid_x < GRID_WIDTH and grid_y < GRID_HEIGHT:
        grid[grid_y][grid_x] = 1 - grid[grid_y][grid_x]

def place_preset(preset, top_left):
    #Places a preset pattern on the grid starting from a given position.
    global grid
    x_offset, y_offset = top_left
    pattern = rotate_pattern(PRESETS.get(preset, []), current_direction)
    if pattern:
        for dx, dy in pattern:
            if 0 <= x_offset + dx < GRID_WIDTH and 0 <= y_offset + dy < GRID_HEIGHT:
                grid[y_offset + dy][x_offset + dx] = 1

def clear_grid():
    #Clears the entire grid.
    global grid
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def randomize_grid():
    #Fills the grid randomly.
    global grid
    grid = [[random.choice([0, 1]) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def save_grid(filename='game_of_life.sav'):
    #Saves the current grid to a file.
    with open(filename, 'wb') as f:
        pickle.dump(grid, f)

def load_grid(filename='game_of_life.sav'):
    #Loads the grid from a file.
    global grid
    try:
        with open(filename, 'rb') as f:
            grid = pickle.load(f)
    except FileNotFoundError:
        print(f"Save file '{filename}' not found.")

# Main game loop
while True:
    screen.fill(BLACK)
    draw_cells()
    draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            action = handle_menu_click(mouse_pos)
            if action == 'start':
                running = True
            elif action == 'pause':
                running = False
            elif action == 'clear':
                clear_grid()
            elif action == 'randomize':
                randomize_grid()
            elif action == 'save':
                save_grid()
            elif action == 'load':
                load_grid()
            elif action == 'speed+':
                current_fps = min(60, current_fps + 1)
            elif action == 'speed-':
                current_fps = max(1, current_fps - 1)
            elif action in PRESETS:
                dragging_preset = action
            else:
                toggle_direction(mouse_pos)
                handle_mouse_click(mouse_pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_preset:
                mouse_pos = event.pos
                grid_x = mouse_pos[0] // CELL_SIZE
                grid_y = mouse_pos[1] // CELL_SIZE
                place_preset(dragging_preset, (grid_x, grid_y))
                dragging_preset = None
        elif event.type == pygame.MOUSEWHEEL:
            scroll_offset += event.y * 30
            scroll_offset = min(scroll_offset, 0)
            scroll_offset = max(scroll_offset, -(1150 - HEIGHT + 150))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                running = True
            elif event.key == pygame.K_p:
                running = not running
            elif event.key == pygame.K_c:
                clear_grid()
            elif event.key == pygame.K_r:
                randomize_grid()
            elif event.key == pygame.K_s:  # Save with 's'
                save_grid()
            elif event.key == pygame.K_l:  # Load with 'l'
                load_grid()
            elif event.key == pygame.K_d:  # Increase speed with 'd'
                current_fps = min(60, current_fps + 1)
            elif event.key == pygame.K_a:  # Decrease speed with 'a'
                current_fps = max(1, current_fps - 1)
            elif event.key == pygame.K_d:
                draw_mode = not draw_mode

    if running:
        update_grid()

    if draw_mode:
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:  # Left mouse button pressed
            grid_x = mouse_pos[0] // CELL_SIZE
            grid_y = mouse_pos[1] // CELL_SIZE
            if grid_x < GRID_WIDTH and grid_y < GRID_HEIGHT:
                grid[grid_y][grid_x] = 1

    pygame.display.flip()
    clock.tick(current_fps)