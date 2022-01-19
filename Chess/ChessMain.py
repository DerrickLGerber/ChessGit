"""
UI display and handling user input
"""
import datetime

import pygame as p
import pygame.surface

import os

# from tkinter import *
# import tkinter as tk

#from tkinter import *

import tkinter
#import tkFileDialog
#import tkinter.filedialog

from Chess import ChessEngine, SmartMoveFinder

"""
    :) Workable chess set
    :) Determine check / check mate
    :) Prevent move when creating check / check mate
    :) Cancel move
    :) indicate black or white's turn
    :) enpassant
    :) castle
    :) ai - minimax, negamax, alpha-beta pruning

    :) player level - beginner, intermediate, advanced (no suggestions or possible blue squares) 
    :) player timing
    :) enable or disable AI
    :) select human color

    :) Automated Tutoring On / Off
    :) Suggest Move On / Off 

    :) indicate check, check mate

    :) clock tick
mouse cursor
Suggestion only in beginner and intermeditate
Esc - stop thinking
Summary of pieces
Beginner, Intermediate - show pieces and move image
Load, Save - allow load lessons

web engine
https://colab.research.google.com/github/iAmEthanMai/chess-engine-model/blob/main/python_chess_engine.ipynb#scrollTo=tIks0yXVpEw2
score track
Reset button

Dec 2021
    :) Suggestion
    :) Save
    :) Load
    :) En passant
    :) Castle
    :) Possible time per options - suggestion or move
    :) Enable AI so black can get suggesstions
    :) buttons load, save
    :) clock tick
    :) set self.whiteKingHasMoved = False,self.whiteLeftRookHasMoved = False,self.whiteRightRookHasMoved = False
    :) self.blackKingHasMoved = False,self.blackLeftRookHasMoved = False,self.blackRightRookHasMoved = False
    :) test castling and en passant with AI
Progress .... while thinking ...
mouse cursor for waiting
Reset should reset the clocks
description of move
possible animations
restart new game
Good or Bad previous move

AI Enabled -  clock not ticking
"""

#WIDTH = HEIGHT = 512 #400
WIDTH = 900 #512#650
HEIGHT = 800 #512 #400
DIMENSION = 8 #8x8
BOARDHEIGHT = 512
SQUARE_SIZE = BOARDHEIGHT // DIMENSION
PADLEFT=30
PADTOP=50
SUMMARY_SQUARE_SIZE = BOARDHEIGHT // DIMENSION
SUMMARY_PADLEFT=30
SUMMARY_PADTOP=600
#MAX_SECONDS = 300
MAX_MINUTES_PLAY = 5

MAX_FPS = 15 #for animations
IMAGES = {}

IsOptionBeginner = False
OptionBeginnerTop = 440
OptionBeginnerLeft = 630

IsOptionIntermediate = False
OptionIntermediateTop = 460
OptionIntermediateLeft = 630

IsOptionIntermediatePlus = False
OptionIntermediatePlusTop = 460
OptionIntermediatePlusLeft = 770

IsOptionAdvanced = False
OptionAdvancedTop = 480
OptionAdvancedLeft = 630

IsOptionAdvancedPlus = False
OptionAdvancedPlusTop = 480
OptionAdvancedPlusLeft = 770

IsOptionNone = True
OptionNoneTop = 440
OptionNoneLeft = 770

ButtonUndoTop = 510
ButtonUndoLeft = 630
ButtonSuggestionTop = 535
ButtonSuggestionLeft = 630

ButtonLoadTop = 510
ButtonLoadLeft = 770#800
ButtonSaveTop = 535
ButtonSaveLeft = 770#800
ButtonResetTop = 560
ButtonResetLeft = 770#800

ButtonEnableAITop = 600#560
ButtonEnableAILeft = 630
ButtonColorAITop = 600
ButtonColorAILeft = 770#800

IsButtonUndo = False
IsButtonSuggestion = False
IsButtonAIEnabled = False
IsAIEnabled = False
IsButtonAIColorWhite = False
IsAIColorWhite = False
IsButtonLoad = False
IsButtonSave = False
IsButtonReset = False
CountPiecesInitialized = False
#WhiteSeconds = 0
#BlackSeconds = 0

#drawnPawnPromotionLeft = 0
#drawnPawnPromotionTop = 0
#pawnPromotionPieces = []

PlayerTurnCircleWhiteLeft = 660
PlayerTurnCircleWhiteTop = 220
PlayerTurnCircleBlackLeft = 820
PlayerTurnCircleBlackTop = 220

PlayerTurnWhiteTop = 150
PlayerTurnWhiteLeft = 643
PlayerTurnBlackTop = 150
PlayerTurnBlackLeft = 807

'''
Initialise a global dictionary of images
'''
def loadImages():
    #IMAGES['wp'] = p.image.load("images/wp.png")
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']

    print("Path:" + os.getcwd())
    print("Path:" + os.getcwd()[-5::])

    if os.getcwd()[-5::] != 'Chess':
        os.chdir(os.getcwd() + '/Chess')
        print("Path:" + os.getcwd())

    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/"+piece+".png"), (SQUARE_SIZE, SQUARE_SIZE))
        #can now access IMAGES['wp']

    piece = 'button1'
    IMAGES[piece] = p.transform.scale(p.image.load("images/"+piece+".png"), (130, 23))

