import pygame as pg
from random import choice
from time import sleep

pg.font.init()

class background:
    def __init__(self, master_window, window_side, no_of_blocks):
        self.box_lst = []
        self.temp = 0
        self.no_of_blocks = no_of_blocks
        self.master_window = master_window
        side = window_side / no_of_blocks
        val, val1 = 0, 0
        if window_side % no_of_blocks == 0:
            for i in range(no_of_blocks):
                for j in range(no_of_blocks):
                    self.box_lst.append(pg.Rect(val, val1, side, side))
                    val += side
                val1 += side
                val = 0

    def draw_boxes(self):
        val2 = 0
        for j in range(self.no_of_blocks):
            for i in range(self.no_of_blocks):
                if (i + self.temp) % 2 == 0:
                    pg.draw.rect(self.master_window, "#66ff33", self.box_lst[val2])
                else:
                    pg.draw.rect(self.master_window, "#39e600", self.box_lst[val2])
                val2 += 1
            if j % 2 == 0:
                self.temp = 1
            else:
                self.temp = 0


class block:
    def __init__(self, x, y, side_len, direction, id):
        self.x, self.y = x, y
        self.id = id
        self.direction = direction
        self.rect = pg.Rect(x, y, side_len[0], side_len[1])

    def change_x(self, new_x):
        self.x = self.rect.x = new_x

    def change_y(self, new_y):
        self.y = self.rect.y = new_y


