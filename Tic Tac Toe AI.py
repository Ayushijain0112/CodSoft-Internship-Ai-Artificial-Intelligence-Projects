import sys
import pygame
import numpy as np

pygame.init()

# Colors
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Proportions & Sizes
WIDTH = 300
HEIGHT = 300
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(BLACK)

board = np.zeros((BOARD_ROWS, BOARD_COLS))

def draw_lines():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, WHITE, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, WHITE, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, WHITE, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), CROSS_WIDTH)
                pygame.draw.line(screen, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), CROSS_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    return True

def check_win(player):
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False

def minimax(board, depth, is_maximizing):
    if check_win(2):
        return 1
    if check_win(1):
        return -1
    if is_board_full():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 2
                    score = minimax(board, depth + 1, False)
                    board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 1
                    score = minimax(board, depth + 1, True)
                    board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

def best_move():
    best_score = -float('inf')
    move = (-1, -1)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return False

def restart_game():
    screen.fill(BLACK)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

draw_lines()

player = 1
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] // SQUARE_SIZE
            mouseY = event.pos[1] // SQUARE_SIZE

            if available_square(mouseY, mouseX):
                mark_square(mouseY, mouseX, player)
                if check_win(player):
                    game_over = True
                player = player % 2 + 1

                if not game_over:
                    if best_move():
                        if check_win(2):
                            game_over = True
                        player = player % 2 + 1

                if not game_over:
                    if is_board_full():
                        game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                player = 1

    if not game_over:
        draw_figures()
    else:
        if check_win(1):
            draw_figures()
            draw_lines()
        elif check_win(2):
            draw_figures()
            draw_lines()
        else:
            draw_figures()
            draw_lines()

    pygame.display.update()