'''
main driver for the code - updates graphics and handles user input
'''
def main():
    p.init()
    p.display.set_caption('Chess Playing Tutoring')
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validmoves = gs.getValidMoves()
    moveMade = False #flag for when a move is made

    gs.countPieces()

    #print(gs.board)
    loadImages()
    running = True
    sqSelected = ()#no square selected (tuple: (row,col))
    playerClicks = []#user clicks. Two tuples (6,4) to (4,4)
    gameOver = False
    humanOnly = False
    playerOne = True  #human player
    playerTwo = False

    IsOptionBeginner = False
    IsOptionIntermediate = False
    IsOptionIntermediatePlus = False
    IsOptionAdvanced = False
    IsOptionAdvancedPlus = False
    IsOptionNone = True

    IsButtonUndo = False
    IsButtonSuggestion = False
    IsButtonAIEnabled = False
    IsAIEnabled = False
    IsButtonAIColorWhite = False
    IsAIColorWhite = False
    IsButtonLoad = False
    IsButtonSave = False
    IsButtonReset = False
    CountPiecesInitialized = False

    while running:
        if humanOnly:
            #manual hardcode
            humanTurn = True
        else:
            #humanTurn = not IsAIEnabled or ((gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)) #IsOptionNone
            humanTurn = (not IsAIEnabled or IsOptionNone) or ((gs.whiteToMove and not IsAIColorWhite) or (not gs.whiteToMove and IsAIColorWhite)) #IsOptionNone

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos() #mouse x,y
                    #gs.getOpponentOption(location, BeginnerLeft, BeginnerTop, IntermediateLeft, IntermediateTop, AdvancedLeft, AdvancedTop, NoneLeft, NoneTop)

                    # col = location[0]//SQUARE_SIZE
                    # row = location[1]//SQUARE_SIZE
                    col = (location[0]-PADLEFT)//SQUARE_SIZE
                    row = (location[1]-PADTOP)//SQUARE_SIZE

                    #pawn promotions
                    if location[0] >= gs.drawnPawnPromotionLeft and gs.drawnPawnPromotionLeft > 0\
                        and gs.drawnPawnPromotionTop <= location[1] and location[1] < OptionBeginnerTop:

                        #gs.drawnPawnPromotionLeft = left
                        #gs.drawnPawnPromotionTop = top

                        col = (location[0]-gs.drawnPawnPromotionLeft)//SQUARE_SIZE
                        pawnPromotionPiece = ''
                        if col <= len(gs.pawnPromotionPieces):
                            pawnPromotionPiece = gs.pawnPromotionPieces[col]
                            if gs.hasPawnPromotion \
                                and pawnPromotionPiece != '' \
                                and pawnPromotionPiece != gs.board[gs.lastPawnPromotionRow][gs.lastPawnPromotionCol]:
                                gs.board[gs.lastPawnPromotionRow][gs.lastPawnPromotionCol] = pawnPromotionPiece

                            #self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'
                            #self.hasPawnPromotion = move.isPawnPromotion
                            #self.lastPawnPromotionRow = move.endRow
                            #self.lastPawnPromotionCol = move.endCol

                    else:
                        #clicked on board
                        if row < 8 and col < 8:
                            if sqSelected == (row, col):#same cells clicked
                                sqSelected=()#deselect
                                playerClicks=[]#clear
                            else:
                                sqSelected = (row, col)
                                playerClicks.append(sqSelected)#append 1st and 2nd clicks

                            if len(playerClicks) == 2: #after second clicks
                                move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                                print(move.getChessNotation())
                                for i in range(len(validmoves)):
                                    if move == validmoves[i]:
                                        #move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                                        move.isUserClicked = True
                                        gs.hasPawnPromotion = False
                                        gs.pawnPromotionPieces = []
                                        gs.makeMove(move) #validmoves[i])
                                        gs.storeLastMove(move)
                                        moveMade = True
                                        sqSelected=()#reset user clicks
                                        playerClicks=[]
                                if not moveMade:
                                    playerClicks=[sqSelected]

                        elif OptionBeginnerLeft <= location[0] and location[0] <= OptionNoneLeft + 117 and OptionBeginnerTop <= location[1] and location[1] <= OptionAdvancedTop + 16:
                            # check options
                            gs.getOpponentOption(location,
                                                 OptionBeginnerLeft, OptionBeginnerTop,
                                                 OptionIntermediateLeft, OptionIntermediateTop,
                                                 OptionAdvancedLeft, OptionAdvancedTop,
                                                 OptionNoneLeft, OptionNoneTop,
                                                 OptionIntermediatePlusLeft, OptionIntermediatePlusTop,
                                                 OptionAdvancedPlusLeft, OptionAdvancedPlusTop)

                            IsOptionBeginner = gs.isOptionBeginner
                            IsOptionIntermediate = gs.isOptionIntermediate
                            IsOptionAdvanced = gs.isOptionAdvanced
                            IsOptionNone = gs.isOptionNone
                            IsOptionIntermediatePlus = gs.isOptionIntermediatePlus
                            IsOptionAdvancedPlus = gs.isOptionAdvancedPlus

                            if IsOptionIntermediatePlus: print("Option-Intermediate+ (MinMax)")
                            if IsOptionIntermediate: print("Option-Intermediate (Best)")
                            if IsOptionBeginner: print("Option-Beginner (Random)")
                            if IsOptionAdvanced: print("Option-Advanced (NegaMax)")
                            if IsOptionAdvancedPlus: print("Option-Advanced+ (NegaMax Alpha-Beta)")
                            if IsOptionNone: print("Option-None")

                        elif ButtonUndoLeft <= location[0] and location[0] <= ButtonLoadLeft + 117 and ButtonUndoTop <= location[1] and location[1] <= ButtonEnableAITop + 16:
                            # check buttons
                            gs.getButtonOption(location,
                                                ButtonUndoTop, ButtonUndoLeft,
                                                ButtonSuggestionTop, ButtonSuggestionLeft,
                                                ButtonLoadTop, ButtonLoadLeft,
                                                ButtonSaveTop, ButtonSaveLeft,
                                                ButtonResetTop, ButtonResetLeft,
                                                ButtonEnableAITop, ButtonEnableAILeft,
                                                ButtonColorAITop, ButtonColorAILeft)

                            IsButtonUndo = gs.isButtonUndo
                            IsButtonSuggestion = gs.isButtonSuggestion
                            IsButtonLoad = gs.isButtonLoad
                            IsButtonSave = gs.isButtonSave
                            IsButtonReset = gs.isButtonReset
                            IsButtonAIEnabled = gs.isButtonAIEnabled
                            IsButtonAIColorWhite = gs.isButtonAIColorWhite

                            #switch ai enabled on or off
                            #isAIEnabledOld = IsAIEnabled
                            if IsButtonAIEnabled:
                                IsAIEnabled = not IsAIEnabled#isAIEnabledOld
                                gs.isAIEnabled = IsAIEnabled
                                if IsAIEnabled: print("AI Enable")
                                else: print("AI Disabled")

                            #switch ai color white on or off
                            #isAIColorWhiteOld = IsAIColorWhite
                            if IsButtonAIColorWhite:
                                IsAIColorWhite = not IsAIColorWhite
                                gs.isAIColorWhite = IsAIColorWhite
                                if IsAIColorWhite: print("AI Color White")
                                else: print("AI Color not White")

                            if IsButtonUndo:
                                print("Button-Undo.")
                                gs.undoMove()
                                moveMade = True
                            if IsButtonSuggestion:
                                print("Button-Suggestion.")

                                move = SmartMoveFinder.generateMove(gs, validmoves, IsOptionBeginner,
                                                                      IsOptionIntermediate, IsOptionAdvanced,
                                                                      IsOptionIntermediatePlus, IsOptionAdvancedPlus)

                                if (move != None):
                                    sqSelected = (move.startRow, move.startCol)

                                # if sqSelected == (row, col):  # same cells clicked
                                #     sqSelected = ()  # deselect
                                #     playerClicks = []  # clear
                                # else:
                                #     sqSelected = (row, col)
                                #     playerClicks.append(sqSelected)  # append 1st and 2nd clicks

                            #if IsAIEnabled: print("AI Enabled")
                            if IsButtonLoad:
                                print("Button-Load.")
                                loadFromFile(gs)
                            if IsButtonSave:
                                print("Button-Save.")
                                saveToFile(gs)
                            if IsButtonReset:
                                print("Button-Reset.")
                                #gs.setCleanBoard()
                                #moveMade = True
                                gs = ChessEngine.GameState()
                                validmoves = gs.getValidMoves()
                                #CountPiecesInitialized = False
                                moveMade = False  # flag for when a move is made
                                gameOver = False
                                sqSelected = ()  # reset user clicks
                                playerClicks = []
                                gs.countPieces()
                                gs.whiteKingHasMoved = False
                                gs.whiteLeftRookHasMoved = False
                                gs.whiteRightRookHasMoved = False
                                gs.blackKingHasMoved = False
                                gs.blackLeftRookHasMoved = False
                                gs.blackRightRookHasMoved = False
                                gs.whiteSeconds = 0
                                gs.blackSeconds = 0

                                gs.isOptionBeginner = IsOptionBeginner
                                gs.isOptionIntermediate = IsOptionIntermediate
                                gs.isOptionAdvanced = IsOptionAdvanced
                                gs.isOptionNone = IsOptionNone
                                gs.isOptionIntermediatePlus = IsOptionIntermediatePlus
                                gs.isOptionAdvancedPlus = IsOptionAdvancedPlus
                                gs.isAIEnabled = IsAIEnabled
                                gs.isAIColorWhite = IsAIColorWhite

                    #playerOne = not playerOne
                    #playerTwo = not playerTwo
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo on z
                    gs.undoMove()
                    moveMade = True

        #AI moves
        if not gameOver and not humanTurn and not IsOptionNone and IsAIEnabled:
            #aiStartTime = gs.startTime
            gs.isAICalculating = True
            moveAI = SmartMoveFinder.generateMove(gs, validmoves, IsOptionBeginner, IsOptionIntermediate, IsOptionAdvanced, IsOptionIntermediatePlus, IsOptionAdvancedPlus)
            gs.isAICalculating = False
            gs.moveSummary = moveAI
            gs.makeMove(moveAI)
            gs.storeLastMove(move)
            moveMade = True
            gs.setTime()
            #gs.startTime = aiStartTime
            #playerOne = not playerOne
            #playerTwo = not playerTwo

        gs.moveMade = False
        if moveMade:
            validmoves = gs.getValidMoves()
            gameOver = gs.isGameOver() #gs.isInStaleMate or gs.isInCheckMate or gs.timeHasExpired
            moveMade = False
            gs.moveMade = True
            gs.countPieces()
            gs.getTimes()

        #if checkmate
        #gameOver = True

        drawGameState(screen, gs, sqSelected, validmoves)
        clock.tick(MAX_FPS)
        p.display.flip()
        #print(clock.get_rawtime())


