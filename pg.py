from random import random
import pygame as pg
import copy


LIFE = 1
DEATH = 0

class App:
    def __init__(self):
        self.res = self.width, self.height = (800, 450)
        self.screen = pg.display.set_mode(self.res, pg.SCALED)
        self.clock = pg.time.Clock()
        self.TILE = 2
        self.cols, self.rows = self.width // self.TILE, self.height // self.TILE
        self.grid = [[1 if random() < 0.08 else 0 for col in range(self.cols)] for row in range(self.rows)]
        self.field_copy = copy.deepcopy(self.grid)
        self.FPS = 60

    def get_rect(self, x, y):
        return x * self.TILE + 1, y * self.TILE + 1, self.TILE - 1, self.TILE - 1

    def neibours_alive(self, field, i, j):
        cnt = 0
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                tmp_x = x
                tmp_y = y
                if i + x > self.rows - 1:
                    tmp_x = -i
                if i + x < 0:
                    tmp_x = self.rows - 1
                if j + y > self.cols - 1:
                    tmp_y = -j
                if j + y < 0:
                    tmp_y = self.cols - 1
                if field[i + tmp_x][j + tmp_y] == 1 and not (x == 0 and y == 0):
                    cnt += 1
        return cnt

    def update_field(self, field):
        for x in range(self.cols):
            for y in range(self.rows):
                if self.is_dead(field[y][x]):
                    if self.neibours_alive(field, y, x) == 3:
                        self.field_copy[y][x] = LIFE
                else:
                    if self.neibours_alive(field, y, x) < 2 or self.neibours_alive(field, y, x) > 3:
                        self.field_copy[y][x] = DEATH
        return self.field_copy

    def is_dead(self, cage):
        return True if cage == 0 else False

    def update(self):
        self.screen.fill(pg.Color('black'))
        self.grid = copy.deepcopy(self.update_field(self.grid))

    def draw(self):
        [[pg.draw.rect(self.screen, pg.Color('darkorange'), self.get_rect(x, y)) for x, col in enumerate(row) if col]
         for y, row in enumerate(self.update_field(self.grid))]

        pg.display.flip()

    def run(self):
        while True:
            self.draw()
            self.update()

            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            self.clock.tick(self.FPS)
            pg.display.set_caption(f'Game of Life. FPS: {self.clock.get_fps()}')


if __name__ == '__main__':
    app = App()
    app.run()

