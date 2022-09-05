from copy import copy
import pygame
from mouse import *

class Chessboar():
    def __init__(self):
        self.peaces={
            0:'empty',
            1:'pawn',
            2:'rook',
            3:'knight',
            4:'bishop',
            5:'queen',
            6:'king'
        }

        # my chessboar syntax will be 8x8 grid where if there is a peace it will be [chesspeace(empty=0), color]

        # IN ONE GRID FIRST NUMBER = PEACE SECOND NUMBER = COLOR
        self.default_chessboard_grid = [[1,0,1,0,1,0,1,0],[0,1,0,1,0,1,0,1],[1,0,1,0,1,0,1,0],[0,1,0,1,0,1,0,1],[1,0,1,0,1,0,1,0],[0,1,0,1,0,1,0,1],[1,0,1,0,1,0,1,0],[0,1,0,1,0,1,0,1]]
        self.default_peace_configuration = [[[0,0]]*8,[[1,0]]*8, [[0,0]]*8, [[0,0]]*8, [[0,0]]*8, [[0,0]]*8, [[1,1]]*8, [[0,0]]*8]
        self.square_size = 128
        # [[[2,0],[3,0],[4,0],[5,0],[6,0],[4,0],[3,0],[2,0]], [[1,0]]*8, [[0]]*8, [[0]]*8, [[0]]*8, [[0]]*8, [[1,1]]*8, [[2,1],[3,1],[4,1],[5,1],[6,1],[4,1],[3,1],[2,1]]]
        self.icon_size = (128,128)
        self.refreshPeaceModels()

        self.all_moves=  [[[[2,0], [1,0],[1,1], [1,-1]], [[-2,0], [-1,0],[-1,-1], [-1,1]]], # pawn first is white second is black     FORMAT IS Y, X
                                [[1,0], [2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7]]
                               ]  # first number is x second number is y

    def refreshPeaceModels(self):
        self.black_peaces = []
        self.white_peaces = []

        #pawn
        self.black_peaces.append(pygame.transform.scale(pygame.image.load('images/black_pawn.png'), self.icon_size))
        self.white_peaces.append(pygame.transform.scale(pygame.image.load('images/white_pawn.png'), self.icon_size))

        #rook
        self.black_peaces.append(pygame.transform.scale(pygame.image.load('images/black_rook.png'), self.icon_size))
        self.white_peaces.append(pygame.transform.scale(pygame.image.load('images/white_rook.png'), self.icon_size))

        #knight
        self.black_peaces.append(pygame.transform.scale(pygame.image.load('images/black_knight.png'), self.icon_size))
        self.white_peaces.append(pygame.transform.scale(pygame.image.load('images/white_knight.png'), self.icon_size))
        
        #bishop
        self.black_peaces.append(pygame.transform.scale(pygame.image.load('images/black_bishop.png'), self.icon_size))
        self.white_peaces.append(pygame.transform.scale(pygame.image.load('images/white_bishop.png'), self.icon_size))

        #queen
        self.black_peaces.append(pygame.transform.scale(pygame.image.load('images/black_queen.png'), self.icon_size))
        self.white_peaces.append(pygame.transform.scale(pygame.image.load('images/white_queen.png'), self.icon_size))

        #king
        self.black_peaces.append(pygame.transform.scale(pygame.image.load('images/black_king.png'), self.icon_size))
        self.white_peaces.append(pygame.transform.scale(pygame.image.load('images/white_king.png'), self.icon_size))


    def drawChessboard(self, surfrace, chessboard):
        y=0
        for row in chessboard:
            x=0
            for item in row:
                if item == 0:
                    rect = pygame.Rect(x*self.square_size,y*self.square_size,self.square_size,self.square_size)
                    pygame.draw.rect(surfrace, [100,100,100], rect, 100)
                if item == 1:
                    rect = pygame.Rect(x*self.square_size,y*self.square_size,self.square_size,self.square_size)
                    pygame.draw.rect(surfrace, [255,255,255,50], rect, 100)
                if item == 2:
                    rect = pygame.Rect(x*self.square_size,y*self.square_size,self.square_size,self.square_size)
                    pygame.draw.rect(surfrace, [255,0,0, 50], rect, 100)
                if item == 3:
                    rect = pygame.Rect(x*self.square_size,y*self.square_size,self.square_size,self.square_size)
                    pygame.draw.rect(surfrace, [0,255,0, 50], rect, 100)
                x+=1
            y+=1

    def drawPeaces(self, surface, peace_config):
        y=0
        for row in peace_config:
            x=0
            for peace in row:
                if peace[0] != 0:
                    peace_type, color = peace[0], peace[1]
                    if color == 0:
                        surface.blit(self.black_peaces[peace_type-1],(x,y))#,special_flags=pygame.BLEND_RGBA_MULT)
                    if color == 1:
                        surface.blit(self.white_peaces[peace_type-1],(x,y))#,special_flags=pygame.BLEND_RGBA_MULT)
                x+=self.square_size
            y+=self.square_size


    def findAvalableMoves(self, peace, peaceyx, chessboard_grid, peace_config):
        available_moves=[]
        self.all_moves = self.restoreAvailableMovesList()


        if peace[0] == 1: # if its a pawn
            if peaceyx[0]+1 in range(3,7) and peace[1] == 0:
                self.all_moves[0][0].pop(0)    
                
            if peaceyx[0]+1 in range(0,7) and peace[1] == 1:
                self.all_moves[0][1].pop(0)

            if peace[1] == 0: # if its black
                for move in self.all_moves[0][0]: #[0][0] is black pawn
                    try: # first is to check if its empty because then to check if the move is diagonal then we check if its not our team color
                        if peace_config[peaceyx[0]+move[0]][peaceyx[1]+move[1]][0] != 0 and move in self.restoreAvailableMovesList()[0][0][2:4] and peaceyx[1]+move[1] != -1 and peace_config[peaceyx[0]+move[0]][peaceyx[1]+move[1]][1] != 0:  # i want the second color to be 1
                            chessboard_grid[peaceyx[0]+move[0]][peaceyx[1]+move[1]] = 2 # 2 ir red
                            available_moves.append([peaceyx[0]+move[0],peaceyx[1]+move[1]])
                            
                        if peace_config[peaceyx[0]+move[0]][peaceyx[1]+move[1]][0] == 0 and move in self.restoreAvailableMovesList()[0][0][0:2] and peaceyx[0]+move[0] != 8: # this defines the forward motion
                            chessboard_grid[peaceyx[0]+move[0]][peaceyx[1]+move[1]] = 3 # 3 is green
                            available_moves.append([peaceyx[0]+move[0],peaceyx[1]+move[1]])
                    except IndexError:
                        pass # we dont display it if its off the baord



            if peace[1] == 1: # if its white
                for move in self.all_moves[0][1]: # [0][0] is white pawn
                    try: # first is to check if its empty because then to check if the move is diagonal then we check if its not our team color
                        if peace_config[peaceyx[0]+move[0]][peaceyx[1]+move[1]][0] != 0 and move in self.restoreAvailableMovesList()[0][1][2:4] and peaceyx[1]+move[1] != -1 and peace_config[peaceyx[0]+move[0]][peaceyx[1]+move[1]][1] != 1:
                            chessboard_grid[peaceyx[0]+move[0]][peaceyx[1]+move[1]] = 2
                            available_moves.append([peaceyx[0]+move[0],peaceyx[1]+move[1]])

                        if peace_config[peaceyx[0]+move[0]][peaceyx[1]+move[1]][0] == 0 and move in self.restoreAvailableMovesList()[0][1][0:2] and peaceyx[0]+move[0] != -1:
                            chessboard_grid[peaceyx[0]+move[0]][peaceyx[1]+move[1]] = 3
                            available_moves.append([peaceyx[0]+move[0],peaceyx[1]+move[1]])

                    except IndexError:
                        pass # we just dont display it if its off the board
            
            
        return chessboard_grid, available_moves

    def restoreAvailableMovesList(self):
        return [[[[2,0], [1,0],[1,1], [1,-1]], [[-2,0], [-1,0],[-1,-1], [-1,1]]], # pawn first is white second is black     FORMAT IS Y, X
                            [[1,0], [2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7]]
                           ]

    def removePeace(self, peace_config, peace1yx, peace2yx): # this is for removing peaces
        if peace_config[peace1yx[0]][peace1yx[1]] != [0,0]:
            if peace2yx[0] == 7 or peace2yx[0] == 0 and peace_config[peace1yx[0]][peace1yx[1]][0] == 1: # check if its on the last row and its a pawn
                peace_config[peace1yx[0]][peace1yx[1]], peace_config[peace2yx[0]][peace2yx[1]] = [5,peace_config[peace1yx[0]][peace1yx[1]][1]],[0,0]
            peace_config[peace1yx[0]][peace1yx[1]], peace_config[peace2yx[0]][peace2yx[1]] = peace_config[peace2yx[0]][peace2yx[1]], peace_config[peace1yx[0]][peace1yx[1]] # swap peaces
            peace_config[peace1yx[0]][peace1yx[1]] = [0,0] # remove the second peace
            print(f'{peace1yx}({peace_config[peace1yx[0]][peace1yx[1]]}) took {peace2yx}({peace_config[peace2yx[0]][peace2yx[1]]})')
        return peace_config

    def swapPeaces(self, peace_config, peace1yx, peace2yx): # this is for moving peaces
        if peace_config[peace1yx[0]][peace1yx[1]] != [0,0]:
            if peace2yx[0] == 7 or peace2yx[0] == 0 and peace_config[peace1yx[0]][peace1yx[1]][0] == 1: # check if its on the last row and its a pawn
                peace_config[peace1yx[0]][peace1yx[1]], peace_config[peace2yx[0]][peace2yx[1]] = [5,peace_config[peace1yx[0]][peace1yx[1]][1]],[0,0]
            peace_config[peace1yx[0]][peace1yx[1]], peace_config[peace2yx[0]][peace2yx[1]] = peace_config[peace2yx[0]][peace2yx[1]], peace_config[peace1yx[0]][peace1yx[1]]
            print(f'{peace1yx}({peace_config[peace1yx[0]][peace1yx[1]]}) moved to {peace2yx}({peace_config[peace2yx[0]][peace2yx[1]]})')
        return peace_config


    def restoreDefaultPeaceConfiguration(self):
        return [[[0,0]]*8,[[1,0]]*8, [[0,0]]*8, [[0,0]]*8, [[0,0]]*8, [[0,0]]*8, [[1,1]]*8, [[0,0]]*8]


    def restoreChessboardGrid(self):
        return [[1,0,1,0,1,0,1,0],[0,1,0,1,0,1,0,1],[1,0,1,0,1,0,1,0],[0,1,0,1,0,1,0,1],[1,0,1,0,1,0,1,0],[0,1,0,1,0,1,0,1],[1,0,1,0,1,0,1,0],[0,1,0,1,0,1,0,1]]




chess=Chessboar()
print('peace_config:\n')
for i in chess.default_peace_configuration:
    row=[]
    for j in i:
        row.append(chess.peaces.get(j[0]))
    print(row)