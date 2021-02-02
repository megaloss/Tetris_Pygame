import pygame
import random
import numpy as np
pygame.init()
WIDTH = 400
HEIGHT = 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("comicsans", 30, True)
font_end = pygame.font.SysFont("comicsans", 50, True)
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
# size of a block
width = 19
height = 19
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 0, 255)


class Block:

    SHAPES = [[[1, 1, 1, 1]],
              [[0, 1, 0],
               [1, 1, 1]],
              [[1, 0, 0],
               [1, 1, 1]],
              [[0, 0, 1],
               [1, 1, 1]],
              [[1, 1],
               [1, 1]],
              [[0, 1],
               [1, 1],
               [1, 0]],
              [[1, 0],
               [1, 1],
               [0, 1]]]

    def __init__(self):
        self.shape = np.array(random.choice(self.SHAPES))
        self.x = 10
        self.y = 2
        self.frozen = False
        self.color = random.choice([RED, BLUE, GREEN, YELLOW])

    def get_width(self):
        return len(self.shape[0])

    def get_height(self):
        return len(self.shape)

    def freeze(self, frozen_list):
        res = ''
        self.frozen = True
        if self.y-self.get_height() < 3:
            res = 'You loose !'
            return 0, res
        for y, line in enumerate(self.shape):
            for x, block in enumerate(line):
                if block:
                    frozen_list[self.y+y][self.x+x] = self.color
        score = check_frozen(frozen_list)
        return score, res

    def rotate(self, frozen_list):
        self.shape = np.rot90(self.shape)
        x = self.x
        y = self.y
        if self.get_width() > 3:
            self.x -= 1
            self.y += 1
        elif self.get_width() < 2:
            self.x += 1
            self.y -= 1
        if self.x+self.get_width() > 17:
            self.shape = np.rot90(self.shape, -1)
            self.x = x
            self.y = y
        if self.x < 1:
            self.shape = np.rot90(self.shape, -1)
            self.x = x
            self.y = y


def move(block, frozen_list):
    if block.y+block.get_height() > 27:
        score, res = block.freeze(frozen_list)
        return True, score, res
    for y, line in enumerate(block.shape):
        for x, brick in enumerate(line):
            if brick and (255 in frozen_list[block.y+y+1][block.x+x]):
                score, res = block.freeze(frozen_list)
                return True, score, res

    block.y += 1
    return False, 0, ''


def move_left(block, frozen_list):
    if block.x < 2:
        return False
    for y, line in enumerate(block.shape):
        for x, brick in enumerate(line):
            if brick and (255 in frozen_list[block.y+y][block.x+x-1]):
                return False
    return True


def move_right(block, frozen_list):
    if block.x+block.get_width() > 17:
        return False
    for y, line in enumerate(block.shape):
        for x, brick in enumerate(line):
            if brick and (255 in frozen_list[block.y+y][block.x+x+1]):
                return False
    return True


def check_frozen(frozen_list):
    score, double = 0, 0
    for y in range(len(frozen_list)):
        for i in range(1, len(frozen_list[y])):
            if np.all(frozen_list[y][i] == 0):
                break
        else:
            double += 1
            score += 17*double

            frozen_list[1:y+1] = frozen_list[0:y].copy()
    return score


def end_of_game(text):
    # print text and wait 3 sec
    text = font_end.render(str(text), 1, (200, 100, 100))
    win.blit(text, (30, 300))
    pygame.display.update()
    pygame.time.delay(3000)


def redraw(block, score, frozen_list):
    # clear screen
    win.fill((0, 0, 0))

    # draw the game boarders
    pygame.draw.rect(win, (155, 155, 155), (0, 0, WIDTH-20, HEIGHT-20), 20)

    def draw_block(block):
        for y, shape_line in enumerate(block.shape):
            for x, part in enumerate(shape_line):
                if part:
                    pygame.draw.rect(win, block.color, ((block.x+x)*20, (block.y+y)*20, width, height), 0)

    for y, line in enumerate(frozen_list):
        for x, frozen_block in enumerate(line):
            if 255 in frozen_block:
                pygame.draw.rect(win, frozen_block, (x * 20, y * 20, width, height), 0)

    draw_block(block)

    # print score
    text = font.render("Score: " + str(score), 1, (100, 100, 200))
    win.blit(text, (90, 10))
    # update screen
    pygame.display.update()


def main():
    run = True
    score = 0
    # starting position and direction
    frozen_list = np.zeros((28, 18, 3), dtype='uint8')
    block = Block()
    # res = ''
    while run:
        clock.tick(5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and move_left(block, frozen_list):
                    block.x -= 1
                if event.key == pygame.K_RIGHT and move_right(block, frozen_list):
                    block.x += 1
                if event.key == pygame.K_UP:
                    block.rotate(frozen_list)
                if event.key == pygame.K_DOWN and block.y+block.get_height() < 28:
                    block.y += 1

                if event.key == pygame.K_SPACE:
                    block.freeze(frozen_list)

                if event.key == pygame.K_q:
                    pygame.quit()
        # move block
        ev, delta_score, res = move(block, frozen_list)
        if ev:
            block = Block()
            score += delta_score
        # draw screen
        redraw(block, score, frozen_list)
        # end game if we got a signal
        if res:
            end_of_game(res)
            run = False

    main()


main()
