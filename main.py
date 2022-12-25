import sys
import math
import numpy as np
import pygame

ROW_COUNT = 6
COLUMN_COUNT = 7


#creates an empty matrix using numpy
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


#drops/allots the piece/value at the desired place
def drop_piece(board, row, col, piece):
    board[row][col] = piece


#checks if the location of the piece is empty
def is_valid_location(board, col):
    return board[5][col] == 0


def get_next_open_row(board, col):
    for i in range(ROW_COUNT):
        if board[i][col] == 0:
            return i


#flipping the board because difference in origin
def print_board(board):
    print(np.flip(board, 0))


#checking for every way a player can win
def win(board, piece):
    # check horizontal loc
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True
    # check vert loc
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # check for +ve diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # check for -ve diagonals
    for c in range(COLUMN_COUNT):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True


#drawing board on the gaming window
def draw_board(board):
    for r in range(COLUMN_COUNT):
        for c in range(ROW_COUNT):
            #draw blue rectangle
            pygame.draw.rect(screen, (0, 0, 255), (r*SQUARESIZE, c*SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE), 0)
            #draw black circle where counter isn't placed
            pygame.draw.circle(screen, (0, 0, 0), (r*SQUARESIZE + SQUARESIZE/2, c*SQUARESIZE + SQUARESIZE + SQUARESIZE/2), radius=SQUARESIZE/2 - 5)

    for r in range(COLUMN_COUNT):
        for c in range(ROW_COUNT):
            if board[c][r] == 1:
                #red circle for 1st player
                pygame.draw.circle(screen, (255, 0, 0), (int(r * SQUARESIZE + SQUARESIZE / 2), height - int(c * SQUARESIZE + SQUARESIZE / 2)), radius=SQUARESIZE / 2 - 5)
            elif board[c][r] == 2:
                #yellow circle for 2nd player
                pygame.draw.circle(screen, (255, 255, 0), (int(r * SQUARESIZE + SQUARESIZE / 2), height - int(c * SQUARESIZE + SQUARESIZE / 2)), radius=SQUARESIZE / 2 - 5)
    pygame.display.update()


board = create_board()
game_over = False
turn = 0

# initialising pygame
pygame.init()

SQUARESIZE = 100    #pixels
#dimentions of the game window
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

screen = pygame.display.set_mode((width, height))
draw_board(board)
pygame.display.update()

font = pygame.font.SysFont("monospace", 75)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, SQUARESIZE))
            posx = event.pos[0]

            if turn == 0:
                pygame.draw.circle(screen, (255, 0, 0), (posx, int(SQUARESIZE/2)), SQUARESIZE / 2 - 5)
            else:
                pygame.draw.circle(screen, (255, 255, 0), (posx, int(SQUARESIZE / 2)), SQUARESIZE / 2 - 5)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, SQUARESIZE))
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if win(board, 1):
                        label = font.render("Player 1 wins!", True, (255, 0, 0))
                        screen.blit(label, (40, 10))
                        game_over = True
            else:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if win(board, 2):
                        label = font.render("Player 2 wins!", True, (255, 255, 0))
                        screen.blit(label, (40, 10))
                        game_over = True

            print_board(board)
            draw_board(board)
            #changing turn from 1 to 2 and vice versa
            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(5000)
