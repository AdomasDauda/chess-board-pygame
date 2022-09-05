import pygame
from chessboard import *

class Mouse():
    def __init__(self):
        self.mouse_pos = self.getMousePos()
        self.mouse_grid = self.getMouseGrid()
    
    def getMouseGrid(self):
        self.getMousePos()
        self.mouse_grid = int(self.mouse_pos[0]/128), int(self.mouse_pos[1]/128)
        return self.mouse_grid

    def getMousePos(self):
        self.mouse_pos = pygame.mouse.get_pos()
        return self.mouse_pos