
from Chess import ChessMain, ChessEngine
from abc import ABC, abstractmethod


class Board():

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
        self.row = position[0]
        self.col = position[1]
        self.ID = self.row *10 + self.col

    def getRankFile(self):
        return ChessEngine.colsToFiles[self.col] + ChessEngine.rowsToRanks[self.row]

    def changePiece(self, piece):
        self.piece = piece

    def getAllPossibleMoves(self):
        return self.piece.getAllPossibleMoves


class Piece():
    def __init__(self, color):
        self.color = color

    @abstractmethod
    def getAllPossibleMoves(self):
        pass

class EmptyPiece(Piece):
    def __init__(self):
        super().__init__("-")

    def __str__(self):
        return  '--'

    def getAllPossibleMoves(self):
        pass


class PawnPiece(Piece):
    def __init__(self, color):
        super().__init__(color)

    def __str__(self):
        return self.color + 'P'

    def getAllPossibleMoves(self):
        pass


class RookPiece(Piece):
    def __init__(self, color):
        super().__init__(color)

    def __str__(self):
        return self.color + 'R'

    def getAllPossibleMoves(self):
        pass


class KingPiece(Piece):
    def __init__(self, color):
        super().__init__(color)

    def __str__(self):
        return self.color + 'K'

    def getAllPossibleMoves(self):
        pass


class QueenPiece(Piece):
    def __init__(self, color):
        super().__init__(color)

    def __str__(self):
        return self.color + 'Q'

    def getAllPossibleMoves(self):
        pass


class BishopPiece(Piece):
    def __init__(self, color):
        super().__init__(color)

    def __str__(self):
        return self.color + 'B'

    def getAllPossibleMoves(self):
        pass


class KnightPiece(Piece):
    def __init__(self, color):
        super().__init__(color)

    def __str__(self):
        return self.color + 'N'

    def getAllPossibleMoves(self):
        pass

class Move():

    def __init__(self, startSq, endSq):
        self.startSq = startSq
        self.endSq = endSq
        self.pieceMoved = startSq.piece
        self.pieceCaptured = endSq.piece
        # pawn promotion
        self.isPawnPromotion = (str(self.pieceMoved) == 'wP' and self.endSq.position[0] == 0) or \
                               (str(self.pieceMoved) == 'bP' and self.endSq.position[0] == 7)
        self.promotionChoice = 'Q'
        self.moveID = self.startSq.ID * 100 + self.endSq.ID

    '''
    Overriding the equals method
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.startSq.getRankFile() + self.endSq.getRankFile()

'''

'''
class EnPassantMove(Move):
    def __init__(self, startSq, endSq):
        super().__init__(startSq, endSq)
        self.pieceCaptured = PawnPiece('w') if str(self.pieceMoved) == 'bP' else PawnPiece('b')

'''

'''
class CastleMove(Move):
    def __init__(self, startSq, endSq):
        super().__init__(startSq, endSq)

class MoveHandler():

    def __init__(self):
        self.board = Board().board
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.enPassantPossible = ()  # square where an en passant is currently possible
        #self.currentCastlingRights = CastleRights(True, True, True, True)
        #self.castleRightsLog = [
        #    CastleRights(self.currentCastlingRights.whiteKingSide, self.currentCastlingRights.blackKingSide,
        #                 self.currentCastlingRights.whiteQueenSide, self.currentCastlingRights.blackQueenSide)]


    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of col's in given row.
                color = self.board[r][c].piece.color
                if (color == 'w' and self.whiteToMove) or (color == 'b' and not self.whiteToMove):
                    moves.extend(self.board[r][c].getAllPossibleMoves())
        return moves