'''
Responsible for graphics
'''
def drawGameState(screen, gs, sqSelected, validmoves):
    drawBoard(screen, gs, sqSelected, validmoves)#draw squares on board
    drawPlayerTime(screen, gs)
    drawGameOver(screen, gs) #notification
    drawPieces(screen, gs.board)#draw pieces

    #if not CountPiecesInitialized or gs.moveMade:
    drawPieceSummary(screen, gs)
    #CountPiecesInitialized = True

    drawPossibleOptions(screen, gs, sqSelected, validmoves) #if square was select on first click

    if IsButtonSuggestion and sqSelected != ():
        drawPossibleSuggestions(screen, gs, sqSelected, validmoves) #user clicked suggestion

    drawPlayerTurn(screen, gs.whiteToMove) #draw player turn
    drawPawnPromotion(screen, gs) #draw pawn promotion area
    drawPlayerLevels(screen, gs) #beginner, intermediate, advanced
    drawOptions(screen, gs) #options available to user


'''
Draw squares. Top left square is always white/light
'''
def drawBoard(screen, gs, sqSelected, validmoves):
    colors = [p.Color("light gray"), p.Color("gray")]
    selected = p.Color("light blue")
    #ranksToRows = gs.getRanksToRows()
    rowsToRanks = gs.getRowsToRanks()
    colsToFiles = gs.getColsToFiles()
    fontr = p.font.Font('freesansbold.ttf', 10)

    selectedOption = False

    for row in range(DIMENSION):
        for col in range(DIMENSION):
            if sqSelected == (row, col):
                #selected square
                color = selected
                selectedOption = True
            else:
                color = colors[((row + col) % 2)]

            #draw a square
            p.draw.rect(screen, color, p.Rect(col*SQUARE_SIZE+PADLEFT, row*SQUARE_SIZE+PADTOP, SQUARE_SIZE, SQUARE_SIZE))

            #if selectedOption:
            #    drawPossibleOptions(screen, gs, sqSelected, validmoves)

            if row == (DIMENSION-1):
                # horizontal letters
                #fontr = p.font.Font('freesansbold.ttf', 10)
                #color = colors[((row) % 2)]
                textc = fontr.render(colsToFiles[col], False, p.Color("black"), p.Color(color))
                textRectc = textc.get_rect()
                textRectc.top = (row * SQUARE_SIZE + PADTOP) + (SQUARE_SIZE * 0.85)
                textRectc.left = (col*SQUARE_SIZE+PADLEFT) + (SQUARE_SIZE * 0.90)
                screen.blit(textc, textRectc)

        #vertical numbers
        #fontr = p.font.Font('freesansbold.ttf', 10)
        color = colors[((row) % 2)]
        #textr = fontr.render(str(row+1), False, p.Color("black"), p.Color(color))
        #textr = fontr.render(str(ranksToRows[str(row+1)]+1), False, p.Color("black"), p.Color(color))
        textr = fontr.render(rowsToRanks[row], False, p.Color("black"), p.Color(color))
        textRectr = textr.get_rect()
        textRectr.top = row*SQUARE_SIZE+PADTOP
        textRectr.left = PADLEFT
        screen.blit(textr, textRectr)

    #ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
    #               "5": 3, "6": 2, "7": 1, "8": 0}
    #filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
    #               "e": 4, "f": 5, "g": 6, "h": 7}


    #p.draw.rect(screen, p.Color("black"), p.Rect(15, 25, BOARDHEIGHT+15, BOARDHEIGHT+25))
    #                                     (left,top)     (left,top)

    #board
    #top
    p.draw.line(screen, p.Color("black"), (0,PADTOP), ((DIMENSION*SQUARE_SIZE)+PADLEFT+PADLEFT,PADTOP), 2)
    #bottom
    p.draw.line(screen, p.Color("black"), (0,(DIMENSION*SQUARE_SIZE)+PADLEFT+PADLEFT), ((DIMENSION*SQUARE_SIZE)+PADLEFT+PADLEFT,(DIMENSION*SQUARE_SIZE)+PADLEFT+PADLEFT), 2)
    #right
    p.draw.line(screen, p.Color("black"), ((DIMENSION*SQUARE_SIZE)+PADLEFT+PADLEFT,PADTOP), ((DIMENSION*SQUARE_SIZE)+PADLEFT+PADLEFT,(DIMENSION*SQUARE_SIZE)+PADLEFT+PADLEFT), 2)

    #menu
    #right
    #p.draw.line(screen, p.Color("black"), ((DIMENSION*SQUARE_SIZE)+PADLEFT+PADLEFT+10,0), ((DIMENSION*SQUARE_SIZE)+PADLEFT+PADLEFT+10,(DIMENSION*SQUARE_SIZE)+PADLEFT+PADLEFT+10), 2)
    p.draw.line(screen, p.Color("black"), ((DIMENSION*SQUARE_SIZE)+PADLEFT+PADLEFT+10,0), ((DIMENSION*SQUARE_SIZE)+PADLEFT+PADLEFT+10,HEIGHT), 2)

    #players
    #bottom
    p.draw.line(screen, p.Color("black"), ((DIMENSION*SQUARE_SIZE)+PADLEFT+PADLEFT+10,300), (WIDTH,300), 2)
    #vertical split
    p.draw.line(screen, p.Color("black"), ((DIMENSION*SQUARE_SIZE)+PADLEFT+PADLEFT+170,0), ((DIMENSION*SQUARE_SIZE)+PADLEFT+PADLEFT+170,300), 2)

    font = p.font.Font('freesansbold.ttf',20)
    text1 = font.render('Player 1', False, p.Color("black"), p.Color("white"))
    textRect1 = text1.get_rect()
    textRect1.top = 10
    textRect1.left = 630
    screen.blit(text1, textRect1)

    text2 = font.render('Player 2', False, p.Color("black"), p.Color("white"))
    textRect2 = text2.get_rect()
    textRect2.top = 10
    textRect2.left = 780
    screen.blit(text2, textRect2)

    text3 = font.render('Board', False, p.Color("black"), p.Color("white"))
    textRect3 = text3.get_rect()
    textRect3.top = 10
    textRect3.left = 260
    screen.blit(text3, textRect3)

    # timeTodisplay = '00:00'
    # displayWhite = True
    # timeTodisplay = gs.getTimesToDisplay(displayWhite)
    #
    # fontT = p.font.Font('freesansbold.ttf',40)
    # textT1 = fontT.render(timeTodisplay, False, p.Color("black"), p.Color("white"))
    # textRectT1 = textT1.get_rect()
    # textRectT1.top = 50
    # textRectT1.left = 615
    # screen.blit(textT1, textRectT1)
    #
    # timeTodisplay = "00:00"
    # displayWhite = False
    # timeTodisplay = gs.getTimesToDisplay(displayWhite)
    #
    # textT2 = fontT.render(timeTodisplay, False, p.Color("black"), p.Color("white"))
    # textRectT2 = textT2.get_rect()
    # textRectT2.top = 50
    # textRectT2.left = 765
    # screen.blit(textT2, textRectT2)

    # fontBig = p.font.Font('freesansbold.ttf',35)
    # text4 = fontBig.render('W', True, p.Color("black"), p.Color("white"))
    # textRect4 = text4.get_rect()
    # textRect4.top = 150
    # textRect4.left = 644
    # screen.blit(text4, textRect4)
    #
    # text5 = fontBig.render('B', True, p.Color("black"), p.Color("white"))
    # textRect5 = text5.get_rect()
    # textRect5.top = 150
    # textRect5.left = 807
    # screen.blit(text5, textRect5)


    #description
    #top
    p.draw.line(screen, p.Color("black"), (0,(DIMENSION*SQUARE_SIZE)+PADLEFT+PADLEFT+10), (WIDTH,(DIMENSION*SQUARE_SIZE)+PADLEFT+PADLEFT+10), 2)

