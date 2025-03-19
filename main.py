import pygame
import random

pygame.init()

#Constants

HEADER = 100
ROWS, COLS = 10, 10
CELL_SIZE = 50
WIDTH, HEIGHT = (CELL_SIZE * ROWS), (CELL_SIZE * COLS) + HEADER
MINE_COUNT = 15
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

#Assets Loading
images = {
    "covered": pygame.image.load("Assets/covered.png"),
    "flag": pygame.image.load("Assets/flag.png"),
    "mine": pygame.image.load("Assets/seamine.png"),
    "0": pygame.image.load("Assets/0.png"),
    "1": pygame.image.load("Assets/1.png"),
    "2": pygame.image.load("Assets/2.png"),
    "3": pygame.image.load("Assets/3.png"),
    "4": pygame.image.load("Assets/4.png"),
    "5": pygame.image.load("Assets/5.png"),
    "6": pygame.image.load("Assets/6.png"),
    "7": pygame.image.load("Assets/7.png"),
    "8": pygame.image.load("Assets/8.png")
}


for key in images:
    images[key] = pygame.transform.scale(images[key], (CELL_SIZE, CELL_SIZE))

#Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
                    screen.blit(images["mine"], (x, y))
                else:
                    screen.blit(images[str(board[r][c])], (x, y))
            else:
                screen.blit(images["covered"], (x, y))

start_time = pygame.time.get_ticks()
font = pygame.font.Font(None, 36)

#Game Loop
running = True
while running:
    screen.fill(WHITE)

    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    time_text = font.render(str(f"Time: {elapsed_time}s"), True, GREY)

    flags_placed = sum(row.count(True) for row in flagged)
    mines_remaining = MINE_COUNT - flags_placed
    mine_text = font.render(str(f"Mines: {mines_remaining}"), True, GREY)
    screen.blit(time_text, (10, 10))
    screen.blit (mine_text, (WIDTH - mine_text.get_width() - 10, 10))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if y >= HEADER:
                row, col = (y - HEADER) // CELL_SIZE, x // CELL_SIZE

            if event.button == 1 and not flagged[row][col]:
                if board[row][col] == -1:
                    reveal_mines()
                    print("Game Over.")
                    draw_board()
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    running = False
                if board[row][col] == 0:
                    flood_fill(row, col)
                else:
                    revealed[row][col] = True
                if check_win():
                    print("You win!")
                    running = False
            elif event.button == 3:
                if not revealed[row][col] and flags_placed < MINE_COUNT:
                    flagged[row][col] = not flagged[row][col]

    draw_board()
    pygame.display.flip()

pygame.quit()