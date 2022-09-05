from chessboard import *
from mouse import *
import pygame
import time


def main():

    chess = Chessboar()

    pygame.init()
    clock = pygame.time.Clock()
    display = pygame.display.set_mode((1024,1024))
    chessboard = chess.default_chessboard_grid
    peace_config = chess.default_peace_configuration

    peace1yx = []
    peace2yx = []

    mouse = Mouse()
    #driver code
    while True:

        display.fill([255,255,255])
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    print('refreshing models')
                    chess.refreshPeaceModels()
                if event.key == pygame.K_q:
                    peace_config = chess.restoreDefaultPeaceConfiguration()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:

                if len(peace1yx) == 0:
                    last_peace_config = peace_config
                    peace1yx.append(mouse.getMouseGrid()[1])
                    peace1yx.append(mouse.getMouseGrid()[0])



            if event.type == pygame.MOUSEBUTTONUP:
                if len(peace2yx) == 0:
                    peace2yx.append(mouse.getMouseGrid()[1])
                    peace2yx.append(mouse.getMouseGrid()[0])
                if peace2yx in available_moves:
                    peace_config = chess.removePeace(peace_config, peace1yx, peace2yx)
                if peace2yx not in available_moves:
                    print('invalid move')
                    print(available_moves, peace1yx, 'tried to move to:', peace2yx)
                    peace_config = last_peace_config
                peace1yx = []
                peace2yx = []

        chess.drawChessboard(display, chessboard)


        if peace1yx != []:
            peace = peace_config[peace1yx[0]][peace1yx[1]]
            icon_size = chess.icon_size[0]
            chessboard, available_moves = chess.findAvalableMoves(peace, peace1yx, chessboard, peace_config)
            try:
                if peace[0] != 0:
                    if peace[1] == 1:
                        display.blit(chess.white_peaces[peace[0]-1], [mouse.getMousePos()[0]-icon_size/2,mouse.getMousePos()[1]-icon_size/2])
                    if peace[1] == 0:
                        display.blit(chess.black_peaces[peace[0]-1], [mouse.getMousePos()[0]-icon_size/2,mouse.getMousePos()[1]-icon_size/2])
            except IndexError:
                print(f'{peace1yx} is empty')

        if peace1yx == []:
            chessboard = chess.restoreChessboardGrid()


        chess.drawPeaces(display,peace_config)

        pygame.display.update()



if __name__ == '__main__':
    main()

