import pygame
import chess
 
# Initialize Pygame
pygame.init()
 
# Configure the window size

window_size = (800, 800)
screen = pygame.display.set_mode(window_size)
 
# Create a dictionary to map piece types to corresponding letters
piece_map = {1: 'p', 2: 'n', 3: 'b', 4: 'r', 5: 'q', 6: 'k'}
 
# Load the images of chess pieces
# Make sure you have the images of the pieces in the same folder as your script

piecesw = {piece: pygame.image.load(f"ChessAI/images/w{piece}.png") for piece in piece_map.values()}
piecesb = {piece: pygame.image.load(f"ChessAI/images/b{piece}.png") for piece in piece_map.values()}
 
# Create a chess board

board = chess.Board()
print(board)
# Function to draw the chess board
def draw_board(the_board):
    global screen
    colors = [(233, 236, 239), (125, 135, 150)]
    for i in range(0, 8):
        for j in range(0, 8):
            pygame.draw.rect(screen, colors[((i + j) % 2)], [i * 100, j * 100, 100, 100])
            if the_board.piece_at(chess.square(i, j)):
                piece_name = str(the_board.piece_at(chess.square(i, j)))
                if piece_name.islower():
                    screen.blit(piecesw[piece_name], pygame.Rect(i * 100, j * 100, 100, 100))
                else :
                    screen.blit(piecesb[piece_name.lower()], pygame.Rect(i * 100, j * 100, 100, 100))
 
# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    draw_board(board)
    pygame.display.flip()