"""
This class will be the main driver class and will handle user input and display of the current game state.
"""

import pygame as p
from Chess import ChessEngine

width = height = 512
dimension = 8
sqSize = height // dimension
maxFPS = 15
images = {}

def loadImages():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        images[piece] = p.transform .scale(p.image.load("EMMbastard/" + piece + ".png"), (sqSize, sqSize))

def main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gameState = ChessEngine.GameState()
    loadImages()
    running = True
    sqSelected = () #last click of the user (row, col)
    playerClicks = [] #player clicks ex: [(1,2), (3,4)]
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//sqSize
                row = location[1]//sqSize
                if sqSelected == (row, col): #clicked same square
                    sqSelected = () #deselect
                    playerClicks = [] #clear clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) #append both clicks
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gameState.board)
                    print(move.getChessNotation())
                    gameState.makeMove(move)
                    sqSelected = () #reset square for next
                    playerClicks = [] #reset clicks for next
        drawGameState(screen, gameState)
        clock.tick(maxFPS)
        p.display.flip()

def drawGameState(screen, gameState):
    drawBoard(screen)
    drawPieces(screen, gameState.board)

def drawBoard(screen):
    colors = [p.Color("light gray"), p.Color("dark green")]
    for r in range(dimension):
        for c in range(dimension):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*sqSize, r*sqSize, sqSize, sqSize))

def drawPieces(screen, board):
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c*sqSize, r*sqSize, sqSize, sqSize))

if __name__ == "__main__":
    main()