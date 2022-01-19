import datetime

"""
Store state of game, determine valid moves and move log
"""
class GameState():
    def __init__(self):
        #board is 8X8 2D list
        #pieces are 2 letters - colour (black or white) and piece (Rook, Night, Bishop, Queen, King, pawn)
        #-- is an empty space with no piece
        self.boardOrig = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.setCleanBoard()
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                            'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.moveMade = False
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingAt = (7, 4)
        self.blackKingAt = (0, 4)
        self.maxRows = 7
        self.maxCols = 7
        self.minRow = 0
        self.minCol = 0
        self.isInCheckMate = False
        self.isInStaleMate = False
        self.timeHasExpired = False
        self.isAICalculating = False

        #orthogonal - vertical and horizontal
        #diagonal - 45, 135, 225, 315 degrees
        #self.isInCheck = False
        #self.pins = [] #pieces preventing check
        #self.checks = [] #current checks

        #en passant - two pawns go past each other - one pawn moves in behind the other pawn and captures it
        #pawn promotion - a pawn makes it to the opposing last row. To queen for now
        self.hasPawnPromotion = False
        self.drawnPawnPromotionLeft = 0
        self.drawnPawnPromotionTop = 0
        self.pawnPromotionPieces = []
        self.lastPawnPromotionRow = 0
        self.lastPawnPromotionCol = 0

        #castle - no pieces between the king and castle/rook

        self.isOptionBeginner = False
        #BeginnerTop = 440
        #BeginnerLeft = 630
        self.isOptionIntermediate = False
        self.isOptionIntermediatePlus = False
        #IntermediateTop = 460
        #IntermediateLeft = 630
        self.isOptionAdvanced = False
        #AdvancedTop = 480
        #AdvancedLeft = 630
        self.isOptionAdvancedPlus = False
        self.isOptionNone = True
        #NoneTop = 440
        #NoneLeft = 800
        self.isAIEnabled = False
        self.isAIColorWhite = False
        self.whiteSeconds = 0
        self.blackSeconds = 0
        self.startTime = datetime.datetime.now()
        self.whiteLastMove = None
        self.blackLastMove = None
        self.whiteEnPassant = 3
        self.blackEnPassant = 4
        self.whiteKingHasMoved = False
        self.whiteLeftRookHasMoved = False
        self.whiteRightRookHasMoved = False
        self.blackKingHasMoved = False
        self.blackLeftRookHasMoved = False
        self.blackRightRookHasMoved = False

        self.wP = 0
        self.wN = 0
        self.wB = 0
        self.wR = 0
        self.wQ = 0
        self.bP = 0
        self.bN = 0
        self.bB = 0
        self.bR = 0
        self.bQ = 0
        self.countedPieces = {'wK': 0, 'wQ': 0, 'wR': 0, 'wB': 0, 'wN': 0, 'wp': 0, 'bK': 0, 'bQ': 0, 'bR': 0, 'bB': 0, 'bN': 0, 'bp': 0}

    def setTime(self):
        self.startTime = datetime.datetime.now()

    def getTimes(self):
        endTime = datetime.datetime.now()
        delta = endTime - self.startTime

        # if self.isAICalculating:
        #     delta = endTime

        if self.moveMade:
            print("Move made. Seconds: " + str(delta.total_seconds()) + " Start:" + str(self.startTime) + " End:" + str(endTime) + " White:"+str(self.whiteToMove))
            self.moveMade = False

        #now = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        #datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        if self.whiteToMove:
            self.whiteSeconds += delta.total_seconds()
            #added_seconds = datetime.timedelta(0, self.blackSeconds)
        else:
            self.blackSeconds += delta.total_seconds()
            #added_seconds = datetime.timedelta(0, self.whiteSeconds)

        # now = datetime.datetime(2010, 1, 1, 0,5)
        # new_datetime = now - added_seconds
        # print("Now: " + str(new_datetime) + " More:" + new_datetime.strftime("%M:%S"))

        self.setTime()

    def getTimesToDisplay(self, displayWhite, maxMinutesPlay):

        # if not (displayWhite and self.isAIEnabled and self.isAIColorWhite) \
        #     and not (not displayWhite and self.isAIEnabled and not self.isAIColorWhite):
        self.getTimes()

        now = datetime.datetime(2010, 1, 1, 0, maxMinutesPlay)

        #added_seconds = datetime.timedelta(0, 0)

        if displayWhite:
            added_seconds = datetime.timedelta(0, self.whiteSeconds)
            #if self.isAIEnabled and self.isAIColorWhite:
            #    added_seconds = datetime.timedelta(0, 0)
        else:
            added_seconds = datetime.timedelta(0, self.blackSeconds)
            #if self.isAIEnabled and not self.isAIColorWhite:
            #    added_seconds = datetime.timedelta(0, 0)


        new_datetime = now - added_seconds

        #AI's clock should not tick
        #if displayWhite and self.isAIEnabled and self.isAIColorWhite:
        #    new_datetime = now
        #elif not displayWhite and self.isAIEnabled and not self.isAIColorWhite:
        #    new_datetime = now

        minute = new_datetime.minute

        if not self.timeHasExpired:
            self.timeHasExpired = minute > maxMinutesPlay

        return new_datetime.strftime("%M:%S")

    def isGameOver(self):
        return self.isInStaleMate or self.isInCheckMate or self.timeHasExpired

    def setCleanBoard(self):
        #self.board = []
        #self.board = self.boardOrig
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

    def getRanksToRows(self):
        move = Move((0,0), (1,1), self.board)
        return move.ranksToRows

    def getRowsToRanks(self):
        move = Move((0,0), (1,1), self.board)
        return move.rowsToRanks

    def getColsToFiles(self):
        move = Move((0,0), (1,1), self.board)
        return move.colsToFiles

    '''
    Takes a move as a parameter (not castling and en-passant
    '''
    def makeMove(self, move):
        if move != None:
            self.board[move.startRow][move.startCol] = ""
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move) #log move for later

            if move.isUserClicked: # and lastMove != None:
                if self.whiteToMove:
                    lastMove = self.blackLastMove  # evaluate opponents last move
                    moveRow = +1
                    pawnPiece = 'bp'  # evaluate opponents last move
                    kingPiece = 'wK'
                    rookPiece = 'wR'
                else:
                    lastMove = self.whiteLastMove  # evaluate opponents last move
                    moveRow = -1
                    pawnPiece = 'wp'  # evaluate opponents last move
                    kingPiece = 'bK'
                    rookPiece = 'bR'

                #EnPassant
                if lastMove != None and move.pieceMoved[1] == pawnPiece[1] and move.endCol == lastMove.endCol and move.endRow + moveRow == lastMove.endRow:
                    self.board[lastMove.endRow][lastMove.endCol] = ""

                #castling
                #if self.whiteToMove:
                colMoved = 2
                kingHasMoved = self.whiteKingHasMoved if self.whiteToMove else self.blackKingHasMoved
                if move.endCol < move.startCol:
                    rookCol = 0
                    rookColMove = move.endCol+1
                    rookHasMoved = self.whiteLeftRookHasMoved if self.whiteToMove else self.blackLeftRookHasMoved
                else:
                    rookCol = 7
                    rookColMove = move.endCol-1
                    rookHasMoved = self.whiteRightRookHasMoved if self.whiteToMove else self.blackRightRookHasMoved

                if move.pieceMoved == kingPiece and move.startRow == move.endRow and abs(move.startCol - move.endCol) == colMoved \
                    and self.board[move.startRow][rookCol] == rookPiece \
                    and not kingHasMoved and not rookHasMoved:
                        if self.whiteToMove:
                            self.whiteKingHasMoved = True
                            if rookCol == 0:
                                self.whiteLeftRookHasMoved = True
                            else:
                                self.whiteRightRookHasMoved = True
                        else:
                            self.blackKingHasMoved = True
                            if rookCol == 0:
                                self.blackLeftRookHasMoved = True
                            else:
                                self.blackRightRookHasMoved = True
                        self.board[move.startRow][rookCol] = ""
                        self.board[move.startRow][rookColMove] = rookPiece

            self.swapPlayers() #self.whiteToMove = not self.whiteToMove #switch turns

            #keep track of Kings
            if move.isUserClicked:
                if move.pieceMoved == 'wK':
                    self.whiteKingAt = (move.endRow, move.endCol)
                    self.whiteKingHasMoved = True
                elif move.pieceMoved == 'bK':
                    self.blackKingAt = (move.endRow, move.endCol)
                    self.blackKingHasMoved = True

                if move.pieceMoved == 'wR':
                    if move.startRow == 7 and move.startCol == 0 and not self.whiteLeftRookHasMoved:
                        self.whiteLeftRookHasMoved = True
                    elif move.startRow == 7 and move.startCol == 7 and not self.whiteRightRookHasMoved:
                        self.whiteRightRookHasMoved = True
                elif move.pieceMoved == 'bR':
                    if move.startRow == 0 and move.startCol == 0 and not self.blackLeftRookHasMoved:
                        self.blackLeftRookHasMoved = True
                    elif move.startRow == 0 and move.startCol == 7 and not self.blackRightRookHasMoved:
                        self.blackRightRookHasMoved = True
            else:
                # keep track of Kings
                if move.pieceMoved == 'wK':
                    self.whiteKingAt = (move.endRow, move.endCol)
                elif move.pieceMoved == 'bK':
                    self.blackKingAt = (move.endRow, move.endCol)

            #pawn promotion to Q
            if move.isPawnPromotion and move.isUserClicked:
                self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'
                self.hasPawnPromotion = move.isPawnPromotion
                self.lastPawnPromotionRow = move.endRow
                self.lastPawnPromotionCol = move.endCol


            #(self.blackKingAt[0], self.blackKingAt[1])

    '''
    Undo the last move
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.swapPlayers() #self.whiteToMove = not self.whiteToMove #switch turns

        #keep track of Kings
        if move.pieceMoved == 'wK':
            self.whiteKingAt = (move.startRow, move.startCol)
        elif move.pieceMoved == 'bK':
            self.blackKingAt = (move.startRow, move.startCol)

        #enpassant
        #2 sqr pawn advance
        #castling

        self.isInCheckMate = False;
        self.isInStaleMate = False;

    '''
    All moves consider checks
    '''
    def getValidMoves(self):
        #all posible moves
        moves = self.getAllPossibleMoves()
        #make each move
        for i in range(len(moves)-1,-1,-1): #backwards
            self.makeMove(moves[i])
            #all possible moves - opponent
            #do opponent moves attack king
            # if attack king - not valid
            self.swapPlayers()
            if self.isInCheck():
                moves.remove(moves[i])
            self.swapPlayers()
            self.undoMove()

        if len(moves) == 0:
            if self.isInCheck():
                self.isInCheckMate = True
            else:
                self.isInStaleMate = True
        else:
            self.isInCheckMate = False
            self.isInStaleMate = False

        return moves

    '''
    Check if a king position is under attack
    '''
    def isInCheck(self):
        if self.whiteToMove:
            return self.isSquareUnderAttack(self.whiteKingAt[0], self.whiteKingAt[1])
        else:
            return self.isSquareUnderAttack(self.blackKingAt[0], self.blackKingAt[1])

    '''
    Check if the specific square is under attack
    '''
    def isSquareUnderAttack(self, row, col):
        self.swapPlayers()  #self.whiteToMove = not self.whiteToMove
        opponentMoves = self.getAllPossibleMoves()
        self.swapPlayers() #self.whiteToMove = not self.whiteToMove

        for move in opponentMoves:
            if move.endRow == row and move.endCol == col:
                return True

        return False

    def swapPlayers(self):
        # endTime = datetime.datetime.now()
        # delta = self.startTime - endTime
        # print("Seconds: " + str(delta.seconds))
        # self.setTime()

        self.whiteToMove = not self.whiteToMove

    def storeLastMove(self,move):
        if self.whiteToMove:
            self.blackLastMove = move
        else:
            self.whiteLastMove = move

    '''
    All moves not considering checks
    '''
    def getAllPossibleMoves(self):
        #pass
        moves = [] #[Move((6,4),(4,4), self.board)]
        for row in range(len(self.board)): #number of rows
            for col in range(len(self.board[row])): #number of cols in row
                if self.board[row][col] != "":
                    turn = self.board[row][col][0]
                    if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                        piece = self.board[row][col][1]
                        self.moveFunctions[piece](row, col, moves)
                        #if piece == 'p':
                        #    self.getPawnMoves(row, col, moves)
                        #elif piece == 'R':
                        #    self.getRookMoves(row, col, moves)
        return moves

    '''
    Get all pawn moves for pawn located at row,col
    '''
    def getPawnMoves(self, row, col, moves):
        if self.whiteToMove:
            #move up
            if row-1 >= self.minRow and (self.board[row-1][col] == "--" or self.board[row-1][col] == ""):
                moves.append(Move((row,col), (row-1,col), self.board)) #1 square advance
                if row == 6 and (self.board[row-2][col] == "--" or self.board[row-2][col] == ""):
                    moves.append(Move((row, col), (row - 2, col), self.board))  # 2 square advance
            if col-1 >= self.minCol and row-1 >= self.minRow:
                if self.board[row-1][col-1] != '--' and self.board[row-1][col-1] != '' and self.board[row-1][col-1][0] == 'b': #black piece to capture
                    moves.append(Move((row,col),(row-1,col-1),self.board))
            if col+1 <= self.maxCols and row-1 >= self.minRow:
                if self.board[row-1][col+1] != '--' and self.board[row-1][col+1] != '' and self.board[row-1][col+1][0] == 'b': #black piece to capture
                    moves.append(Move((row,col),(row-1,col+1),self.board))

            #EnPassant
            if row-1 >= self.minRow and row == self.whiteEnPassant:
                if self.whiteToMove:
                    lastMove = self.blackLastMove
                else:
                    lastMove = self.whiteLastMove
                #lastMove = self.moveLog[len(self.moveLog)-1]
                if lastMove != None and lastMove.pieceMoved == 'bp' and row == lastMove.endRow \
                        and abs(lastMove.startRow - lastMove.endRow) == 2 \
                        and (col == lastMove.endCol-1 or col == lastMove.endCol+1):
                    moves.append(Move((row, col), (row - 1, lastMove.endCol), self.board))
                    #print("Moves:" + str(len(self.moveLog)))
                    #print("Last move startRow:" + str(lastMove.startRow) + " startCol:" + str(lastMove.startCol) + " endRow:" + str(lastMove.endRow) + " endCol:" + str(lastMove.endCol))

        else: #black pawns
            #move down
            if row+1 <= self.maxRows and (self.board[row+1][col] == "--" or self.board[row+1][col] == ""):
                moves.append(Move((row,col), (row+1,col), self.board)) #1 square advance
                if row == 1 and self.board[row+2][col] == "--":
                    moves.append(Move((row, col), (row + 2, col), self.board))  # 2 square advance
            if col-1 >= self.minCol and row+1 <= self.maxRows:
                if self.board[row+1][col-1] != '--' and self.board[row+1][col-1] != '' and self.board[row+1][col-1][0] == 'w': #white piece to capture
                    moves.append(Move((row,col),(row+1,col-1),self.board))
            if col+1 <= self.maxCols and row+1 <= self.maxRows:
                if self.board[row+1][col+1] != '--' and self.board[row+1][col+1] != '' and self.board[row+1][col+1][0] == 'w': #white piece to capture
                    moves.append(Move((row,col),(row+1,col+1),self.board))

            #EnPassant
            if row-1 >= self.minRow and row == self.blackEnPassant:
                if self.whiteToMove:
                    lastMove = self.blackLastMove
                else:
                    lastMove = self.whiteLastMove
                #lastMove = self.moveLog[len(self.moveLog)-1]
                if lastMove != None and lastMove.pieceMoved == 'wp' and row == lastMove.endRow \
                        and abs(lastMove.startRow - lastMove.endRow) == 2 \
                        and (col == lastMove.endCol-1 or col == lastMove.endCol+1):
                    moves.append(Move((row, col), (row + 1, lastMove.endCol), self.board))
                    #print("Moves:" + str(len(self.moveLog)))
                    #print("Last move startRow:" + str(lastMove.startRow) + " startCol:" + str(lastMove.startCol) + " endRow:" + str(lastMove.endRow) + " endCol:" + str(lastMove.endCol))

        #pawn promotions

    #rook
    #knight
    #bishop

    '''
    Get all rook moves for rook located at row,col
    '''
    def getRookMoves(self, row, col, moves):
        colorPieceOpponent = ''
        if self.whiteToMove:
            colorPieceOpponent = 'b'
            # if col-1 >= 0:
            #     if self.board[row-1][col-1] != '' and self.board[row-1][col-1][0] == 'b': #black piece to capture
            #         moves.append(Move((row,col),(row-1,col-1),self.board))
            # if col+1 <= 7:
            #     if self.board[row-1][col+1] != '' and self.board[row-1][col+1][0] == 'b': #black piece to capture
            #         moves.append(Move((row,col),(row-1,col+1),self.board))

        else:  # black pawns
            colorPieceOpponent = 'w'
            # move down
            # if self.board[row+1][col] == "--":
            #     moves.append(Move((row,col), (row+1,col), self.board)) #1 square advance
            #     if row == 1 and self.board[row+2][col] == "--":
            #         moves.append(Move((row, col), (row + 2, col), self.board))  # 2 square advance
            # if col-1 >= 0:
            #     if self.board[row+1][col-1] != '' and self.board[row+1][col-1][0] == 'w': #white piece to capture
            #         moves.append(Move((row,col),(row+1,col-1),self.board))
            # if col+1 <= 7:
            #     if self.board[row+1][col+1] != '' and self.board[row+1][col+1][0] == 'w': #white piece to capture
            #         moves.append(Move((row,col),(row+1,col+1),self.board))

        #move up
        move1 = row-1 >= 0 and (self.board[row-1][col] == "--" or self.board[row-1][col] == '' or self.board[row-1][col][0] == colorPieceOpponent)
        hasOpponent1 = row-1 >= 0 and self.board[row-1][col] != "--" and self.board[row-1][col] != '' and self.board[row-1][col][0] == colorPieceOpponent
        move2 = row-2 >= 0 and (self.board[row-2][col] == "--" or self.board[row-2][col] == '' or self.board[row-2][col][0] == colorPieceOpponent)
        hasOpponent2 = row-2 >= 0 and self.board[row-2][col] != "--" and self.board[row-2][col] != '' and self.board[row-2][col][0] == colorPieceOpponent
        move3 = row-3 >= 0 and (self.board[row-3][col] == "--" or self.board[row-3][col] == '' or self.board[row-3][col][0] == colorPieceOpponent)
        hasOpponent3 = row-3 >= 0 and self.board[row-3][col] != "--" and self.board[row-3][col] != '' and self.board[row-3][col][0] == colorPieceOpponent
        move4 = row-4 >= 0 and (self.board[row-4][col] == "--" or self.board[row-4][col] == '' or self.board[row-4][col][0] == colorPieceOpponent)
        hasOpponent4 = row-4 >= 0 and self.board[row-4][col] != "--" and self.board[row-4][col] != '' and self.board[row-4][col][0] == colorPieceOpponent
        move5 = row-5 >= 0 and (self.board[row-5][col] == "--" or self.board[row-5][col] == '' or self.board[row-5][col][0] == colorPieceOpponent)
        hasOpponent5 = row-5 >= 0 and self.board[row-5][col] != "--" and self.board[row-5][col] != '' and self.board[row-5][col][0] == colorPieceOpponent
        move6 = row-6 >= 0 and (self.board[row-6][col] == "--" or self.board[row-6][col] == '' or self.board[row-6][col][0] == colorPieceOpponent)
        hasOpponent6 = row-6 >= 0 and self.board[row-6][col] != "--" and self.board[row-6][col] != '' and self.board[row-6][col][0] == colorPieceOpponent
        move7 = row-7 >= 0 and (self.board[row-7][col] == "--" or self.board[row-7][col] == '' or self.board[row-7][col][0] == colorPieceOpponent)
        #hasOpponent7 = self.board[row-7][col] != "--" and self.board[row-7][col] != '' and self.board[row-7][col][0] == colorPieceOpponent

        #move8 = row-8 >= 0 and (self.board[row-8][col] == "--" or self.board[row-8][col] == '' or self.board[row-8][col][0] == 'b')

        if move1:
            moves.append(Move((row,col), (row-1,col), self.board)) #1 square advance
        if move1 and not hasOpponent1 and move2:
            moves.append(Move((row,col), (row-2,col), self.board)) #2 square advance
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3:
            moves.append(Move((row,col), (row-3,col), self.board)) #3 square advance
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4:
            moves.append(Move((row,col), (row-4,col), self.board)) #4 square advance
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4 and not hasOpponent4 and move5:
            moves.append(Move((row,col), (row-5,col), self.board)) #5 square advance
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4 and not hasOpponent4 and move5 and not hasOpponent5 and move6:
            moves.append(Move((row,col), (row-6,col), self.board)) #6 square advance
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4 and not hasOpponent4 and move5 and not hasOpponent5 and move6 and not hasOpponent6 and move7:
            moves.append(Move((row,col), (row-7,col), self.board)); #7 square advance
        #if move1 and move2 and move3 and move4 and move5 and move6 and move7 and move8:
        #    moves.append(Move((row,col), (row-8,col), self.board)) #8 square advance

        #move down
        move1 = row+1 <= 7 and (self.board[row+1][col] == "--" or self.board[row+1][col] == '' or self.board[row+1][col][0] == colorPieceOpponent)
        hasOpponent1 = row+1 <= 7 and (self.board[row+1][col] != "--" and self.board[row+1][col] != '' and self.board[row+1][col][0] == colorPieceOpponent);
        move2 = row+2 <= 7 and (self.board[row+2][col] == "--" or self.board[row+2][col] == '' or self.board[row+2][col][0] == colorPieceOpponent)
        hasOpponent2 = row+2 <= 7 and self.board[row+2][col] != "--" and self.board[row+2][col] != '' and self.board[row+2][col][0] == colorPieceOpponent
        move3 = row+3 <= 7 and (self.board[row+3][col] == "--" or self.board[row+3][col] == '' or self.board[row+3][col][0] == colorPieceOpponent)
        hasOpponent3 = row+3 <= 7 and self.board[row+3][col] != "--" and self.board[row+3][col] != '' and self.board[row+3][col][0] == colorPieceOpponent
        move4 = row+4 <= 7 and (self.board[row+4][col] == "--" or self.board[row+4][col] == '' or self.board[row+4][col][0] == colorPieceOpponent)
        hasOpponent4 = row+4 <= 7 and self.board[row+4][col] != "--" and self.board[row+4][col] != '' and self.board[row+4][col][0] == colorPieceOpponent
        move5 = row+5 <= 7 and (self.board[row+5][col] == "--" or self.board[row+5][col] == '' or self.board[row+5][col][0] == colorPieceOpponent)
        hasOpponent5 = row+5 <= 7 and self.board[row+5][col] != "--" and self.board[row+5][col] != '' and self.board[row+5][col][0] == colorPieceOpponent
        move6 = row+6 <= 7 and (self.board[row+6][col] == "--" or self.board[row+6][col] == '' or self.board[row+6][col][0] == colorPieceOpponent)
        hasOpponent6 = row+6 <= 7 and self.board[row+6][col] != "--" and self.board[row+6][col] != '' and self.board[row+6][col][0] == colorPieceOpponent
        move7 = row+7 <= 7 and (self.board[row+7][col] == "--" or self.board[row+7][col] == '' or self.board[row+7][col][0] == colorPieceOpponent)
        ##hasOpponent7 = self.board[row+7][col] != "--" and self.board[row+7][col] != '' and self.board[row+7][col][0] == colorPieceOpponent

        if move1:
            moves.append(Move((row,col), (row+1,col), self.board)) #1 square advance
        if move1 and not hasOpponent1 and move2:
            moves.append(Move((row,col), (row+2,col), self.board)) #2 square advance
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3:
            moves.append(Move((row,col), (row+3,col), self.board)) #3 square advance
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4:
            moves.append(Move((row,col), (row+4,col), self.board)) #4 square advance
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4 and not hasOpponent4 and move5:
            moves.append(Move((row,col), (row+5,col), self.board)) #5 square advance
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4 and not hasOpponent4 and move5 and not hasOpponent5 and move6:
            moves.append(Move((row,col), (row+6,col), self.board)) #6 square advance
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4 and not hasOpponent4 and move5 and not hasOpponent5 and move6 and not hasOpponent6 and move7:
            moves.append(Move((row,col), (row+7,col), self.board)) #7 square advance
        #if move1 and move2 and move3 and move4 and move5 and move6 and move7 and move8:
        #    moves.append(Move((row,col), (row-8,col), self.board)) #8 square advance

        #move left
        move1 = col-1 >= 0 and (self.board[row][col-1] == "--" or self.board[row][col-1] == '' or self.board[row][col-1][0] == colorPieceOpponent)
        hasOpponent1 = col-1 >= 0 and self.board[row][col-1] != "--" and self.board[row][col-1] != '' and self.board[row][col-1][0] == colorPieceOpponent
        move2 = col-2 >= 0 and (self.board[row][col-2] == "--" or self.board[row][col-2] == '' or self.board[row][col-2][0] == colorPieceOpponent)
        hasOpponent2 = col-2 >= 0 and self.board[row][col-2] != "--" and self.board[row][col-2] != '' and self.board[row][col-2][0] == colorPieceOpponent
        move3 = col-3 >= 0 and (self.board[row][col-3] == "--" or self.board[row][col-3] == '' or self.board[row][col-3][0] == colorPieceOpponent)
        hasOpponent3 = col-3 >= 0 and self.board[row][col-3] != "--" and self.board[row][col-3] != '' and self.board[row][col-3][0] == colorPieceOpponent
        move4 = col-4 >= 0 and (self.board[row][col-4] == "--" or self.board[row][col-4] == '' or self.board[row][col-4][0] == colorPieceOpponent)
        hasOpponent4 = col-1 >= 0 and self.board[row][col-4] != "--" and self.board[row][col-4] != '' and self.board[row][col-4][0] == colorPieceOpponent
        move5 = col-5 >= 0 and (self.board[row][col-5] == "--" or self.board[row][col-5] == '' or self.board[row][col-5][0] == colorPieceOpponent)
        hasOpponent5 = col-5 >= 0 and self.board[row][col-5] != "--" and self.board[row][col-5] != '' and self.board[row][col-5][0] == colorPieceOpponent
        move6 = col-6 >= 0 and (self.board[row][col-6] == "--" or self.board[row][col-6] == '' or self.board[row][col-6][0] == colorPieceOpponent)
        hasOpponent6 = col-6 >= 0 and self.board[row][col-6] != "--" and self.board[row][col-6] != '' and self.board[row][col-6][0] == colorPieceOpponent
        move7 = col-7 >= 0 and (self.board[row][col-7] == "--" or self.board[row][col-7] == '' or self.board[row][col-7][0] == colorPieceOpponent)
        #hasOpponent7 = self.board[row][col-7] != "--" and self.board[row][col-7] != '' and self.board[row][col-7][0] == colorPieceOpponent

        if move1:
            moves.append(Move((row,col), (row,col-1), self.board)) #1 square advance
        if move1 and not hasOpponent1 and move2:
            moves.append(Move((row,col), (row,col-2), self.board)) #2 square advance
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3:
            moves.append(Move((row,col), (row,col-3), self.board)) #3 square advance
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4:
            moves.append(Move((row,col), (row,col-4), self.board)) #4 square advance
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4 and not hasOpponent4 and move5:
            moves.append(Move((row,col), (row,col-5), self.board)) #5 square advance
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4 and not hasOpponent4 and move5 and not hasOpponent5 and move6:
            moves.append(Move((row,col), (row,col-6), self.board)) #6 square advance
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4 and not hasOpponent4 and move5 and not hasOpponent5 and move6 and not hasOpponent6 and move7:
            moves.append(Move((row,col), (row,col-7), self.board)) #7 square advance
        #if move1 and move2 and move3 and move4 and move5 and move6 and move7 and move8:
        #    moves.append(Move((row,col), (row,col-8), self.board)) #8 square advance

        #move right
        move1 = col+1 <= 7 and (self.board[row][col+1] == "--" or self.board[row][col+1] == '' or self.board[row][col+1][0] == colorPieceOpponent)
        hasOpponent1 = col+1 <= 7 and self.board[row][col+1] != "--" and self.board[row][col+1] != '' and self.board[row][col+1][0] == colorPieceOpponent
        move2 = col+2 <= 7 and (self.board[row][col+2] == "--" or self.board[row][col+2] == '' or self.board[row][col+2][0] == colorPieceOpponent)
        hasOpponent2 = col+2 <= 7 and self.board[row][col+2] != "--" and self.board[row][col+2] != '' and self.board[row][col+2][0] == colorPieceOpponent
        move3 = col+3 <= 7 and (self.board[row][col+3] == "--" or self.board[row][col+3] == '' or self.board[row][col+3][0] == colorPieceOpponent)
        hasOpponent3 = col+3 <= 7 and self.board[row][col+3] != "--" and self.board[row][col+3] != '' and self.board[row][col+3][0] == colorPieceOpponent
        move4 = col+4 <= 7 and (self.board[row][col+4] == "--" or self.board[row][col+4] == '' or self.board[row][col+4][0] == colorPieceOpponent)
        hasOpponent4 = col+4 <= 7 and self.board[row][col+4] != "--" and self.board[row][col+4] != '' and self.board[row][col+4][0] == colorPieceOpponent
        move5 = col+5 <= 7 and (self.board[row][col+5] == "--" or self.board[row][col+5] == '' or self.board[row][col+5][0] == colorPieceOpponent)
        hasOpponent5 = col+5 <= 7 and self.board[row][col+5] != "--" and self.board[row][col+5] != '' and self.board[row][col+5][0] == colorPieceOpponent
        move6 = col+6 <= 7 and (self.board[row][col+6] == "--" or self.board[row][col+6] == '' or self.board[row][col+6][0] == colorPieceOpponent)
        hasOpponent6 = col+6 <= 7 and self.board[row][col+6] != "--" and self.board[row][col+6] != '' and self.board[row][col+6][0] == colorPieceOpponent
        move7 = col+7 <= 7 and (self.board[row][col+7] == "--" or self.board[row][col+7] == '' or self.board[row][col+7][0] == colorPieceOpponent)
        hasOpponent7 = col+7 <= 7 and self.board[row][col+7] != "--" and self.board[row][col+7] != '' and self.board[row][col+7][0] == colorPieceOpponent


        if move1:
            moves.append(Move((row,col), (row,col+1), self.board)) #1 square advance
        if move1 and not hasOpponent1 and move2:
            moves.append(Move((row,col), (row,col+2), self.board)) #2 square advance
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3:
            moves.append(Move((row,col), (row,col+3), self.board)) #3 square advance
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4:
            moves.append(Move((row,col), (row,col+4), self.board)) #4 square advance
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4 and not hasOpponent4 and move5:
            moves.append(Move((row,col), (row,col+5), self.board)) #5 square advance
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4 and not hasOpponent4 and move5 and not hasOpponent5 and move6:
            moves.append(Move((row,col), (row,col+6), self.board)) #6 square advance
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4 and not hasOpponent4 and move5 and not hasOpponent5 and move6 and not hasOpponent6 and move7:
            moves.append(Move((row,col), (row,col+7), self.board)) #7 square advance

    '''
    Get all knight moves for knight located at row,col
    '''
    def getKnightMoves(self, row, col, moves):
        colorPieceOpponent = ''
        if self.whiteToMove:
            colorPieceOpponent = 'b'
            # if col-1 >= 0:
            #     if self.board[row-1][col-1] != '' and self.board[row-1][col-1][0] == 'b': #black piece to capture
            #         moves.append(Move((row,col),(row-1,col-1),self.board))
            # if col+1 <= 7:
            #     if self.board[row-1][col+1] != '' and self.board[row-1][col+1][0] == 'b': #black piece to capture
            #         moves.append(Move((row,col),(row-1,col+1),self.board))

        else:  # black pawns
            colorPieceOpponent = 'w'
            # move down
            # if self.board[row+1][col] == "--":
            #     moves.append(Move((row,col), (row+1,col), self.board)) #1 square advance
            #     if row == 1 and self.board[row+2][col] == "--":
            #         moves.append(Move((row, col), (row + 2, col), self.board))  # 2 square advance
            # if col-1 >= 0:
            #     if self.board[row+1][col-1] != '' and self.board[row+1][col-1][0] == 'w': #white piece to capture
            #         moves.append(Move((row,col),(row+1,col-1),self.board))
            # if col+1 <= 7:
            #     if self.board[row+1][col+1] != '' and self.board[row+1][col+1][0] == 'w': #white piece to capture
            #         moves.append(Move((row,col),(row+1,col+1),self.board))

        #move up L
        move = row-2 >= 0 and col-1 >= 0 and (self.board[row-2][col-1] == "--" or self.board[row-2][col-1] == '' or self.board[row-2][col-1][0] == colorPieceOpponent)
        if move:
            moves.append(Move((row,col), (row-2,col-1), self.board))

        #move up R
        move = row-2 >= 0 and col+1 <= 7 and (self.board[row-2][col+1] == "--" or self.board[row-2][col+1] == '' or self.board[row-2][col+1][0] == colorPieceOpponent)
        if move:
            moves.append(Move((row,col), (row-2,col+1), self.board))

        #move down L
        move = row+2 <= 7 and col-1 >= 0 and (self.board[row+2][col-1] == "--" or self.board[row+2][col-1] == '' or self.board[row+2][col-1][0] == colorPieceOpponent)
        if move:
            moves.append(Move((row,col), (row+2,col-1), self.board))

        #move down R
        move = row+2 <= 7 and col+1 <= 7 and (self.board[row+2][col+1] == "--" or self.board[row+2][col+1] == '' or self.board[row+2][col+1][0] == colorPieceOpponent)
        if move:
            moves.append(Move((row,col), (row+2,col+1), self.board))

        #move left Up
        move = row-1 >= 0 and col-2 >= 0 and (self.board[row-1][col-2] == "--" or self.board[row-1][col-2] == '' or self.board[row-1][col-2][0] == colorPieceOpponent)
        if move:
            moves.append(Move((row,col), (row-1,col-2), self.board))

        #move left Down
        move = row+1 <= 7 and col-2 >= 0 and (self.board[row+1][col-2] == "--" or self.board[row+1][col-2] == '' or self.board[row+1][col-2][0] == colorPieceOpponent)
        if move:
            moves.append(Move((row,col), (row+1,col-2), self.board))

        #move right Up
        move = row-1 >= 0 and col+2 <= 7 and (self.board[row-1][col+2] == "--" or self.board[row-1][col+2] == '' or self.board[row-1][col+2][0] == colorPieceOpponent)
        if move:
            moves.append(Move((row,col), (row-1,col+2), self.board))

        #move right Down
        move = row+1 <= 7 and col+2 <= 7 and (self.board[row+1][col+2] == "--" or self.board[row+1][col+2] == '' or self.board[row+1][col+2][0] == colorPieceOpponent)
        if move:
            moves.append(Move((row,col), (row+1,col+2), self.board))

    '''
    Get all bishop moves for bishop located at row,col
    '''
    def getBishopMoves(self, row, col, moves):
        colorPieceOpponent = ''
        if self.whiteToMove:
            colorPieceOpponent = 'b'
            # if col-1 >= 0:
            #     if self.board[row-1][col-1] != '' and self.board[row-1][col-1][0] == 'b': #black piece to capture
            #         moves.append(Move((row,col),(row-1,col-1),self.board))
            # if col+1 <= 7:
            #     if self.board[row-1][col+1] != '' and self.board[row-1][col+1][0] == 'b': #black piece to capture
            #         moves.append(Move((row,col),(row-1,col+1),self.board))

        else:  # black pawns
            colorPieceOpponent = 'w'
            # move down
            # if self.board[row+1][col] == "--":
            #     moves.append(Move((row,col), (row+1,col), self.board)) #1 square advance
            #     if row == 1 and self.board[row+2][col] == "--":
            #         moves.append(Move((row, col), (row + 2, col), self.board))  # 2 square advance
            # if col-1 >= 0:
            #     if self.board[row+1][col-1] != '' and self.board[row+1][col-1][0] == 'w': #white piece to capture
            #         moves.append(Move((row,col),(row+1,col-1),self.board))
            # if col+1 <= 7:
            #     if self.board[row+1][col+1] != '' and self.board[row+1][col+1][0] == 'w': #white piece to capture
            #         moves.append(Move((row,col),(row+1,col+1),self.board))

        #move up left
        move1 = col-1 >= 0 and row-1 >= 0 and (self.board[row-1][col-1] == "--" or self.board[row-1][col-1] == '' or self.board[row-1][col-1][0] == colorPieceOpponent)
        hasOpponent1 = col-1 >= 0 and row-1 >= 0 and self.board[row-1][col-1] != "--" and self.board[row-1][col-1] != '' and self.board[row-1][col-1][0] == colorPieceOpponent
        move2 = col-2 >= 0 and row-2 >= 0 and (self.board[row-2][col-2] == "--" or self.board[row-2][col-2] == '' or self.board[row-2][col-2][0] == colorPieceOpponent)
        hasOpponent2 = col-2 >= 0 and row-2 >= 0 and self.board[row-2][col-2] != "--" and self.board[row-2][col-2] != '' and self.board[row-2][col-2][0] == colorPieceOpponent
        move3 = col-3 >= 0 and row-3 >= 0 and (self.board[row-3][col-3] == "--" or self.board[row-3][col-3] == '' or self.board[row-3][col-3][0] == colorPieceOpponent)
        hasOpponent3 = col-3 >= 0 and row-3 >= 0 and self.board[row-3][col-3] != "--" and self.board[row-3][col-3] != '' and self.board[row-3][col-3][0] == colorPieceOpponent
        move4 = col-4 >= 0 and row-4 >= 0 and (self.board[row-4][col-4] == "--" or self.board[row-4][col-4] == '' or self.board[row-4][col-4][0] == colorPieceOpponent)
        hasOpponent4 = col-4 >= 0 and row-4 >= 0 and self.board[row-4][col-4] != "--" and self.board[row-4][col-4] != '' and self.board[row-4][col-4][0] == colorPieceOpponent
        move5 = col-5 >= 0 and row-5 >= 0 and (self.board[row-5][col-5] == "--" or self.board[row-5][col-5] == '' or self.board[row-5][col-5][0] == colorPieceOpponent)
        hasOpponent5 = col-5 >= 0 and row-5 >= 0 and self.board[row-5][col-5] != "--" and self.board[row-5][col-5] != '' and self.board[row-5][col-5][0] == colorPieceOpponent
        move6 = col-6 >= 0 and row-6 >= 0 and (self.board[row-6][col-6] == "--" or self.board[row-6][col-6] == '' or self.board[row-6][col-6][0] == colorPieceOpponent)
        hasOpponent6 = col-6 >= 0 and row-6 >= 0 and self.board[row-6][col-6] != "--" and self.board[row-6][col-6] != '' and self.board[row-6][col-6][0] == colorPieceOpponent
        move7 = col-7 >= 0 and row-7 >= 0 and (self.board[row-7][col-7] == "--" or self.board[row-7][col-7] == '' or self.board[row-7][col-7][0] == colorPieceOpponent)
        #hasOpponent7 = self.board[row-7][col-7] != "--" and self.board[row-7][col-7] != '' and self.board[row-7][col-7][0] == colorPieceOpponent

        if move1:
            moves.append(Move((row,col), (row-1,col-1), self.board))
        if move1 and not hasOpponent1 and move2:
            moves.append(Move((row,col), (row-2,col-2), self.board))
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3:
            moves.append(Move((row,col), (row-3,col-3), self.board))
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4:
            moves.append(Move((row,col), (row-4,col-4), self.board))
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4 and not hasOpponent4 and move5:
            moves.append(Move((row,col), (row-5,col-5), self.board))
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4 and not hasOpponent4 and move5 and not hasOpponent5 and move6:
            moves.append(Move((row,col), (row-6,col-6), self.board))
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4 and not hasOpponent4 and move5 and not hasOpponent5 and move6 and not hasOpponent6 and move7:
            moves.append(Move((row,col), (row-7,col-7), self.board))

        #move up right
        move1 = col+1 <= 7 and row-1 >= 0 and (self.board[row-1][col+1] == "--" or self.board[row-1][col+1] == '' or self.board[row-1][col+1][0] == colorPieceOpponent)
        hasOpponent1 = col+1 <= 7 and row-1 >= 0 and (self.board[row-1][col+1] != "--" and self.board[row-1][col+1] != '' and self.board[row-1][col+1][0] == colorPieceOpponent)
        move2 = col+2 <= 7 and row-2 >= 0 and (self.board[row-2][col+2] == "--" or self.board[row-2][col+2] == '' or self.board[row-2][col+2][0] == colorPieceOpponent)
        hasOpponent2 = col+2 <= 7 and row-2 >= 0 and (self.board[row-2][col+2] != "--" and self.board[row-2][col+2] != '' and self.board[row-2][col+2][0] == colorPieceOpponent)
        move3 = col+3 <= 7 and row-3 >= 0 and (self.board[row-3][col+3] == "--" or self.board[row-3][col+3] == '' or self.board[row-3][col+3][0] == colorPieceOpponent)
        hasOpponent3 = col+3 <= 7 and row-3 >= 0 and (self.board[row-3][col+3] != "--" and self.board[row-3][col+3] != '' and self.board[row-3][col+3][0] == colorPieceOpponent)
        move4 = col+4 <= 7 and row-4 >= 0 and (self.board[row-4][col+4] == "--" or self.board[row-4][col+4] == '' or self.board[row-4][col+4][0] == colorPieceOpponent)
        hasOpponent4 = col+4 <= 7 and row-4 >= 0 and (self.board[row-4][col+4] != "--" and self.board[row-4][col+4] != '' and self.board[row-4][col+4][0] == colorPieceOpponent)
        move5 = col+5 <= 7 and row-5 >= 0 and (self.board[row-5][col+5] == "--" or self.board[row-5][col+5] == '' or self.board[row-5][col+5][0] == colorPieceOpponent)
        hasOpponent5 = col+5 <= 7 and row-5 >= 0 and (self.board[row-5][col+5] != "--" and self.board[row-5][col+5] != '' and self.board[row-5][col+5][0] == colorPieceOpponent)
        move6 = col+6 <= 7 and row-6 >= 0 and (self.board[row-6][col+6] == "--" or self.board[row-6][col+6] == '' or self.board[row-6][col+6][0] == colorPieceOpponent)
        hasOpponent6 = col+6 <= 7 and row-6 >= 0 and (self.board[row-6][col+6] != "--" and self.board[row-6][col+6] != '' and self.board[row-6][col+6][0] == colorPieceOpponent)
        move7 = col+7 <= 7 and row-7 >= 0 and (self.board[row-7][col+7] == "--" or self.board[row-7][col+7] == '' or self.board[row-7][col+7][0] == colorPieceOpponent)

        if move1:
            moves.append(Move((row,col), (row-1,col+1), self.board))
        if move1 and not hasOpponent1 and move2:
            moves.append(Move((row,col), (row-2,col+2), self.board))
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3:
            moves.append(Move((row,col), (row-3,col+3), self.board))
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4:
            moves.append(Move((row,col), (row-4,col+4), self.board))
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4 and not hasOpponent4 and move5:
            moves.append(Move((row,col), (row-5,col+5), self.board))
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4 and not hasOpponent4 and move5 and not hasOpponent5 and move6:
            moves.append(Move((row,col), (row-6,col+6), self.board))
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4 and not hasOpponent4 and move5 and not hasOpponent5 and move6 and not hasOpponent6 and move7:
            moves.append(Move((row,col), (row-7,col+7), self.board))

        #move down left
        move1 = col-1 >= 0 and row+1 <= 7 and (self.board[row+1][col-1] == "--" or self.board[row+1][col-1] == '' or self.board[row+1][col-1][0] == colorPieceOpponent)
        hasOpponent1 = col-1 >= 0 and row+1 <= 7 and self.board[row+1][col-1] != "--" and self.board[row+1][col-1] != '' and self.board[row+1][col-1][0] == colorPieceOpponent
        move2 = col-2 >= 0 and row+2 <= 7 and (self.board[row+2][col-2] == "--" or self.board[row+2][col-2] == '' or self.board[row+2][col-2][0] == colorPieceOpponent)
        hasOpponent2 = col-2 >= 0 and row+2 <= 7 and self.board[row+2][col-2] != "--" and self.board[row+2][col-2] != '' and self.board[row+2][col-2][0] == colorPieceOpponent
        move3 = col-3 >= 0 and row+3 <= 7 and (self.board[row+3][col-3] == "--" or self.board[row+3][col-3] == '' or self.board[row+3][col-3][0] == colorPieceOpponent)
        hasOpponent3 = col-3 >= 0 and row+3 <= 7 and self.board[row+3][col-3] != "--" and self.board[row+3][col-3] != '' and self.board[row+3][col-3][0] == colorPieceOpponent
        move4 = col-4 >= 0 and row+4 <= 7 and (self.board[row+4][col-4] == "--" or self.board[row+4][col-4] == '' or self.board[row+4][col-4][0] == colorPieceOpponent)
        hasOpponent4 = col-4 >= 0 and row+4 <= 7 and self.board[row+4][col-4] != "--" and self.board[row+4][col-4] != '' and self.board[row+4][col-4][0] == colorPieceOpponent
        move5 = col-5 >= 0 and row+5 <= 7 and (self.board[row+5][col-5] == "--" or self.board[row+5][col-5] == '' or self.board[row+5][col-5][0] == colorPieceOpponent)
        hasOpponent5 = col-5 >= 0 and row+5 <= 7 and self.board[row+5][col-5] != "--" and self.board[row+5][col-5] != '' and self.board[row+5][col-5][0] == colorPieceOpponent
        move6 = col-6 >= 0 and row+6 <= 7 and (self.board[row+6][col-6] == "--" or self.board[row+6][col-6] == '' or self.board[row+6][col-6][0] == colorPieceOpponent)
        hasOpponent6 = col-6 >= 0 and row+6 <= 7 and self.board[row+6][col-6] != "--" and self.board[row+6][col-6] != '' and self.board[row+6][col-6][0] == colorPieceOpponent
        move7 = col-7 >= 0 and row+7 <= 7 and (self.board[row+7][col-7] == "--" or self.board[row+7][col-7] == '' or self.board[row+7][col-7][0] == colorPieceOpponent)
        #hasOpponent7 = self.board[row+7][col-7] != "--" and self.board[row-7][col-7] != '' and self.board[row-7][col-7][0] == colorPieceOpponent

        if move1:
            moves.append(Move((row,col), (row+1,col-1), self.board))
        if move1 and not hasOpponent1 and move2:
            moves.append(Move((row,col), (row+2,col-2), self.board))
        if move1 and not hasOpponent1 and move2  and not hasOpponent2 and move3:
            moves.append(Move((row,col), (row+3,col-3), self.board))
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4:
            moves.append(Move((row,col), (row+4,col-4), self.board))
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4 and not hasOpponent4 and move5:
            moves.append(Move((row,col), (row+5,col-5), self.board))
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4 and not hasOpponent4 and move5 and not hasOpponent5 and move6:
            moves.append(Move((row,col), (row+6,col-6), self.board))
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4 and not hasOpponent4 and move5 and not hasOpponent5 and move6 and not hasOpponent6 and move7:
            moves.append(Move((row,col), (row+7,col-7), self.board))

        #move down right
        move1 = col+1 <= 7 and row+1 <= 7 and (self.board[row+1][col+1] == "--" or self.board[row+1][col+1] == '' or self.board[row+1][col+1][0] == colorPieceOpponent)
        hasOpponent1 = col+1 <= 7 and row+1 <= 7 and self.board[row+1][col+1] != "--" and self.board[row+1][col+1] != '' and self.board[row+1][col+1][0] == colorPieceOpponent
        move2 = col+2 <= 7 and row+2 <= 7 and (self.board[row+2][col+2] == "--" or self.board[row+2][col+2] == '' or self.board[row+2][col+2][0] == colorPieceOpponent)
        hasOpponent2 = col+2 <= 7and row+2 <= 7 and self.board[row+2][col+2] != "--" and self.board[row+2][col+2] != '' and self.board[row+2][col+2][0] == colorPieceOpponent
        move3 = col+3 <= 7 and row+3 <= 7 and (self.board[row+3][col+3] == "--" or self.board[row+3][col+3] == '' or self.board[row+3][col+3][0] == colorPieceOpponent)
        hasOpponent3 = col+3 <= 7and row+3 <= 7 and self.board[row+3][col+3] != "--" and self.board[row+3][col+3] != '' and self.board[row+3][col+3][0] == colorPieceOpponent
        move4 = col+4 <= 7 and row+4 <= 7 and (self.board[row+4][col+4] == "--" or self.board[row+4][col+4] == '' or self.board[row+4][col+4][0] == colorPieceOpponent)
        hasOpponent4 = col+4 <= 7 and row+4 <= 7 and self.board[row+4][col+4] != "--" and self.board[row+4][col+4] != '' and self.board[row+4][col+4][0] == colorPieceOpponent
        move5 = col+5 <= 7 and row+5 <= 7 and (self.board[row+5][col+5] == "--" or self.board[row+5][col+5] == '' or self.board[row+5][col+5][0] == colorPieceOpponent)
        hasOpponent5 = col+5 <= 7 and row+5 <= 7 and self.board[row+5][col+5] != "--" and self.board[row+5][col+5] != '' and self.board[row+5][col+5][0] == colorPieceOpponent
        move6 = col+6 <= 7 and row+6 <= 7 and (self.board[row+6][col+6] == "--" or self.board[row+6][col+6] == '' or self.board[row+6][col+6][0] == colorPieceOpponent)
        hasOpponent6 = col+6 <= 7 and row+6 <= 7 and self.board[row+6][col+6] != "--" and self.board[row+6][col+6] != '' and self.board[row+6][col+6][0] == colorPieceOpponent
        move7 = col+7 <= 7 and row+7 <= 7 and (self.board[row+7][col+7] == "--" or self.board[row+7][col+7] == '' or self.board[row+7][col+7][0] == colorPieceOpponent)

        if move1:
            moves.append(Move((row,col), (row+1,col+1), self.board))
        if move1 and not hasOpponent1 and move2:
            moves.append(Move((row,col), (row+2,col+2), self.board))
        if move1 and not hasOpponent1 and move2  and not hasOpponent2 and move3:
            moves.append(Move((row,col), (row+3,col+3), self.board))
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4:
            moves.append(Move((row,col), (row+4,col+4), self.board))
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4 and not hasOpponent4 and move5:
            moves.append(Move((row,col), (row+5,col+5), self.board))
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4 and not hasOpponent4 and move5 and not hasOpponent5 and move6:
            moves.append(Move((row,col), (row+6,col+6), self.board))
        if move1 and not hasOpponent1 and move2 and not hasOpponent2 and move3 and not hasOpponent3 and move4 and not hasOpponent4 and move5 and not hasOpponent5 and move6 and not hasOpponent6 and move7:
            moves.append(Move((row,col), (row+7,col+7), self.board))

    '''
    Get all queen moves for queen located at row,col
    '''
    def getQueenMoves(self, row, col, moves):
        GameState.getRookMoves(self, row, col, moves)
        GameState.getBishopMoves(self, row, col, moves)

    '''
    Get all king moves for king located at row,col
    !Check for check and check mate!
    !check for castle
    '''
    def getKingMoves(self, row, col, moves):
        colorPieceOpponent = ''
        if self.whiteToMove:
            colorPieceOpponent = 'b'
        else:  # black pawns
            colorPieceOpponent = 'w'

        #move up
        move1 = row-1 >= 0 and (self.board[row-1][col] == "--" or self.board[row-1][col] == '' or self.board[row-1][col][0] == colorPieceOpponent)

        if move1:
            moves.append(Move((row,col), (row-1,col), self.board)) #1 square advance

        #move down
        move1 = row+1 <= 7 and (self.board[row+1][col] == "--" or self.board[row+1][col] == '' or self.board[row+1][col][0] == colorPieceOpponent)

        if move1:
            moves.append(Move((row,col), (row+1,col), self.board)) #1 square advance

        #move left
        move1 = col-1 >= 0 and (self.board[row][col-1] == "--" or self.board[row][col-1] == '' or self.board[row][col-1][0] == colorPieceOpponent)

        if move1:
            moves.append(Move((row,col), (row,col-1), self.board)) #1 square advance

        #move right
        move1 = col+1 <= 7 and (self.board[row][col+1] == "--" or self.board[row][col+1] == '' or self.board[row][col+1][0] == colorPieceOpponent)

        if move1:
            moves.append(Move((row,col), (row,col+1), self.board)) #1 square advance

        #move up left
        move1 = col-1 >= 0 and row-1 >= 0 and (self.board[row-1][col-1] == "--" or self.board[row-1][col-1] == '' or self.board[row-1][col-1][0] == colorPieceOpponent)

        if move1:
            moves.append(Move((row,col), (row-1,col-1), self.board))

        #move up right
        move1 = col+1 <= 7 and row-1 >= 0 and (self.board[row-1][col+1] == "--" or self.board[row-1][col+1] == '' or self.board[row-1][col+1][0] == colorPieceOpponent)

        if move1:
            moves.append(Move((row,col), (row-1,col+1), self.board))

        #move down left
        move1 = col-1 >= 0 and row+1 <= 7 and (self.board[row+1][col-1] == "--" or self.board[row+1][col-1] == '' or self.board[row+1][col-1][0] == colorPieceOpponent)

        if move1:
            moves.append(Move((row,col), (row+1,col-1), self.board))

        #move down right
        move1 = col+1 <= 7 and row+1 <= 7 and (self.board[row+1][col+1] == "--" or self.board[row+1][col+1] == '' or self.board[row+1][col+1][0] == colorPieceOpponent)

        if move1:
            moves.append(Move((row,col), (row+1,col+1), self.board))

        #Castling
        #King and rook has not moved
        #No pieces in between
        #king + 2
        #king not in check, not end in check
        #king not move through square being attacked
        kingCol = 4
        if self.whiteToMove:
            kingRow = 7
            kingHasMoved = self.whiteKingHasMoved
            kingPiece = 'wK'
            rookPiece = 'wR'
        else:
            kingRow = 0
            kingHasMoved = self.blackKingHasMoved
            kingPiece = 'bK'
            rookPiece = 'bR'
        if not kingHasMoved:# and not self.isInCheck() and not self.isGameOver():# and  and not self.whiteRightRookHasMoved:
            #left
            if row == kingRow and col == kingCol and self.board[kingRow][kingCol] == kingPiece \
                and not self.whiteLeftRookHasMoved and self.board[kingRow][0] == rookPiece \
                and self.board[kingRow][3] == '' and self.board[kingRow][2] == '' and self.board[kingRow][1] == '':
                    moves.append(Move((row,col), (row,col-2), self.board))
            #right
            if row == kingRow and col == kingCol and self.board[kingRow][kingCol] == kingPiece \
                and not self.whiteRightRookHasMoved and self.board[kingRow][7] == rookPiece \
                and self.board[kingRow][5] == '' and self.board[kingRow][6] == '':
                    moves.append(Move((row,col), (row,col+2), self.board))


    def getOpponentOption(self, location, beginnerLeft, beginnerTop, intermediateLeft, intermediateTop, advancedLeft, advancedTop, noneLeft, noneTop, intermediatePlusLeft, intermediatePlusTop, advancedPlusLeft, advancedPlusTop):

        self.isOptionBeginner = (beginnerLeft <= location[0] and location[0] <= beginnerLeft+117) and (beginnerTop <= location[1] and location[1] <= beginnerTop+16)
        self.isOptionIntermediate = (intermediateLeft <= location[0] and location[0] <= intermediateLeft+117) and (intermediateTop <= location[1] and location[1] <= intermediateTop+16)

        self.isOptionIntermediatePlus = (intermediatePlusLeft <= location[0] and location[0] <= intermediatePlusLeft+117) and (intermediatePlusTop <= location[1] and location[1] <= intermediatePlusTop+16)

        self.isOptionAdvanced = (advancedLeft <= location[0] and location[0] <= advancedLeft+117) and (advancedTop <= location[1] and location[1] <= advancedTop+16)

        self.isOptionAdvancedPlus = (advancedPlusLeft <= location[0] and location[0] <= advancedPlusLeft+117) and (advancedPlusTop <= location[1] and location[1] <= advancedPlusTop+16)

        self.isOptionNone = not (self.isOptionBeginner or self.isOptionIntermediate or self.isOptionIntermediatePlus or self.isOptionAdvanced or self.isOptionAdvancedPlus)


    def getButtonOption(self, location,
                        buttonUndoTop, buttonUndoLeft,
                        buttonSuggestionTop, buttonSuggestionLeft,
                        buttonLoadTop, buttonLoadLeft,
                        buttonSaveTop, buttonSaveLeft,
                        buttonResetTop, buttonResetLeft,
                        buttonEnableAITop, buttonEnableAILeft,
                        buttonColorAITop, buttonColorAILeft):

        self.isButtonUndo = (buttonUndoLeft <= location[0] and location[0] <= buttonUndoLeft+117) and (buttonUndoTop <= location[1] and location[1] <= buttonUndoTop+16)
        self.isButtonSuggestion = (buttonSuggestionLeft <= location[0] and location[0] <= buttonSuggestionLeft+117) and (buttonSuggestionTop <= location[1] and location[1] <= buttonSuggestionTop+16)
        self.isButtonLoad = (buttonLoadLeft <= location[0] and location[0] <= buttonLoadLeft+117) and (buttonLoadTop <= location[1] and location[1] <= buttonLoadTop+16)
        self.isButtonSave = (buttonSaveLeft <= location[0] and location[0] <= buttonSaveLeft+117) and (buttonSaveTop <= location[1] and location[1] <= buttonSaveTop+16)
        self.isButtonReset = (buttonResetLeft <= location[0] and location[0] <= buttonResetLeft+117) and (buttonResetTop <= location[1] and location[1] <= buttonResetTop+16)
        self.isButtonAIEnabled = (buttonEnableAILeft <= location[0] and location[0] <= buttonEnableAILeft+117) and (buttonEnableAITop <= location[1] and location[1] <= buttonEnableAITop+16)
        self.isButtonAIColorWhite = (buttonColorAILeft <= location[0] and location[0] <= buttonColorAILeft+117) and (buttonColorAITop <= location[1] and location[1] <= buttonColorAITop+16)

    def countPieces(self):
        self.wP = 0
        self.wN = 0
        self.wB = 0
        self.wR = 0
        self.wQ = 0
        self.bP = 0
        self.bN = 0
        self.bB = 0
        self.bR = 0
        self.bQ = 0

        for row in self.board:
            for square in row:
                if square != '' and square != '--':
                    if square[0] == 'w':
                        self.wP += 1 if square[1] == 'p' else 0
                        self.wN += 1 if square[1] == 'N' else 0
                        self.wB += 1 if square[1] == 'B' else 0
                        self.wR += 1 if square[1] == 'R' else 0
                        self.wQ += 1 if square[1] == 'Q' else 0
                    elif square[0] == 'b':
                        self.bP += 1 if square[1] == 'p' else 0
                        self.bN += 1 if square[1] == 'N' else 0
                        self.bB += 1 if square[1] == 'B' else 0
                        self.bR += 1 if square[1] == 'R' else 0
                        self.bQ += 1 if square[1] == 'Q' else 0

        #self.countedPieces = {'': 0, '': 0, '': 0, '': 0, '': 0, '': 0, '': 0, '': 0, '': 0, '': 0, '': 0, '': 0}
        self.countedPieces['wK'] = 0
        self.countedPieces['wQ'] = self.wQ
        self.countedPieces['wR'] = self.wR
        self.countedPieces['wB'] = self.wB
        self.countedPieces['wN'] = self.wN
        self.countedPieces['wp'] = self.wP
        self.countedPieces['bK'] = 0
        self.countedPieces['bQ'] = self.bQ
        self.countedPieces['bR'] = self.bR
        self.countedPieces['bB'] = self.bB
        self.countedPieces['bN'] = self.bN
        self.countedPieces['bp'] = self.bP

class Move():
    #maps keys to values
    #key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or \
                               (self.pieceMoved == 'bp' and self.endRow == 7)
        self.isUserClicked = False

        # self.wP = 0
        # self.wN = 0
        # self.wB = 0
        # self.wR = 0
        # self.wQ = 0
        # self.bP = 0
        # self.bN = 0
        # self.bB = 0
        # self.bR = 0
        # self.bQ = 0

        #if (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7):
        #    self.isPawnPromotion = True

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        #print(self.moveID)

    '''
    Override equal method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]