'''
Draw the time its taking each player
'''
def drawPlayerTime(screen, gs):

    #clear background
    fontW = p.font.Font('freesansbold.ttf',40)
    textW = fontW.render('00000', False, p.Color("white"), p.Color("white"))
    textRectW = textW.get_rect()
    textRectW.top = 50
    textRectW.left = 615
    screen.blit(textW, textRectW)

    textRectW2 = textW.get_rect()
    textRectW2.top = 50
    textRectW2.left = 765
    screen.blit(textW, textRectW2)

    timeToDisplay = '00:00'
    displayWhite = True
    timeToDisplay = gs.getTimesToDisplay(displayWhite, MAX_MINUTES_PLAY)

    if gs.isGameOver(): return

    fontT = p.font.Font('freesansbold.ttf',40)

    #if not (gs.isAIEnabled and gs.isAIColorWhite):
    textT1 = fontT.render(timeToDisplay, False, p.Color("black"), None) #p.Color("white"))
    textRectT1 = textT1.get_rect()
    textRectT1.top = 50
    textRectT1.left = 615
    screen.blit(textT1, textRectT1)

    timeToDisplay = "00:00"
    displayWhite = False
    timeToDisplay = gs.getTimesToDisplay(displayWhite, MAX_MINUTES_PLAY)

    if gs.isGameOver(): return

    #if not (gs.isAIEnabled and not gs.isAIColorWhite):
    textT2 = fontT.render(timeToDisplay, False, p.Color("black"), None) #p.Color("white"))
    textRectT2 = textT2.get_rect()
    textRectT2.top = 50
    textRectT2.left = 765
    screen.blit(textT2, textRectT2)