class snake_class:
    def __init__(self, master_window):
        self.master_window = master_window
        self.snake_vel = 30
        self.pause_rect = pg.Rect(15,15,30,30)
        self.play_button = pg.transform.scale(pg.image.load("Assets/play_button.png"),(30,30))
        self.pause_button = pg.transform.scale(pg.image.load("Assets/pause_button.png"),(26,28))
        self.mouth = pg.transform.scale(pg.image.load("Assets/mouth.png"), (56,50))
        self.mouth1 = pg.transform.scale(pg.image.load("Assets/mouth_open.png"), (48, 48))
        self.joint = pg.transform.scale(pg.image.load("Assets/joint.png"), (43, 43))
        self.body = pg.transform.scale(pg.image.load("Assets/body1.png"), (35, 34))
        self.tail = pg.transform.scale(pg.image.load("Assets/tail1.png"), (40, 37))
        self.body_lst = []

    def create_snake(self, no_of_parts, starting_pos):
        self.side_len = 30
        val = 0
        val1 = 0
        x, y = starting_pos[0], starting_pos[1]
        for i in range(no_of_parts):
            self.body_lst.append(block(x - val, y, (self.side_len, self.side_len), "right", val1))
            val += 30
            val1 += 1

    def turn_up(self):
        if self.body_lst[0].direction == "right":
            self.body_lst[0].change_x(self.body_lst[0].x - self.snake_vel)
        if self.body_lst[0].direction == "left":
            self.body_lst[0].change_x(self.body_lst[0].x + self.snake_vel)
        self.body_lst[0].direction = "up"
        self.body_lst[0].change_y(self.body_lst[0].y - self.snake_vel)

    def turn_down(self):
        if self.body_lst[0].direction == "right":
            self.body_lst[0].change_x(self.body_lst[0].x - self.snake_vel)
        if self.body_lst[0].direction == "left":
            self.body_lst[0].change_x(self.body_lst[0].x + self.snake_vel)
        self.body_lst[0].direction = "down"
        self.body_lst[0].change_y(self.body_lst[0].y + self.snake_vel)

    def turn_right(self):
        if self.body_lst[0].direction == "up":
            self.body_lst[0].change_y(self.body_lst[0].y + self.snake_vel)
        if self.body_lst[0].direction == "down":
            self.body_lst[0].change_y(self.body_lst[0].y - self.snake_vel)
        self.body_lst[0].direction = "right"
        self.body_lst[0].change_x(self.body_lst[0].x + self.snake_vel)

    def turn_left(self):
        if self.body_lst[0].direction == "up":
            self.body_lst[0].change_y(self.body_lst[0].y + self.snake_vel)
        if self.body_lst[0].direction == "down":
            self.body_lst[0].change_y(self.body_lst[0].y - self.snake_vel)
        self.body_lst[0].direction = "left"
        self.body_lst[0].change_x(self.body_lst[0].x - self.snake_vel)

    def end_game(self,score):
        self.end_font = pg.font.SysFont("Arial",80,1)
        self.score_font = pg.font.SysFont("Arial",50,1)
        self.master_window.blit(self.end_font.render("Game Over",1,"#000000"),(70,200))
        self.master_window.blit(self.score_font.render(f"Score:{score}",1,"#000000"),(200,280))
        pg.display.update()
        pg.time.delay(4000)

    def move_snake(self,score):
        if self.body_lst[0].x not in range(0, 600) or self.body_lst[0].y not in range(0, 600):
            self.end_game(score)
            return 1
        for i in range(1,len(self.body_lst)):
            if self.body_lst[0].rect.colliderect(self.body_lst[i].rect):
                self.end_game(score)
                return 1

        temp_lst = self.body_lst[::-1]
        for i in range(len(temp_lst) - 1):
            temp_lst[i].change_x(temp_lst[i + 1].x)
            temp_lst[i].change_y(temp_lst[i + 1].y)
        if temp_lst[-1].direction == "right":
            temp_lst[-1].change_x(temp_lst[-1].x + self.snake_vel)
        if temp_lst[-1].direction == "left":
            temp_lst[-1].change_x(temp_lst[-1].x - self.snake_vel)
        if temp_lst[-1].direction == "up":
            temp_lst[-1].change_y(temp_lst[-1].y - self.snake_vel)
        if temp_lst[-1].direction == "down":
            temp_lst[-1].change_y(temp_lst[-1].y + self.snake_vel)

    def draw_snake(self, mouth,val1):
        if val1 == 0:
            pg.draw.rect(self.master_window,"#ffffff",self.pause_rect)
            self.master_window.blit(self.pause_button, (self.pause_rect.x, self.pause_rect.y))
        if val1 == 1:
            start_font = pg.font.SysFont("Arial",50,1)
            pg.draw.rect(self.master_window,"#ffffff",self.pause_rect)
            self.master_window.blit(self.pause_button, (self.pause_rect.x, self.pause_rect.y))
            self.master_window.blit(start_font.render("Press Space to Start",1,"#000000"),(70,150))
            pg.display.update()
            return 1
        if val1 == 2:
            pg.draw.rect(self.master_window,"#ffffff",self.pause_rect)
            self.master_window.blit(self.play_button, (self.pause_rect.x, self.pause_rect.y))
            return 2
        if self.body_lst[0].direction == "right":
            mouth[0] = pg.transform.rotate(mouth[0], 0)
        if self.body_lst[0].direction == "left":
            mouth[0] = pg.transform.rotate(mouth[0], 180)
        if self.body_lst[0].direction == "up":
            mouth[0] = pg.transform.rotate(mouth[0], 90)
        if self.body_lst[0].direction == "down":
            mouth[0] = pg.transform.rotate(mouth[0], 270)
        if mouth[1] == 0:
            self.master_window.blit(mouth[0], (self.body_lst[0].x - 10, self.body_lst[0].y - 9))
        if mouth[1] == 1:
            self.master_window.blit(mouth[0], (self.body_lst[0].x - 7, self.body_lst[0].y - 7))
        for i in range(1, len(self.body_lst) - 1):
            if self.body_lst[i - 1].y == self.body_lst[i].y - self.side_len and self.body_lst[i + 1].y == self.body_lst[
                i].y:
                if self.body_lst[i - 1].x == self.body_lst[i].x and self.body_lst[i].x == self.body_lst[
                    i + 1].x + self.side_len:  # turning up from right
                    self.master_window.blit(pg.transform.rotate(self.joint, 270),
                                            (self.body_lst[i].x - 5, self.body_lst[i].y - 4))
                if self.body_lst[i - 1].x == self.body_lst[i].x and self.body_lst[i].x == self.body_lst[
                    i + 1].x - self.side_len:  # turning up from right
                    self.master_window.blit(pg.transform.rotate(self.joint, 180),
                                            (self.body_lst[i].x - 5, self.body_lst[i].y - 4))
            if self.body_lst[i - 1].y == self.body_lst[i].y + self.side_len and self.body_lst[i + 1].y == self.body_lst[
                i].y:
                if self.body_lst[i - 1].x == self.body_lst[i].x and self.body_lst[i].x == self.body_lst[
                    i + 1].x + self.side_len:  # turning down from right
                    self.master_window.blit(pg.transform.rotate(self.joint, 0),
                                            (self.body_lst[i].x - 5, self.body_lst[i].y - 4))
                if self.body_lst[i - 1].x == self.body_lst[i].x and self.body_lst[i].x == self.body_lst[
                    i + 1].x - self.side_len:  # turning down from left
                    self.master_window.blit(pg.transform.rotate(self.joint, 90),
                                            (self.body_lst[i].x - 5, self.body_lst[i].y - 4))
            if self.body_lst[i - 1].x == self.body_lst[i].x + self.side_len and self.body_lst[i + 1].x == self.body_lst[
                i].x:
                if self.body_lst[i - 1].y == self.body_lst[i].y and self.body_lst[i].y == self.body_lst[
                    i + 1].y - self.side_len:  # turning right from up
                    self.master_window.blit(pg.transform.rotate(self.joint, 90),
                                            (self.body_lst[i].x - 5, self.body_lst[i].y - 4))
                if self.body_lst[i - 1].y == self.body_lst[i].y and self.body_lst[i].y == self.body_lst[
                    i + 1].y + self.side_len:  # turning right from down
                    self.master_window.blit(pg.transform.rotate(self.joint, 180),
                                            (self.body_lst[i].x - 5, self.body_lst[i].y - 4))
            if self.body_lst[i - 1].x == self.body_lst[i].x - self.side_len and self.body_lst[i + 1].x == self.body_lst[
                i].x:
                if self.body_lst[i - 1].y == self.body_lst[i].y and self.body_lst[i].y == self.body_lst[
                    i + 1].y - self.side_len:  # turning left from up
                    self.master_window.blit(pg.transform.rotate(self.joint, 0),
                                            (self.body_lst[i].x - 5, self.body_lst[i].y - 4))
                if self.body_lst[i - 1].y == self.body_lst[i].y and self.body_lst[i].y == self.body_lst[
                    i + 1].y + self.side_len:  # turning right from down
                    self.master_window.blit(pg.transform.rotate(self.joint, 270),
                                            (self.body_lst[i].x - 5, self.body_lst[i].y - 4))
            if self.body_lst[i - 1].y == self.body_lst[i].y == self.body_lst[i + 1].y:
                self.master_window.blit(self.body, (self.body_lst[i].x - 1, self.body_lst[i].y))
            if self.body_lst[i - 1].x == self.body_lst[i].x == self.body_lst[i + 1].x:
                self.master_window.blit(pg.transform.rotate(self.body, 90),
                                        (self.body_lst[i].x - 1, self.body_lst[i].y))
        if self.body_lst[-2].y == self.body_lst[-1].y:
            if self.body_lst[-2].x == self.body_lst[-1].x + self.side_len:
                tail = pg.transform.rotate(self.tail, 0)
                self.body_lst[-1].direction = "right"
            if self.body_lst[-2].x == self.body_lst[-1].x - self.side_len:
                tail = pg.transform.rotate(self.tail, 180)
                self.body_lst[-1].direction = "left"
        if self.body_lst[-2].x == self.body_lst[-1].x:
            if self.body_lst[-2].y == self.body_lst[-1].y - self.side_len:
                tail = pg.transform.rotate(self.tail, 90)
                self.body_lst[-1].direction = "up"
            if self.body_lst[-2].y == self.body_lst[-1].y + self.side_len:
                tail = pg.transform.rotate(self.tail, 270)
                self.body_lst[-1].direction = "down"
        self.master_window.blit(tail, (self.body_lst[-1].x - 3, self.body_lst[-1].y - 2))
        return 0

