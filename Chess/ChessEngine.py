"""
This class will store all information regarding the current game state and for determining valid chess moves
at the current game state. It will also keep a log of all moves.
"""
from Chess import ChessMain
from abc import ABC, abstractmethod

class GameState():
    def __init__(self):
        self.board =[
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.enPassantPossible = ()  # square where an en passant is currently possible
        self.currentCastlingRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRights.whiteKingSide, self.currentCastlingRights.blackKingSide,
                                             self.currentCastlingRights.whiteQueenSide, self.currentCastlingRights.blackQueenSide)]


    '''
    Takes a move as a parameter and executes it. NOTE: will not work for castling, 
    pawn promotion, and en-pessant. 
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        #  update king's position if needed
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        #  pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + move.promotionChoice

        #  en passant
        if isinstance(move, EnPassantMove):
            self.board[move.startRow][move.endCol] = "--"  # captures the pawn
        #  updating enPassantPossible
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:  # pawn moved 2 squares
            self.enPassantPossible = ((move.startRow + move.endRow)//2, move.endCol)
        else:
            self.enPassantPossible = ()

        # castle Move
        if isinstance(move, CastleMove):
            if move.endCol - move.startCol == 2:  # king side castle move
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]  # moves the rook
                self.board[move.endRow][move.endCol + 1] = '--'
            else:  # Queen side castle move
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]  # moves the rook
                self.board[move.endRow][move.endCol - 2] = '--'  # erase old rook

        # update castling rights --> whenever it is a rook or a king move
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRights.whiteKingSide, self.currentCastlingRights.blackKingSide,
                                                 self.currentCastlingRights.whiteQueenSide, self.currentCastlingRights.blackQueenSide))

    '''
    Undo the last move made
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:  # makes sure there is a move to undo.
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch turns back
            # update king's position if needed
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            # undo en passant
            if isinstance(move, EnPassantMove):
                self.board[move.endRow][move.endCol] = "--"  # landing square blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enPassantPossible = (move.endRow, move.endCol)
            # undo 2 square pawn move
            if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
                self.enPassantPossible = ()
            # undo castling Rights
            self.castleRightsLog.pop()  # get rid of the new castle rights
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRights = CastleRights(newRights.whiteKingSide, newRights.blackKingSide, newRights.whiteQueenSide, newRights.blackQueenSide)
            # undo castle move
            if isinstance(move, CastleMove):
                if move.endCol - move.startCol == 2:  # king Side
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = '--'
                else:  # queen side
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'
    '''
    Update the castle rights given the move 
    '''
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRights.whiteKingSide = False
            self.currentCastlingRights.whiteQueenSide = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRights.blackKingSide = False
            self.currentCastlingRights.blackQueenSide = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:  # left rook
                    self.currentCastlingRights.whiteQueenSide = False
                elif move.startCol == 7:  # right rook
                    self.currentCastlingRights.whiteKingSide = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:  # left rook
                    self.currentCastlingRights.blackQueenSideQueenSide = False
                elif move.startCol == 7:  # right rook
                    self.currentCastlingRights.blackKingSide = False

    '''
    All Moves Considering King is in Check
    '''
    def getValidMoves(self):

        tempEnPassantPossible = self.enPassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRights.whiteKingSide, self.currentCastlingRights.blackKingSide,
                                        self.currentCastlingRights.whiteQueenSide, self.currentCastlingRights.blackQueenSide)

        moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0: #checkmate or stalemate
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        self.enPassantPossible = tempEnPassantPossible
        self.currentCastlingRights = tempCastleRights
        return moves

    '''
    Determine if the current player is in check
    '''
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    '''
    Determine if the enemy can attack the square r, c
    '''
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove #switch to opponent view
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove #switch turns back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: #sqaure is under attack
                return True
        return False



    '''
    All Moves Without Considering The King is in Check
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of col's in given row.
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)  # calls appropriate move function based on piece type.
        return moves

    '''
    Get All Pawn Moves For The Pawn Located At Row, Col And Then Adds To Move List 
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # white pawn moves
            if self.board[r - 1][c] == "--":  # 1 square pawn move
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # 2 square pawn move
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:  # captures to the left
                if self.board[r - 1][c - 1][0] == 'b':  # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r-1,c-1) == self.enPassantPossible:
                    moves.append(EnPassantMove((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:  # captures to the right
                if self.board[r - 1][c + 1][0] == 'b':  # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r-1,c+1) == self.enPassantPossible:
                    moves.append(EnPassantMove((r, c), (r - 1, c + 1), self.board))


        else:  # black pawn moves
            if self.board[r + 1][c] == "--":  # 1 square move
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":  # 2 square move
                    moves.append(Move((r, c), ( r + 2, c), self.board))
            # captures
            if c - 1 >= 0:  # capture to left
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r+1,c-1) == self.enPassantPossible:
                    moves.append(EnPassantMove((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:  # capture to right
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r+1,c+1) == self.enPassantPossible:
                    moves.append(EnPassantMove((r, c), (r + 1, c + 1), self.board))
    '''
    Get All Rook Moves For The Rook Located At Row, Col And Then Adds To Move List
    '''
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # friendly piece invalid
                        break
                else:  # off board
                    break

    '''
       Get All Knight Moves For The Knight Located At Row, Col And Then Adds To Move List
       '''
    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # not an ally piece ( empty or enemy)
                    moves.append(Move((r, c), (endRow, endCol), self.board))


    '''
       Get All Bishop Moves For The Bishop Located At Row, Col And Then Adds To Move List
       '''
    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  #friendly piece valid
                        break
                else:  # off board
                    break

    '''
       Get All Queen Moves For The Queen Located At Row, Col And Then Adds To Move List
       '''
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    '''
       Get All King Moves For The King Located At Row, Col And Then Adds To Move List
       '''
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # not an ally piece ( empty or enemy )
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    '''
    Generate all valid castle moves for the King at (r, c) and add them to the list of moves 
    '''
    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return  # cant castle while in check
        if (self.whiteToMove and self.currentCastlingRights.whiteKingSide) or (not self.whiteToMove and self.currentCastlingRights.blackKingSide):
            self.getKingSideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRights.whiteQueenSide) or (not self.whiteToMove and self.currentCastlingRights.blackQueenSide):
            self.getQueenSideCastleMoves(r, c, moves)

    '''
    Helper for getCastleMoves
    '''
    def getKingSideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(CastleMove((r, c), (r, c+2), self.board))

    '''
    Helper For getCastleMoves
    '''
    def getQueenSideCastleMoves(self, r, c, moves):
        if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3] == '--':
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2):
                moves.append(CastleMove((r, c), (r, c - 2), self.board))


class CastleRights():
    def __init__(self, whiteKingSide, blackKingSide, whiteQueenSide, blackQueenSide):
        self.whiteKingSide = whiteKingSide
        self.blackKingSide = blackKingSide
        self.whiteQueenSide = whiteQueenSide
        self.blackQueenSide = blackQueenSide

class Move():
    ranksToRows = {"1":7, "2":6, "3": 5, "4":4, "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):  # optional paramter, defaults to () unless specified
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        #pawn promotion
        self.isPawnPromotion = (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7)
        self.promotionChoice = 'Q'
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
'''

'''
class EnPassantMove(Move):
    def __init__(self, startSq, endSq, board):
        super().__init__(startSq, endSq, board)
        self.pieceCaptured = 'wP' if self.pieceMoved == 'bP' else 'bP'

'''

'''
class CastleMove(Move):
    def __init__(self, startSq, endSq, board):
        super().__init__(startSq, endSq, board)

class Board():
    rows = cols = ChessMain.dimension
    Squares = []
    for i in range(rows):
        col = []
        for j in range(cols):
            pass
            # col.append()
        Squares.append(col)

    def __init__(self):
        self.board = [
            [Square(RookPiece('b'), self, (0,0)), Square(KnightPiece('b'), self, (0,1)), Square(BishopPiece('b'), self, (0,2)), Square(QueenPiece('b'), self, (0,3)), Square(KingPiece('b'), self, (0,4)), Square(BishopPiece('b'), self, (0,5)), Square(KnightPiece('b'), self, (0,6)), Square(RookPiece('b'), self, (0,7))],
            [Square(PawnPiece('b'), self, (1,0)), Square(PawnPiece('b'), self, (1,1)), Square(PawnPiece('b'), self, (1,2)), Square(PawnPiece('b'), self, (1,3)), Square(PawnPiece('b'), self, (1,4)), Square(PawnPiece('b'), self, (1,5)), Square(PawnPiece('b'), self, (1,6)), Square(PawnPiece('b'), self, (1,7))],
            [Square(EmptyPiece(), self, (2,0)), Square(EmptyPiece(), self, (2,1)), Square(EmptyPiece(), self, (2,2)), Square(EmptyPiece(), self, (2,3)), Square(EmptyPiece(), self, (2,4)), Square(EmptyPiece(), self, (2,5)), Square(EmptyPiece(), self, (2,6)), Square(EmptyPiece(), self, (2,7))],
            [Square(EmptyPiece(), self, (3,0)), Square(EmptyPiece(), self, (3,1)), Square(EmptyPiece(), self, (3,2)), Square(EmptyPiece(), self, (3,3)), Square(EmptyPiece(), self, (3,4)), Square(EmptyPiece(), self, (3,5)), Square(EmptyPiece(), self, (3,6)), Square(EmptyPiece(), self, (3,7))],
            [Square(EmptyPiece(), self, (4,0)), Square(EmptyPiece(), self, (4,1)), Square(EmptyPiece(), self, (4,2)), Square(EmptyPiece(), self, (4,3)), Square(EmptyPiece(), self, (4,4)), Square(EmptyPiece(), self, (4,5)), Square(EmptyPiece(), self, (4,6)), Square(EmptyPiece(), self, (4,7))],
            [Square(EmptyPiece(), self, (5,0)), Square(EmptyPiece(), self, (5,1)), Square(EmptyPiece(), self, (5,2)), Square(EmptyPiece(), self, (5,3)), Square(EmptyPiece(), self, (5,4)), Square(EmptyPiece(), self, (5,5)), Square(EmptyPiece(), self, (5,6)), Square(EmptyPiece(), self, (5,7))],
            [Square(PawnPiece('w'), self, (6,0)), Square(PawnPiece('w'), self, (6,1)), Square(PawnPiece('w'), self, (6,2)), Square(PawnPiece('w'), self, (6,3)), Square(PawnPiece('w'), self, (6,4)), Square(PawnPiece('w'), self, (6,5)), Square(PawnPiece('w'), self, (6,6)), Square(PawnPiece('w'), self, (6,7))],
            [Square(RookPiece('w'), self, (7,0)), Square(KnightPiece('w'), self, (7,1)), Square(BishopPiece('w'), self, (7,2)), Square(QueenPiece('w'), self, (7,3)), Square(KingPiece('w'), self, (7,4)), Square(BishopPiece('w'), self, (7,5)), Square(KnightPiece('w'), self, (7,6)), Square(RookPiece('w'), self, (7,7))]]


class Square():
    def __init__(self, piece, board, position):
        self.piece = piece
        self.board = board
        self.position = position

    def changePiece(self, piece):
        self.piece = piece

    def getAllPossibleMoves(self):
        return self.piece.getAllPossibleMoves()

class Piece():
    def __init__(self, color):
        self.color = color

    @abstractmethod
    def getAllPossibleMoves(self):
        pass

class EmptyPiece(Piece):
    def __init__(self):
        super().__init__("-")
    def getAllPossibleMoves(self):
        pass


class PawnPiece(Piece):
    def __init__(self, color):
        super().__init__(color)

    def getAllPossibleMoves(self):
        pass


class RookPiece(Piece):
    def __init__(self, color):
        super().__init__(color)

    def getAllPossibleMoves(self):
        pass


class KingPiece(Piece):
    def __init__(self, color):
        super().__init__(color)

    def getAllPossibleMoves(self):
        pass


class QueenPiece(Piece):
    def __init__(self, color):
        super().__init__(color)

    def getAllPossibleMoves(self):
        pass


class BishopPiece(Piece):
    def __init__(self, color):
        super().__init__(color)

    def getAllPossibleMoves(self):
        pass


class KnightPiece(Piece):
    def __init__(self, color):
        super().__init__(color)

    def getAllPossibleMoves(self):
        pass

class Move2():
    def __init__(self, startSquare, endSquare):
        self.startSquare
        self.endSquare