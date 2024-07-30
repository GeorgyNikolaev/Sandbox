import random
import numpy as np
import pygame

# Инициализация PyGame.
pygame.init()

# Определение цветов
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Установка размеров окна
width = 600
height = 400
window = pygame.display.set_mode((width, height))

# Настройка игры
pygame.display.set_caption('Песочница')

clock = pygame.time.Clock()
base_block = 10
speed = 15

def draw_screen(base, list):
    for x in range(len(list)):
        for y in range(len(list[0])):
            pygame.draw.rect(window, list[x][y], [x * base, y * base, base, base])

def fall_move(pos, array, a, b, isRight):
    if isRight:
        array[pos[0]+1][pos[1]+1] = a
        array[pos[0]][pos[1]] = b
    else:
        array[pos[0]-1][pos[1]+1] = a
        array[pos[0]][pos[1]] = b


def game_loop():
    game_close = False
    isTouch = False

    window.fill(black)
    mapNow = np.zeros((width // base_block, height // base_block, 3)).astype(int)
    mapNext = mapNow.copy()

    pygame.display.update()

    while not game_close:

        for i in pygame.event.get():
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_q:
                    game_close = True
            if i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    isTouch = True
            if i.type == pygame.MOUSEBUTTONUP:
                if i.button == 1:
                    isTouch = False

        if isTouch:
            pos = pygame.mouse.get_pos()
            if 0 <= pos[0] < width and 0 <= pos[1] < height:
                mapNext[pos[0] // base_block][pos[1] // base_block] = white

        change_down = []
        for i, Xline in enumerate(mapNow):
            for j, item in enumerate(Xline):
                if not np.allclose(item, black) and j < height // base_block - 1:
                    if not np.allclose(item, mapNow[i][j+1]):
                        mapNext[i][j+1] = item
                        mapNext[i][j] = black
                    elif i == 0 and np.allclose(black, mapNow[1][j+1]):
                        fall_move([i, j], mapNext, item, black, True)
                    elif i == width//base_block-1 and np.allclose(black, mapNow[width//base_block-2][j+1]):
                        fall_move([i, j], mapNext, item, black, False)
                    elif 0 < i < width // base_block - 1:
                        right = np.allclose(item, mapNow[i+1][j+1])
                        left = np.allclose(item, mapNow[i-1][j+1])
                        if right and not left:
                            fall_move([i, j], mapNext, item, black, False)
                        elif not right and left:
                            fall_move([i, j], mapNext, item, black, True)
                        elif not right and not left:
                            if random.randrange(0, 1) > 0.5:
                                fall_move([i, j], mapNext, item, black, True)
                            else:
                                fall_move([i, j], mapNext, item, black, False)


        draw_screen(base_block, mapNext)
        mapNow = mapNext.copy()
        pygame.display.update()

        pygame.time.delay(0)

    pygame.quit()
    quit()


game_loop()
