import random

PieceScores={'K':0, 'Q':10, 'R':5, 'B':3, 'N':3, 'p':1 }
CheckMate = 1000
StaleMate = 0
MaxDepth = 3


def generateMove(gs, validMoves, isBeginner, isIntermediate, isAdvanced, isIntermediatePlus, isAdvancedPlus):
    #depending on option selected return a move
    if isBeginner:
        #random
        return findRandomMove(validMoves)
    elif isIntermediate:
        #eval all moves
        return findBestMove(gs, validMoves)
    elif isIntermediatePlus:
        #compare min and max scores per colour
        return findBestMoveMinMax(gs, validMoves)
    elif isAdvanced:
        #compare score for entire board
        return findBestMoveNegaMax(gs, validMoves)
    elif isAdvancedPlus:
        #compare score for entire board and use alpha beta pruning
        return findBestMoveNegaMaxAlphaBeta(gs, validMoves)

'''
find the best move based on scores
'''
def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    #maxScore = -turnMultiplier * CheckMate
    opponentMinMaxScore = CheckMate
    bestMove = None
    random.shuffle(validMoves)
    for move in validMoves:
        gs.makeMove(move)
        opponentMoves = gs.getValidMoves()

        if gs.isInStaleMate:
            opponentMaxScore = StaleMate
        elif gs.isInCheckMate:
            opponentMaxScore = -CheckMate
        else:
            opponentMaxScore = -CheckMate
            for opponentMove in opponentMoves:
                gs.makeMove(opponentMove)
                gs.getValidMoves()

                if gs.isInCheckMate:
                    score = CheckMate #-turnMultiplier * CheckMate
                elif gs.isInStaleMate:
                    score = StaleMate
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)

                #max
                if score > opponentMaxScore:
                    opponentMaxScore = score
                    #bestMove = move
                    #if score > 0:
                    #    print("Opp-possible move:" + opponentMove.getChessNotation() + " ("+str(score)+")")

                gs.undoMove()

        #min
        if opponentMinMaxScore > opponentMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestMove = move;
            #if opponentMaxScore > 0:
            print("Opp-possible move:" + move.getChessNotation() + " ("+str(opponentMaxScore)+")")

        gs.undoMove()

    return bestMove


# '''
# find the best move based on scores
# '''
# def findBestMove(gs, validMoves):
#     turnMultiplier = 1 if gs.whiteToMove else -1
#     maxScore = -turnMultiplier * CheckMate
#     opponentMinMaxScore = CheckMate
#     bestMove = None
#     random.shuffle(validMoves)
#     for move in validMoves:
#         gs.makeMove(move)
#         opponentMoves = gs.getValidMoves()
#         #random.shuffle(opponentMoves)
#         opponentMaxScore = -CheckMate
#         for opponentMove in opponentMoves:
#             gs.makeMove(opponentMove)
#
#             if gs.isInCheckMate:
#                 score = -turnMultiplier * CheckMate
#             elif gs.isInStaleMate:
#                 score = StaleMate
#             else :
#                 score = -turnMultiplier * scoreMaterial(gs.board)
#
#             #max
#             if score > opponentMaxScore:
#                 opponentMaxScore = score
#                 #bestMove = move
#
#             gs.undoMove()
#
#         #min
#         if opponentMinMaxScore > opponentMaxScore:
#             opponentMinMaxScore = opponentMaxScore
#             bestMove = move;
#
#         gs.undoMove()
#
#     return bestMove


'''
Recursive calls
'''
def findBestMoveMinMax(gs, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    findMoveMinMax(gs, validMoves, MaxDepth, gs.whiteToMove);

    return nextMove

def findMoveMinMax(gs, validMoves, depth, whiteTomove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)

    if whiteTomove:
        maxScore = -CheckMate
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, False)
            if score > maxScore:
                maxScore = score
                if depth == MaxDepth:
                    nextMove = move
                if score > 0:
                    print("W-possible move:" + move.getChessNotation() + " (score:"+str(score)+")(depth:"+str(depth)+")")
            gs.undoMove()
        return maxScore
    else:
        minScore = CheckMate
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, True)
            if score < minScore:
                minScore = score
                if depth == MaxDepth:
                    nextMove = move
                if score > 0:
                    print("B-possible move:" + move.getChessNotation() + " (score:"+str(score)+")(depth:"+str(depth)+")")
            gs.undoMove()
        return minScore

'''
Random move
'''
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

'''
score board
'''
def scoreMaterial(board):
    score = 0
    wScore = 0
    bScore = 0
    for row in board:
        for square in row:
            if square != '':
                if square[0] == 'w':
                    score += PieceScores[square[1]]
                    wScore += PieceScores[square[1]]
                elif square[0] == 'b':
                    score -= PieceScores[square[1]]
                    bScore += PieceScores[square[1]]
                #print('.')

    # print('W:' + str(wScore))
    # print('B:' + str(bScore))

    return score