class apple:
    def __init__(self, master_window, block_lst, body_lst, snake_vel, x, y):
        self.master_window = master_window
        self.snake_vel = snake_vel
        self.body_lst = body_lst
        self.score = 0
        self.score_font = pg.font.SysFont("Arial",30,1)
        self.block_lst = block_lst
        self.apple = pg.transform.scale(pg.image.load("Assets/appleimage.png"), (40, 40))
        self.rect = pg.Rect(x, y, 30, 30)
        self.x, self.y = x, y
        self.range_lst = [[f for f in range(self.x - 30, self.x + 60)], [f for f in range(self.y - 30, self.y + 60)]]

    def position_checker(self, x):
        for ech in self.body_lst:
            if ech.x == x:
                return 1
        return 0

    def eat_apple(self):
        if self.body_lst[-1].direction == "right":
            self.body_lst[-1].change_x(self.body_lst[-1].x - self.snake_vel)
            self.body_lst.insert(-1, block(self.body_lst[-1].x + 30, self.body_lst[-1].y, (30, 30), "null",
                                           len(self.body_lst) - 2))
        if self.body_lst[-1].direction == "left":
            self.body_lst.insert(-1, block(self.body_lst[-1].x, self.body_lst[-1].y, (30, 30), "null",
                                           len(self.body_lst) - 2))
            self.body_lst[-1].change_x(self.body_lst[-1].x + self.snake_vel)
        if self.body_lst[-1].direction == "up":
            self.body_lst.insert(-1, block(self.body_lst[-1].x, self.body_lst[-1].y, (30, 30), "null",
                                           len(self.body_lst) - 2))
            self.body_lst[-1].change_y(self.body_lst[-1].y + self.snake_vel)
        if self.body_lst[-1].direction == "down":
            self.body_lst.insert(-1, block(self.body_lst[-1].x, self.body_lst[-1].y, (30, 30), "null",
                                           len(self.body_lst) - 2))
            self.body_lst[-1].change_y(self.body_lst[-1].y - self.snake_vel)

    def change_x(self, new_x):
        self.x = self.rect.x = new_x

    def change_y(self, new_y):
        self.y = self.rect.y = new_y

    def randomize_pos(self):
        block = choice(self.block_lst)
        while self.position_checker(block.x) != 0:
            block = choice(self.block_lst)
        self.change_y(block.y)
        self.change_x(block.x)
        self.range_lst = [[f for f in range(self.x - 30, self.x + 60)], [f for f in range(self.y - 30, self.y + 60)]]

    def draw_apple(self, mouth):
        a = False
        if self.body_lst[1].rect.x == self.rect.x and self.body_lst[1].rect.y == self.rect.y:
            a = True
        if self.body_lst[1].rect.x == self.rect.x and self.body_lst[1].rect.y == self.rect.y:
            a = True
        if a == True:
            self.score += 1
            self.eat_apple()
            self.randomize_pos()
        self.master_window.blit(self.apple, (self.rect.x - 5, self.rect.y - 9))
        self.master_window.blit(self.score_font.render(str(self.score),1,"#000000"),(560,10))