'''
Draw green circle to highlight which player's turn it is
'''
def drawPlayerTurn(screen, drawWhite):
    #clear
    p.draw.circle(screen, p.Color("white"), (660, 220), 20)
    p.draw.circle(screen, p.Color("white"), (820,220), 20)
    fontSizeWhite = 35
    fontSizeBlack = 35
    colorWhite = p.Color("black")
    colorBlack = p.Color("light gray")

    # playerTurnCircleWhiteLeft = 660
    # playerTurnCircleWhiteTop = 220
    # playerTurnCircleBlackLeft = 820
    # playerTurnCircleBlackTop = 220
    #
    # playerTurnWhiteTop = 150
    # playerTurnWhiteLeft = 643
    # playerTurnBlackTop = 150
    # playerTurnBlackLeft = 807

    if drawWhite == True:
        p.draw.circle(screen, p.Color("green"), (PlayerTurnCircleWhiteLeft,PlayerTurnCircleWhiteTop), 20)
        p.draw.circle(screen, p.Color("light gray"), (PlayerTurnCircleBlackLeft,PlayerTurnCircleBlackTop), 10)
        # fontSizeWhite = 35
        # fontSizeBlack = 20
        colorWhite = p.Color("black")
        colorBlack = p.Color("light gray")
    else:
        p.draw.circle(screen, p.Color("light gray"), (PlayerTurnCircleWhiteLeft,PlayerTurnCircleWhiteTop), 10)
        p.draw.circle(screen, p.Color("green"), (PlayerTurnCircleBlackLeft,PlayerTurnCircleBlackTop), 20)
        # fontSizeWhite = 20
        # fontSizeBlack = 35
        colorWhite = p.Color("light gray")
        colorBlack = p.Color("black")

    fontWhite = p.font.Font('freesansbold.ttf',fontSizeWhite)
    text4 = fontWhite.render('W', drawWhite, colorWhite, p.Color("white"))
    textRect4 = text4.get_rect()
    textRect4.top = PlayerTurnWhiteTop #150
    textRect4.left = PlayerTurnWhiteLeft #643
    screen.blit(text4, textRect4)

    fontBlack = p.font.Font('freesansbold.ttf',fontSizeBlack)
    text5 = fontBlack.render('B', not drawWhite, colorBlack, p.Color("white"))
    textRect5 = text5.get_rect()
    textRect5.top = PlayerTurnBlackTop #150
    textRect5.left = PlayerTurnBlackLeft #807
    screen.blit(text5, textRect5)

'''
Draw pieces
'''
def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            #not empty
            if piece != '--' and piece != '':
                screen.blit(IMAGES[piece], p.Rect(col*SQUARE_SIZE+PADLEFT, row*SQUARE_SIZE+PADTOP, SQUARE_SIZE, SQUARE_SIZE))

def drawPieceSummary(screen, gs):
    summary = [
        ["bp", "bR", "bN", "bB", "bQ"],
        ["wp", "wR", "wN", "wB", "wQ"]]
    spacerTop = 20
    font = p.font.Font('freesansbold.ttf', 18)
    if len(gs.countedPieces) == 0:
        gs.countPieces()

    for row in range(2):
        for col in range(5):
            piece = summary[row][col]
            #not empty
            if piece != '--' and piece != '':
                if row == 0:
                    screen.blit(IMAGES[piece], p.Rect(col*SUMMARY_SQUARE_SIZE+SUMMARY_PADLEFT, row*SUMMARY_SQUARE_SIZE+SUMMARY_PADTOP, SUMMARY_SQUARE_SIZE, SUMMARY_SQUARE_SIZE))
                else:
                    screen.blit(IMAGES[piece], p.Rect(col*SUMMARY_SQUARE_SIZE+SUMMARY_PADLEFT, row*SUMMARY_SQUARE_SIZE+SUMMARY_PADTOP+spacerTop, SUMMARY_SQUARE_SIZE, SUMMARY_SQUARE_SIZE))

                pieceText = str( gs.countedPieces[piece] )

                text1 = font.render(pieceText, False, p.Color("black"), p.Color("white"))
                textRect1 = text1.get_rect()
                if row== 0:
                    textRect1.top = row*SUMMARY_SQUARE_SIZE+SUMMARY_PADTOP + 65
                else:
                    textRect1.top = row*SUMMARY_SQUARE_SIZE+SUMMARY_PADTOP+spacerTop + 65

                textRect1.left = col*SUMMARY_SQUARE_SIZE+SUMMARY_PADLEFT+30
                screen.blit(text1, textRect1)

