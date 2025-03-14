import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 800
ROWs, COLS = 10, 10
CELL_SIZE = WIDTH // COLS
MINE_COUNT = 15

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)

#Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

#Board Generation
board = [[0 for _ in range(COLS)] for _ in range(ROWs)]
mines = set(random.sample(range(ROWs * COLS), MINE_COUNT))

for mine in mines:
    row, col = divmod(mine, COLS)
    board[row][col] = -1

#Game Loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for row in range(ROWs):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GREY, rect, 1)

    pygame.display.flip()

pygame.quit()