'''
Score entire board. Positive number is good for white, negative is good for black
'''
def scoreBoard(gs):
    if gs.isInCheckMate:
        if gs.whiteToMove:
            return -CheckMate #black won
        else:
            return CheckMate #white won
    elif gs.isInStaleMate:
        if gs.whiteToMove:
            return -StaleMate
        else:
            return StaleMate

    score = 0
    for row in gs.board:
        for square in row:
            if square != '' and square != '--':
                #print('1 square[0]:'+str(square[0])+' square[1]:'+square[1]+' PieceScores[square[1]]:'+str(PieceScores[square[1]])+' score:'+str(score))
                if square[0] == 'w':
                    score += PieceScores[square[1]]
                elif square[0] == 'b':
                    score -= PieceScores[square[1]]
                #print('2 square[0]:'+str(square[0])+' square[1]:'+square[1]+' PieceScores[square[1]]:'+str(PieceScores[square[1]])+' score:'+str(score))

    return score

def findBestMoveNegaMax(gs, validMoves):
    global nextMove, counter
    nextMove = None
    counter = 0
    random.shuffle(validMoves)

    score = findMoveNegaMax(gs, validMoves, MaxDepth, 1 if gs.whiteToMove else -1)

    print("(score after findMoveNegaMax:" + str(score) + ")(counter:"+str(counter)+")")
    #print('PieceScores[square[p]:' + str(PieceScores['p']))
    #print('PieceScores[square[N]:' + str(PieceScores['N']))
    #print('PieceScores[square[B]:' + str(PieceScores['B']))


    return nextMove

def findMoveNegaMax(gs, validMoves, depth, whiteToMoveInt):
    #print("whiteToMoveInt:" + str(whiteToMoveInt) + " (depth:" + str(depth) + ")")
    global nextMove,counter
    counter += 1

    if depth == 0:
        return whiteToMoveInt * scoreBoard(gs)
        #whiteToMoveInt = turnMultiplier

    maxScore = -CheckMate
    counterInner=0
    for move in validMoves:
        counterInner += 1
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth -1, -whiteToMoveInt)
        if score > maxScore:
            maxScore = score
            if depth == MaxDepth:
                nextMove = move
            #if score > 0:
            if whiteToMoveInt == 1:
                print("W-possible move:" + move.getChessNotation() + " (score:" + str(score) + ")(depth:" + str(
                    depth) + ")(counter:" + str(counterInner) + ")")
            else:
                print("B-possible move:" + move.getChessNotation() + " (score:" + str(score) + ")(depth:" + str(
                    depth) + ")(counter:" + str(counterInner) + ")")
        gs.undoMove()

    return maxScore

def findBestMoveNegaMaxAlphaBeta(gs, validMoves):
    global nextMove, counter
    nextMove = None
    counter = 0
    random.shuffle(validMoves)

    score = findMoveNegaMaxAlphaBeta(gs, validMoves, MaxDepth, -CheckMate, CheckMate, 1 if gs.whiteToMove else -1)

    print("(score after findMoveNegaMaxAlphaBeta:" + str(score) + ")(counter:"+str(counter)+")")
    #print('PieceScores[square[p]:' + str(PieceScores['p']))
    #print('PieceScores[square[N]:' + str(PieceScores['N']))
    #print('PieceScores[square[B]:' + str(PieceScores['B']))

    #gs.countPieces()

    return nextMove

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, whiteToMoveInt):
    #print("whiteToMoveInt:" + str(whiteToMoveInt) + " (depth:" + str(depth) + ")")
    global nextMove,counter
    counter += 1
    if depth == 0:
        return whiteToMoveInt * scoreBoard(gs)
        #whiteToMoveInt = turnMultiplier

    maxScore = -CheckMate
    counterInner = 0
    for move in validMoves:
        counterInner += 1
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth -1, -beta, -alpha, -whiteToMoveInt)
        if score > maxScore:
            maxScore = score
            if depth == MaxDepth:
                nextMove = move
            #if score > 0:
            if whiteToMoveInt == 1:
                print("W-possible move:" + move.getChessNotation() + " (score:" + str(score) + ")(depth:" + str(depth) + ")(counter:"+str(counterInner)+")")
            else:
                print("B-possible move:" + move.getChessNotation() + " (score:" + str(score) + ")(depth:" + str(depth) + ")(counter:"+str(counterInner)+")")
        gs.undoMove()
        #pruning
        if maxScore > alpha:
           alpha = maxScore
        if alpha >= beta:
           break

    return maxScore

# def countPieces(gs):
#     gs.wP = 0
#     gs.wN = 0
#     gs.wB = 0
#     gs.wR = 0
#     gs.wQ = 0
#     gs.bP = 0
#     gs.bN = 0
#     gs.bB = 0
#     gs.bR = 0
#     gs.bQ = 0
#
#     for row in gs.board:
#         for square in row:
#             if square != '' and square != '--':
#                 if square[0] == 'w':
#                     gs.wP += 1 if square[1] == 'p' else 0
#                     gs.wN += 1 if square[1] == 'N' else 0
#                     gs.wB += 1 if square[1] == 'B' else 0
#                     gs.wR += 1 if square[1] == 'R' else 0
#                     gs.wQ += 1 if square[1] == 'Q' else 0
#                 elif square[0] == 'b':
#                     gs.bP += 1 if square[1] == 'p' else 0
#                     gs.bN += 1 if square[1] == 'N' else 0
#                     gs.bB += 1 if square[1] == 'B' else 0
#                     gs.bR += 1 if square[1] == 'R' else 0
#                     gs.bQ += 1 if square[1] == 'Q' else 0

#def findBestMove():

#def findFastest

