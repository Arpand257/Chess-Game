import pygame
import chess
import chess.svg
import sys

pygame.init()
WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2-Player Chess")

# Load piece
pieces_img = {}
pieces = ['p', 'r', 'n', 'b', 'q', 'k']
colors = ['w', 'b']
for color in colors:
    for piece in pieces:
        name = color + piece
        img = pygame.image.load(f"https://raw.githubusercontent.com/niklasf/python-chess/master/docs/static/img/{name}.png")
        img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
        pieces_img[name] = img

# Colors
LIGHT = (240, 217, 181)
DARK = (181, 136, 99)

# Game board
board = chess.Board()

def draw_board():
    for row in range(8):
        for col in range(8):
            color = LIGHT if (row + col) % 2 == 0 else DARK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces():
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row = 7 - (square // 8)
            col = square % 8
            color = 'w' if piece.color == chess.WHITE else 'b'
            name = color + piece.symbol().lower()
            screen.blit(pieces_img[name], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def get_square_under_mouse(pos):
    x, y = pos
    col = x // SQUARE_SIZE
    row = 7 - (y // SQUARE_SIZE)
    return chess.square(col, row)

selected_square = None
running = True

while running:
    draw_board()
    draw_pieces()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            square = get_square_under_mouse(pygame.mouse.get_pos())
            if selected_square is None:
                if board.piece_at(square) and board.piece_at(square).color == board.turn:
                    selected_square = square
            else:
                move = chess.Move(selected_square, square)
                if move in board.legal_moves:
                    board.push(move)
                selected_square = None
