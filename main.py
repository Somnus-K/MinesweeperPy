import pygame
import random
import sys
import os

pygame.init()

#Constants

#grid size, mine count
DIFFICULTIES = {
    "easy": (8, 8, 10),
    "medium": (16, 16, 40),
    "hard": (16, 30, 99)
}
HEADER = 50
ROWS, COLS = 10, 10
CELL_SIZE = 60
WIDTH, HEIGHT = (CELL_SIZE * ROWS), (CELL_SIZE * COLS) + HEADER
BUTTON_WIDTH = max(80, WIDTH // 10)
BUTTON_HEIGHT = 40
reset_button_x = WIDTH // 2 - BUTTON_WIDTH - 10  # Left of center
menu_button_x = WIDTH // 2 + 10  # Right of center
reset_button = pygame.Rect(reset_button_x, 5, BUTTON_WIDTH, BUTTON_HEIGHT)
menu_button = pygame.Rect(menu_button_x, 5, BUTTON_WIDTH, BUTTON_HEIGHT)
MINE_COUNT = 15
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

def resource_path(relative_path):
    """ Get the absolute path for assets, compatible with PyInstaller """
    if hasattr(sys, '_MEIPASS'):  # When running from an .exe
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

#Assets Loading
images = {
    "covered": pygame.image.load(resource_path("Assets/covered.png")),
    "flag": pygame.image.load(resource_path("Assets/flag.png")),
    "mine": pygame.image.load(resource_path("Assets/seamine.png")),
    "mine_hit": pygame.image.load(resource_path("Assets/clickedmine.png")),
    "0": pygame.image.load(resource_path("Assets/0.png")),
    "1": pygame.image.load(resource_path("Assets/1.png")),
    "2": pygame.image.load(resource_path("Assets/2.png")),
    "3": pygame.image.load(resource_path("Assets/3.png")),
    "4": pygame.image.load(resource_path("Assets/4.png")),
    "5": pygame.image.load(resource_path("Assets/5.png")),
    "6": pygame.image.load(resource_path("Assets/6.png")),
    "7": pygame.image.load(resource_path("Assets/7.png")),
    "8": pygame.image.load(resource_path("Assets/8.png"))
}


for key in images:
    images[key] = pygame.transform.scale(images[key], (CELL_SIZE, CELL_SIZE))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
def start_screen():
    """Display the difficulty selection menu."""
    screen.fill(WHITE)
    font = pygame.font.Font(None, 50)
    title_text = font.render("Select Difficulty", True, GREY)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

    # Difficulty buttons
    buttons = {}
    button_y = 150
    for difficulty in DIFFICULTIES:
        button_rect = pygame.Rect(WIDTH // 2 - 100, button_y, 200, 50)
        buttons[difficulty] = button_rect
        pygame.draw.rect(screen, GREY, button_rect, border_radius=5)
        text = font.render(difficulty, True, WHITE)
        screen.blit(text, (button_rect.x + 40, button_rect.y + 10))
        button_y += 80

    pygame.display.flip()

    # Wait for user to click a difficulty
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for difficulty, rect in buttons.items():
                    if rect.collidepoint(x, y):
                        while pygame.mouse.get_pressed()[0]:
                            pygame.event.pump()
                        pygame.event.clear()
                        pygame.time.delay(100)
                        return difficulty  # Return selected difficulty


selected_difficulty = None

# Show the start screen and get the chosen difficulty
difficulty_choice = start_screen()
ROWS, COLS, MINE_COUNT = DIFFICULTIES[difficulty_choice]  # Apply chosen difficulty

# Recalculate screen size based on selection
WIDTH, HEIGHT = (CELL_SIZE * COLS), (CELL_SIZE * ROWS) + HEADER
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#Screen Setup
pygame.display.set_caption("Minesweeper")

#Board Generation
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]

#Mine Generation for Board
mines = set(random.sample(range(ROWS * COLS), MINE_COUNT))
for mine in mines:
    row, col = divmod(mine, COLS)
    board[row][col] = -1
#Counts adjacent mines
def count_mines(r, c):
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == -1:
                count += 1
    return count

for r in range(ROWS):
    for c in range(COLS):
        if board[r][c] != -1:
            board[r][c] = count_mines(r, c)

def flood_fill(r, c):
    """Recursively reveals all 0 tiles and their neighbors"""
    if not 0 <= r < ROWS and 0 <= c < COLS:
        return
    if revealed[r][c] or flagged[r][c]:
        return
    if board[r][c] == -1:
        return
    revealed[r][c] = True
    if board [r][c] == 0:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    flood_fill(nr, nc)

def check_win():
    for r in range(ROWS):
        for c in range(COLS):
            if not revealed[r][c] and board[r][c] != -1:
                return False
    return True

def reveal_mines():
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == -1:
                revealed[r][c] = True

def draw_board():
    for r in range(ROWS):
        for c in range(COLS):
            x, y = c * CELL_SIZE, r * CELL_SIZE + HEADER
            if flagged[r][c]:
                screen.blit(images["flag"], (x, y))
            elif revealed[r][c]:
                if board[r][c] == -1:
                    if (r, c) == clicked_mine:
                        screen.blit(images["mine_hit"], (x, y))
                    else:
                        screen.blit(images["mine"], (x, y))
                else:
                    screen.blit(images[str(board[r][c])], (x, y))
            else:
                screen.blit(images["covered"], (x, y))

def reset_game():
    global board, revealed, flagged, mines, start_time, game_over
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]
    game_over = False

    mines = set(random.sample(range(ROWS * COLS), MINE_COUNT))
    for mine in mines:
        row, col = divmod(mine, COLS)
        board[row][col] = -1

    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != -1:
                board[r][c] = count_mines(r, c)

    start_time = pygame.time.get_ticks()