'''
Draw the pawn promotion area
'''
def drawPawnPromotion(screen, gs):
    #Pawn Promotion
    if gs.hasPawnPromotion:
        colorPP = p.Color("black")
        if not gs.whiteToMove:
            pieces = ['','wR', 'wN', 'wB', 'wQ']
        else:
            pieces = ['','bR', 'bN', 'bB', 'bQ']
    else:
        colorPP = p.Color("light gray")
        pieces = ['', '', '', '', '']

    top = 320
    left = 630
    gs.drawnPawnPromotionLeft = left
    gs.drawnPawnPromotionTop = top
    #gs.pawnPromotionPieces = []

    #col = (location[0] - PADLEFT) // SQUARE_SIZE
    #row = (location[1] - PADTOP) // SQUARE_SIZE

    fontPP = p.font.Font('freesansbold.ttf',20)
    textPP = fontPP.render('Pawn Promotion', False, colorPP, p.Color("white"))
    textRectPP = textPP.get_rect()
    textRectPP.top = top
    textRectPP.left = left
    screen.blit(textPP, textRectPP)

    colorOdd = p.Color("light gray")
    colorEven = p.Color("gray")

    colors = [p.Color("light gray"), p.Color("gray")]
    num = 1
    while num < len(pieces):
        color = colors[((num) % 2)]
        if gs.hasPawnPromotion:
            p.draw.rect(screen, color, p.Rect(num*SQUARE_SIZE+(left-SQUARE_SIZE), 1*SQUARE_SIZE+(top+20-SQUARE_SIZE),
                                              SQUARE_SIZE, SQUARE_SIZE))
            if len(pieces) != 0:
                screen.blit(IMAGES[pieces[num]],p.Rect(num * SQUARE_SIZE + (left-SQUARE_SIZE),
                                                       1 * SQUARE_SIZE + (top+20 - SQUARE_SIZE),
                                                       SQUARE_SIZE, SQUARE_SIZE))
                if len(gs.pawnPromotionPieces) <= len(pieces[num])+1:
                    gs.pawnPromotionPieces.append(pieces[num])
                #screen.blit(IMAGES['wR'],p.Rect(1 * SQUARE_SIZE + PADLEFT, 1 * SQUARE_SIZE + PADTOP, SQUARE_SIZE, SQUARE_SIZE))
        else:
            if len(gs.pawnPromotionPieces) != 0:
                pawnPiece = gs.pawnPromotionPieces.pop()

            p.draw.rect(screen, p.Color("white"), p.Rect(num*SQUARE_SIZE+(left-SQUARE_SIZE), 1*SQUARE_SIZE+(top+20-SQUARE_SIZE), SQUARE_SIZE, SQUARE_SIZE))

                #screen.blit(IMAGES['wp'],
                #            p.Rect(num * SQUARE_SIZE + (left - SQUARE_SIZE), 1 * SQUARE_SIZE + (top + 20 - SQUARE_SIZE),
                #                   SQUARE_SIZE, SQUARE_SIZE))
                #p.draw.rect(screen, colorPP, p.Rect(num*SQUARE_SIZE+(left-SQUARE_SIZE), 1*SQUARE_SIZE+(top+20-SQUARE_SIZE), SQUARE_SIZE, SQUARE_SIZE))
                #p.draw.rect(screen, p.Color("white"), p.Rect(num*SQUARE_SIZE+630, 1*SQUARE_SIZE+340, SQUARE_SIZE, SQUARE_SIZE))

        num = num + 1

    p.draw.line(screen, p.Color("black"), ((DIMENSION * SQUARE_SIZE) + PADLEFT + PADLEFT + 10, 430), (WIDTH, 430), 2)

