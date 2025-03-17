import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 10, 10
#CELL_SIZE = WIDTH // COLS
MINE_COUNT = 15
#
WHITE = (255, 255, 255)
#BLACK = (0, 0, 0)
GREY = (128, 128, 128)
#RED = (255, 0, 0)

#Images
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

CELL_SIZE = 50

for key in images:
    images[key] = pygame.transform.scale(images[key], (CELL_SIZE, CELL_SIZE))

#Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

#Board Generation
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]

mines = set(random.sample(range(ROWS * COLS), MINE_COUNT))
for mine in mines:
    row, col = divmod(mine, COLS)
    board[row][col] = -1

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

#Game Loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            col, row = x // CELL_SIZE, y // CELL_SIZE

            if event.button == 1 and not flagged[row][col]:
                revealed[row][col] = True
            elif event.button == 3:
                flagged[row][col] = not flagged[row][col]

    for r in range(ROWS):
        for c in range(COLS):
            x, y = c * CELL_SIZE, r * CELL_SIZE
            if flagged[r][c]:
                screen.blit(images["flag"], (x, y))
            elif revealed[r][c]:
                if board[r][c] == -1:
                    screen.blit(images["mine"], (x, y))
                else:
                    screen.blit(images[str(board[r][c])], (x, y))
            else:
                screen.blit(images["covered"], (x, y))
    pygame.display.flip()

pygame.quit()