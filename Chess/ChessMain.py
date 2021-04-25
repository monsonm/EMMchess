"""
This class will be the main driver class and will handle user input and display of the current game state.
"""

import pygame as p
from Chess import ChessEngine

width = height = 512
dimension: int = 8
sqSize = height // dimension
maxFPS = 15
images = {}

def loadImages():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("EMMbastard/" + piece + ".png"), (sqSize, sqSize))
def main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gameState = ChessEngine.GameState()
    validMoves = gameState.getValidMoves()
    moveMade = False #flag varriable for when a move is made

    loadImages()
    running = True
    sqSelected = () #last click of the user (row, col)
    playerClicks = [] #player clicks ex: [(1,2), (3,4)]
    gameOver = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # Mouse Handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
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
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gameState.makeMove(validMoves[i])
                                moveMade = True
                                print(move.getChessNotation())
                                sqSelected = ()  #reset square for next
                                playerClicks = []  #reset clicks for next
                        if not moveMade:
                            playerClicks = [sqSelected]
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo when keyboard 'z' is pressed
                    gameState.undoMove()
                    moveMade = True
                    gameOver = False
                if e.key == p.K_r:  # reset game when 'r' pressed
                    gameState = ChessEngine.GameState()
                    validMoves = gameState.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    gameOver = False
                    #animate = False    #if we decide to animate later :)

        if moveMade:
            validMoves = gameState.getValidMoves()
            moveMade = False

        drawGameState(screen, gameState, validMoves, sqSelected)

        if gameState.checkMate:
            gameOver = True
            if gameState.whiteToMove:
                drawText(screen, 'Black wins')
            else:
                drawText(screen, 'White wins')
        if gameState.staleMate:
            gameOver = True
            drawText(screen, 'Stalemate')

        clock.tick(maxFPS)
        p.display.flip()

def drawGameState(screen, gameState, validMoves, sqSelected):
    drawBoard(screen)
    drawHighlightedSquares(screen,gameState, validMoves, sqSelected)
    drawPieces(screen, gameState.board)

def drawBoard(screen):
    colors = [p.Color("gray"), p.Color("dark green")]
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

def drawHighlightedSquares(screen, gameState, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gameState.board[r][c][0] == ('w' if gameState.whiteToMove else 'b'): #selected color matches whose turn it is
            #highlight selected
            surface = p.Surface((sqSize, sqSize))
            surface.set_alpha(100)
            surface.fill(p.Color('blue'))
            screen.blit(surface, (c*sqSize,r*sqSize))
            #highlight movable squares
            surface.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(surface, (move.endCol*sqSize, move.endRow*sqSize))

def drawText(screen, s):
    font = p.font.SysFont('Helvetica', 32, True, False)
    textObject = font.render(s, 0, p.Color('orange'))
    textLocation = p.Rect(0,0,width, height).move(width/2 - textObject.get_width()/2, height/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)

if __name__ == "__main__":
    main()