'''
Draw available player level
'''
def drawPlayerLevels(screen, gs):
    #p.draw.circle(screen, p.Color("green"), (660, 220), 20)
    #p.draw.circle(screen, p.Color("light gray"), (820, 220), 10)

    circlePaddingLeft = 10
    circlePaddingTop = 8

    font = p.font.Font('freesansbold.ttf',18)
    text1 = font.render('Beginner', False, p.Color("black"), p.Color("white"))
    textRect1 = text1.get_rect()
    textRect1.top = OptionBeginnerTop #440
    textRect1.left = OptionBeginnerLeft #630
    screen.blit(text1, textRect1)
    p.draw.circle(screen, p.Color("light gray"), (OptionBeginnerLeft-circlePaddingLeft, OptionBeginnerTop+circlePaddingTop), 10)
    if gs.isOptionBeginner:
        p.draw.circle(screen, p.Color("blue"), (OptionBeginnerLeft - circlePaddingLeft, OptionBeginnerTop + circlePaddingTop),
                      10)

    text2 = font.render('Intermediate', False, p.Color("black"), p.Color("white"))
    textRect2 = text2.get_rect()
    textRect2.top = OptionIntermediateTop #460
    textRect2.left = OptionIntermediateLeft #630
    screen.blit(text2, textRect2)
    p.draw.circle(screen, p.Color("light gray"), (OptionIntermediateLeft-circlePaddingLeft, OptionIntermediateTop+circlePaddingTop), 10)
    if gs.isOptionIntermediate:
        p.draw.circle(screen, p.Color("blue"), (OptionIntermediateLeft - circlePaddingLeft, OptionIntermediateTop + circlePaddingTop),
                      10)

    text3 = font.render('Advanced', False, p.Color("black"), p.Color("white"))
    textRect3 = text3.get_rect()
    textRect3.top = OptionAdvancedTop #480
    textRect3.left = OptionAdvancedLeft #630
    screen.blit(text3, textRect3)
    p.draw.circle(screen, p.Color("light gray"), (OptionAdvancedLeft-circlePaddingLeft, OptionAdvancedTop+circlePaddingTop), 10)
    if gs.isOptionAdvanced:
        p.draw.circle(screen, p.Color("blue"), (OptionAdvancedLeft - circlePaddingLeft, OptionAdvancedTop + circlePaddingTop),
                      10)

    text4 = font.render('None', False, p.Color("black"), p.Color("white"))
    textRect4 = text4.get_rect()
    textRect4.top = OptionNoneTop #440
    textRect4.left = OptionNoneLeft #800
    screen.blit(text4, textRect4)
    p.draw.circle(screen, p.Color("light gray"), (OptionNoneLeft-circlePaddingLeft, OptionNoneTop+circlePaddingTop), 10)
    if gs.isOptionNone:
        p.draw.circle(screen, p.Color("blue"), (OptionNoneLeft - circlePaddingLeft, OptionNoneTop + circlePaddingTop),
                      10)

    text5 = font.render('Intermediate+', False, p.Color("black"), p.Color("white"))
    textRect5 = text5.get_rect()
    textRect5.top = OptionIntermediatePlusTop #440
    textRect5.left = OptionIntermediatePlusLeft #800
    screen.blit(text5, textRect5)
    p.draw.circle(screen, p.Color("light gray"), (OptionIntermediatePlusLeft-circlePaddingLeft, OptionIntermediatePlusTop +circlePaddingTop), 10)
    if gs.isOptionIntermediatePlus:
        p.draw.circle(screen, p.Color("blue"), (OptionIntermediatePlusLeft - circlePaddingLeft, OptionIntermediatePlusTop + circlePaddingTop),
                      10)

    text6 = font.render('Advanced+', False, p.Color("black"), p.Color("white"))
    textRect6 = text6.get_rect()
    textRect6.top = OptionAdvancedPlusTop #440
    textRect6.left = OptionAdvancedPlusLeft #770
    screen.blit(text6, textRect6)
    p.draw.circle(screen, p.Color("light gray"), (OptionAdvancedPlusLeft-circlePaddingLeft, OptionAdvancedPlusTop +circlePaddingTop), 10)
    if gs.isOptionAdvancedPlus:
        p.draw.circle(screen, p.Color("blue"), (OptionAdvancedPlusLeft - circlePaddingLeft, OptionAdvancedPlusTop + circlePaddingTop),
                      10)

    p.draw.line(screen, p.Color("black"), ((DIMENSION * SQUARE_SIZE) + PADLEFT + PADLEFT + 10, 500), (WIDTH, 500), 2)

'''
Draw player options
'''
def drawOptions(screen, gs):
    font = p.font.Font('freesansbold.ttf', 18)

    screen.blit(IMAGES['button1'], p.Rect(ButtonUndoLeft-20,
                                            ButtonUndoTop-2,
                                            500, 500))

    textU = font.render('Undo', False, p.Color("black"), None)#p.Color("light grey"))
    textRectU = textU.get_rect()
    textRectU.top = ButtonUndoTop #515
    textRectU.left = ButtonUndoLeft+20 #630
    screen.blit(textU, textRectU)

    screen.blit(IMAGES['button1'], p.Rect(ButtonSuggestionLeft-20,
                                            ButtonSuggestionTop-2,
                                            500, 500))

    textS = font.render('Suggestion', False, p.Color("black"), None)#p.Color("light grey"))
    textRectS = textS.get_rect()
    textRectS.top = ButtonSuggestionTop #545
    textRectS.left = ButtonSuggestionLeft-5 #630
    screen.blit(textS, textRectS)

    screen.blit(IMAGES['button1'], p.Rect(ButtonLoadLeft-20,
                                            ButtonLoadTop-2,
                                            500, 500))

    textL = font.render('Load', False, p.Color("black"), None)#p.Color("light grey"))
    textRectL = textL.get_rect()
    textRectL.top = ButtonLoadTop #510
    textRectL.left = ButtonLoadLeft+20 #800
    screen.blit(textL, textRectL)

    screen.blit(IMAGES['button1'], p.Rect(ButtonSaveLeft-20,
                                            ButtonSaveTop-2,
                                            500, 500))

    textSa = font.render('Save', False, p.Color("black"), None)#p.Color("light grey"))
    textRectSa = textSa.get_rect()
    textRectSa.top = ButtonSaveTop #535
    textRectSa.left = ButtonSaveLeft+20 #800
    screen.blit(textSa, textRectSa)

    screen.blit(IMAGES['button1'], p.Rect(ButtonResetLeft-20,
                                            ButtonResetTop-2,
                                            500, 500))

    textSa = font.render('Reset', False, p.Color("black"), None)#p.Color("light grey"))
    textRectSa = textSa.get_rect()
    textRectSa.top = ButtonResetTop #560
    textRectSa.left = ButtonResetLeft+20 #800
    screen.blit(textSa, textRectSa)

    textEA = font.render('Enable AI', False, p.Color("black"), p.Color("white"))
    textRectEA = textEA.get_rect()
    textRectEA.top = ButtonEnableAITop
    textRectEA.left = ButtonEnableAILeft
    screen.blit(textEA, textRectEA)

    circlePaddingLeft = 10
    circlePaddingTop = 8

    p.draw.circle(screen, p.Color("light gray"), (ButtonEnableAILeft-circlePaddingLeft, ButtonEnableAITop+circlePaddingTop), 10)
    if gs.isAIEnabled:
        p.draw.circle(screen, p.Color("blue"), (ButtonEnableAILeft - circlePaddingLeft, ButtonEnableAITop + circlePaddingTop),
                      10)

    textEAC = font.render('AI uses White', False, p.Color("black"), p.Color("white"))
    textRectEAC = textEAC.get_rect()
    textRectEAC.top = ButtonColorAITop
    textRectEAC.left = ButtonColorAILeft
    screen.blit(textEAC, textRectEAC)

    p.draw.circle(screen, p.Color("light gray"), (ButtonColorAILeft-circlePaddingLeft, ButtonColorAITop+circlePaddingTop), 10)
    if gs.isAIColorWhite:
        p.draw.circle(screen, p.Color("blue"), (ButtonColorAILeft-circlePaddingLeft, ButtonColorAITop+circlePaddingTop), 10)

    #AI Line
    p.draw.line(screen, p.Color("black"), ((DIMENSION * SQUARE_SIZE) + PADLEFT + PADLEFT + 10, ButtonEnableAITop+30), (WIDTH, ButtonEnableAITop+30), 2)