start_time = pygame.time.get_ticks()
font = pygame.font.Font(None, 36)

clicked_mine = None

game_over = False

#Game Loop
running = True
while running:
    screen.fill(WHITE)

    if not game_over:
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    time_text = font.render(str(f"Time: {elapsed_time}s"), True, GREY)

    flags_placed = sum(row.count(True) for row in flagged)
    mines_remaining = MINE_COUNT - flags_placed
    mine_text = font.render(str(f"Mines: {mines_remaining}"), True, GREY)
    screen.blit(time_text, (10, 10))
    mine_counter_x = WIDTH - mine_text.get_width() - 10
    screen.blit (mine_text, (mine_counter_x, 10))
    menu_button.x = mine_counter_x - BUTTON_WIDTH - 10
    reset_button.x = menu_button.x - BUTTON_WIDTH - 10

    # Draw Reset Button
    pygame.draw.rect(screen, GREY, reset_button, border_radius=5)
    reset_text = font.render("Reset", True, WHITE)
    screen.blit(reset_text, (reset_button.x + 10, reset_button.y + 10))

    # Draw Main Menu Button
    pygame.draw.rect(screen, GREY, menu_button, border_radius=5)
    menu_text = font.render("Menu", True, WHITE)
    screen.blit(menu_text, (menu_button.x + 10, menu_button.y + 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            if reset_button.collidepoint(x, y):
                reset_game()
                continue

            if menu_button.collidepoint(x, y):
                difficulty_choice = start_screen()
                ROWS, COLS, MINE_COUNT = DIFFICULTIES[difficulty_choice]
                WIDTH, HEIGHT = (CELL_SIZE * COLS), (CELL_SIZE * ROWS) + HEADER
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
                reset_game()
                continue

            if y >= HEADER:
                row, col = (y - HEADER) // CELL_SIZE, x // CELL_SIZE

            if event.button == 1 and not flagged[row][col]:
                if board[row][col] == -1:
                    clicked_mine = (row, col)
                    reveal_mines()
                    print("Game Over.")
                    game_over = True
                    draw_board()
                    pygame.display.flip()
                    #pygame.time.delay(2000)
                    #running = False
                if board[row][col] == 0:
                    flood_fill(row, col)
                else:
                    revealed[row][col] = True
                if check_win():
                    print("You win!")
                    game_over = True
                    #running = False
            elif event.button == 3:
                if not revealed[row][col] and flags_placed < MINE_COUNT:
                    flagged[row][col] = not flagged[row][col]

    draw_board()
    pygame.display.flip()

pygame.quit()