'''
Draw available move options
'''
def drawPossibleOptions(screen, gs, sqSelected, validmoves):
    selected = p.Color("light blue")

    #if beginner or intermediate

    if len(validmoves) > 0 and len(sqSelected) > 0:
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                for i in range(len(validmoves)):
                    move = validmoves[i]
                    if sqSelected == (move.startRow, move.startCol) and (row,col) == (move.endRow,move.endCol):

                        p.draw.rect(screen, selected, p.Rect(col*SQUARE_SIZE+PADLEFT+(SQUARE_SIZE/2)-((SQUARE_SIZE/4)/2),
                                                             row*SQUARE_SIZE+PADTOP+(SQUARE_SIZE/2)-((SQUARE_SIZE/4)/2),
                                                             SQUARE_SIZE/4, SQUARE_SIZE/4))

'''
Draw available move options
'''
def drawPossibleSuggestions(screen, gs, sqSelected, validmoves):
    selected = p.Color("light blue")

    #if beginner or intermediate

    if len(validmoves) > 0 and len(sqSelected) > 0:
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                for i in range(len(validmoves)):
                    move = validmoves[i]
                    if sqSelected == (move.startRow, move.startCol) and (row,col) == (move.endRow,move.endCol):

                        p.draw.rect(screen, selected, p.Rect(col*SQUARE_SIZE+PADLEFT+(SQUARE_SIZE/2)-((SQUARE_SIZE/4)/2),
                                                             row*SQUARE_SIZE+PADTOP+(SQUARE_SIZE/2)-((SQUARE_SIZE/4)/2),
                                                             SQUARE_SIZE/4, SQUARE_SIZE/4))



def drawGameOver(screen, gs):
    if gs.isGameOver(): #gs.isInCheckMate or gs.isInStaleMate or gs.timeHasExpired:
        font = p.font.Font('freesansbold.ttf',20)
        color = p.Color("black")
        if not gs.whiteToMove:
            color = p.Color("green")
        else:
            color = p.Color("red")

        if gs.isInStaleMate:
            text = 'Game Over - Stalemate'
        elif gs.isInCheckMate:
            text = 'Game Over - Checkmate'
        elif gs.timeHasExpired:
            text = 'Game Over - Time Has Expired'

        textU = font.render(text, False, color, p.Color("white"))
        textRectU = textU.get_rect()
        textRectU.top = ((DIMENSION*SQUARE_SIZE)/2)+PADTOP             #515
        textRectU.left = ((DIMENSION*SQUARE_SIZE)/2)+PADLEFT-len(text) #630
        screen.blit(textU, textRectU)

        fontWin = p.font.Font('freesansbold.ttf',21)
        textWin = fontWin.render('Winner', False, p.Color("green"), p.Color("white"))
        textRectWin = textWin.get_rect()

        if not gs.whiteToMove:
            textRectWin.top = PlayerTurnCircleWhiteTop + 30
            textRectWin.left = PlayerTurnCircleWhiteLeft - 40
        else:
            textRectWin.top = PlayerTurnCircleBlackTop + 30
            textRectWin.left = PlayerTurnCircleBlackLeft - 40

        screen.blit(textWin, textRectWin)

def saveToFile(gs):
    import tkinter as tk
    from tkinter import filedialog

    filetypes = (
        ('Chess files', '*.chess'),
        ('All files', '*.*'),
    )

    # open-file dialog
    #fileName = "files//"+str(datetime.datetime.now().strftime("%Y %m %d %H %M %S")) + ".chess"
    fileName = str(datetime.datetime.now().strftime("%Y %m %d %H %M %S")) + ".chess"
    root = tk.Tk()
    # fileName = tk.filedialog.askopenfilename(
    #     title='Select a file to save...',
    #     filetypes=filetypes,
    #     initialdir='files',
    #     initialfile=fileName
    # )
    fileName = tk.filedialog.asksaveasfilename(
        title='Select a file to save...',
        filetypes=filetypes,
        initialdir='files',
        initialfile=fileName
    )
    root.destroy()

    #fileName = "files//"+str(datetime.datetime.now().strftime("%Y %m %d %H %M %S")) + ".chess"
    # print("Now: " + str(new_datetime) + " More:" + new_datetime.strftime("%M:%S"))
    f = open(fileName, "w")

    for row in range(DIMENSION):
        pieceString = ""
        for col in range(DIMENSION):
            piece = "--" if gs.board[row][col] == "" or gs.board[row][col] == " " else gs.board[row][col]
            pieceString += " " + piece

        f.writelines("{}\n".format(pieceString))

    #f.write(str(gs.board))
    f.close()

    print("File saved: " + fileName)

def loadFromFile(gs):
    import tkinter as tk
    from tkinter import filedialog

    filetypes = (
        ('Chess files', '*.chess'),
        ('All files', '*.*'),
    )

    # open-file dialog
    root = tk.Tk()
    fileName = tk.filedialog.askopenfilename(
        title='Select a file to load...',
        filetypes=filetypes,
        initialdir='files',
    )
    root.destroy()
    print("File loaded: " + fileName)

    myFile = open(fileName,'r')

    #ips = {}
    row = 0
    col = 0

    for line in myFile:
        parts = line.split()
        print("row:" + str(row) + " parts:" + str(parts))
        for part in parts:
            print("row:" +str(row) + " col:" +str(col)+ " part:" + part)
            gs.board[row][col] = part

            col += 1
            if col > DIMENSION-1:
                col = 0
                row += 1
        # if parts[1] == 'Failure':
        #     ips.setdefault(parts[0], 0)
        #     ips[parts[0]] += 1

    myFile.close()
    print("File loaded: " + fileName)


if __name__ == "__main__":
    main()