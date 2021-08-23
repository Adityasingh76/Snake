import pygame as pg
import random as rd
import time

class background:
    def __init__(self,master_window,window_side,no_of_blocks):
        self.box_lst = []
        self.temp = 0
        self.master_window = master_window
        width = height = window_side / no_of_blocks
        val, val1 = 0, 0
        if window_side % no_of_blocks == 0:
            for i in range(no_of_blocks):
                for j in range(no_of_blocks):
                    self.box_lst.append(pg.Rect(val, val1, width, height))
                    val += 30
                val1 += 30
                val = 0

    def draw_boxes(self):
        val2 = 0
        for j in range(20):
            for i in range(20):
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
    def __init__(self, type, x, y, direction, image):
        self.type = type
        self.x = x
        self.y = y
        self.joint_direction = "null"
        self.fake_direction = direction
        self.last_direction = direction
        self.status = "unused"
        self.last_cod = [0,0]
        self.handler = 0
        self.direction = direction
        self.image = image
        self.original_image = image
        try:
            if self.type == "joint":
                self.rect = pg.Rect(self.x, self.y, 60, 60)
            else:
                self.rect = pg.Rect(self.x, self.y, 30, 30)
        except:
            pass
    def change_cod(self,new_x,new_y):
        self.last_cod[0],self.last_cod[1] = new_x,new_y
    def change_x(self, new_value):
        self.x = new_value
        self.rect.x = new_value

    def change_y(self, new_value):
        self.y = new_value
        self.rect.y = new_value

class snake_class():
    def __init__(self,master_window):
        self.master_window = master_window
        self.snake_vel = 30
        self.mouth = pg.transform.scale(pg.image.load("Assets/mouth.png"), (55, 58))
        self.mouth1 = pg.transform.scale(pg.image.load("Assets/mouth1.png"), (30, 58))
        self.mouth2 = pg.transform.scale(pg.image.load("Assets/mouth2.png"), (30, 58))
        self.joint = pg.transform.scale(pg.image.load("Assets/joint.png"), (43, 43))
        self.body = pg.transform.scale(pg.image.load("Assets/body.png"), (35, 34))
        self.tail = pg.transform.scale(pg.image.load("Assets/tail.png"), (40, 38))
        self.body_lst = []
    def create_body_lst(self,no_of_parts,x,y):
        self.body_lst.append(block("mouth",x,y,"right",self.mouth))
        val = 30
        for i in range(0,no_of_parts-2):
            self.body_lst.append(block("body",x-val,y,"right",self.body))
            val += 30
        self.body_lst.append(block("tail",x-val,y,"right",self.tail))
    def turn_up(self,initial_direction):
        if initial_direction == "right":
            image = pg.transform.rotate(self.joint,270)
        else:
            image = pg.transform.rotate(self.joint,180)
        self.body_lst.insert(1,block("joint",self.body_lst[0].x,self.body_lst[0].y,"null",image))
        self.body_lst[1].fake_direction = "up"
        self.body_lst[0].direction = "up"
        self.body_lst[0].change_cod(self.body_lst[0].x,self.body_lst[0].y)
        self.body_lst[0].image = pg.transform.rotate(self.body_lst[0].original_image, 90)
        self.body_lst[0].change_y(self.body_lst[0].y-30)
        self.body_lst[0].handler = 1

    def turn_down(self,initial_direction):
        if initial_direction == "right":
            image = pg.transform.rotate(self.joint,0)
        else:
            image = pg.transform.rotate(self.joint,90)
        self.body_lst.insert(1,block("joint",self.body_lst[0].x,self.body_lst[0].y,"null",image))
        self.body_lst[1].fake_direction = "down"
        self.body_lst[0].direction = "down"
        self.body_lst[0].change_cod(self.body_lst[0].x,self.body_lst[0].y)
        self.body_lst[0].image = pg.transform.rotate(self.body_lst[0].original_image, 270)
        self.body_lst[0].change_y(self.body_lst[0].y+30)
        self.body_lst[0].handler = 1

    def turn_right(self,initial_direction):
        if initial_direction == "up":
            image = pg.transform.rotate(self.joint,90)
        else:
            image = pg.transform.rotate(self.joint,180)
        self.body_lst.insert(1,block("joint",self.body_lst[0].x,self.body_lst[0].y,"null",image))
        self.body_lst[0].direction = "right"
        self.body_lst[1].fake_direction = "right"
        self.body_lst[0].change_cod(self.body_lst[0].x,self.body_lst[0].y)
        self.body_lst[0].image = pg.transform.rotate(self.body_lst[0].original_image, 0)
        self.body_lst[0].change_x(self.body_lst[0].x+30)
        self.body_lst[0].handler = 1

    def turn_left(self,initial_direction):
        if initial_direction == "up":
            image = pg.transform.rotate(self.joint,0)
        else:
            image = pg.transform.rotate(self.joint,270)
        self.body_lst.insert(1,block("joint",self.body_lst[0].x,self.body_lst[0].y,"null",image))
        self.body_lst[1].fake_direction = "left"
        self.body_lst[0].direction = "left"
        self.body_lst[0].change_cod(self.body_lst[0].x,self.body_lst[0].y)
        self.body_lst[0].image = pg.transform.rotate(self.body_lst[0].original_image, 180)
        self.body_lst[0].change_x(self.body_lst[0].x-30)
        self.body_lst[0].handler = 1

    def slide_block(self,index):
        val,val1 = 0,1
        for i in range(len(self.body_lst)):
            if self.body_lst[index-val1].type == "joint":
                temp = self.body_lst[index-val1]
                self.body_lst[index-val1] = self.body_lst[index-val]
                self.body_lst[index-val] = temp
                val1 += 1
                val += 1
            else:
                break
        return val1-1
    def move_snake(self):
        temp_lst = self.body_lst[::-1]
        val = 0
        if self.body_lst[0].type == "mouth":
            print(self.body_lst[0].type,end=";")
            for j in range(1,len(self.body_lst)):
                print(self.body_lst[j].type,end=";")
                if self.body_lst[j-1].type == "joint" and self.body_lst[j].type != "joint" and self.body_lst[j-1].status == "unused":
                    self.body_lst[j-1].status = "used"
                    if self.body_lst[j].type != "tail":
                        j -= self.slide_block(j)
                        temp_val = j - 1
                        while self.body_lst[temp_val].type == "joint":
                            temp_val -= 1
                        temp_direction = self.body_lst[temp_val].direction
                    if self.body_lst[j].type == "tail":
                        temp = self.body_lst[j-1]
                        self.body_lst[j-1] = self.body_lst[j]
                        self.body_lst[j] = temp
                        j -= 1
                        temp_val = j - 1
                        temp_direction = self.body_lst[j+1].fake_direction
                    print(f"'{self.body_lst[j].type,temp_val,temp_direction}'",end=";")
                    if temp_direction == "up":
                        self.body_lst[j].direction = "up"
                        self.body_lst[j].image = pg.transform.rotate(self.body_lst[j].original_image,90)
                    if temp_direction == "down":
                        self.body_lst[j].direction = "down"
                        self.body_lst[j].image = pg.transform.rotate(self.body_lst[j].original_image,270)
                    if temp_direction == "left":
                        self.body_lst[j].direction = "left"
                        self.body_lst[j].image = pg.transform.rotate(self.body_lst[j].original_image,180)
                    if temp_direction == "right":
                        self.body_lst[j].direction = "right"
                        self.body_lst[j].image = pg.transform.rotate(self.body_lst[j].original_image,0)
            print()
            for i in range(len(self.body_lst)):
                if temp_lst[i].type == "mouth":
                    if temp_lst[i].direction == "right":
                        temp_lst[i].change_x(temp_lst[i].x+self.snake_vel)
                    if temp_lst[i].direction == "left":
                        temp_lst[i].change_x(temp_lst[i].x-self.snake_vel)
                    if temp_lst[i].direction == "up":
                        temp_lst[i].change_y(temp_lst[i].y-self.snake_vel)
                    if temp_lst[i].direction == "down":
                        temp_lst[i].change_y(temp_lst[i].y+self.snake_vel)
                elif temp_lst[i].type != "joint" and temp_lst[i].type != "tail":
                    if temp_lst[i+1].type == "mouth" and temp_lst[i+1].handler == 1:
                        temp_lst[i].change_x(temp_lst[i+1].last_cod[0])
                        temp_lst[i].change_y(temp_lst[i+1].last_cod[1])
                    if temp_lst[i+1].type != "joint":
                        temp_lst[i].change_x(temp_lst[i+1].x)
                        temp_lst[i].change_y(temp_lst[i+1].y)
                    if temp_lst[i+1].type == "joint":
                        val = i+1
                        while temp_lst[val].type == "joint":
                            val += 1
                        val -= i
                        temp_lst[i].change_x(temp_lst[i+val].x)
                        temp_lst[i].change_y(temp_lst[i+val].y)
        for ech in self.body_lst:
            if ech.type == "joint" and ech.status == "used":
                ech.status = "unused"
        for ech in self.body_lst[::-1]:
            if ech.type != "joint":
                break
            elif ech.type == "joint":
                self.body_lst.pop(self.body_lst.index(ech))
    def draw_snake(self):
        for i in range(len(self.body_lst)):
            if self.body_lst[i].type == "mouth":
                self.master_window.blit(self.body_lst[i].image,(self.body_lst[i].x-13,self.body_lst[i].y-12))
            if self.body_lst[i].type == "joint":
                self.master_window.blit(self.body_lst[i].image,(self.body_lst[i].x-5,self.body_lst[i].y-4))
            if self.body_lst[i].type == "body":
                self.master_window.blit(self.body_lst[i].image,(self.body_lst[i].x-1,self.body_lst[i].y))
            if self.body_lst[i].type == "tail":
                self.master_window.blit(self.body_lst[i].image,(self.body_lst[i].x-3,self.body_lst[i].y-2))
class apple():
    def __init__(self):
        self.apple = pg.transform.scale(pg.image.load("Assets/appleimage.png"), (40, 40))

def main():
    win = pg.display.set_mode((600,600))
    pg.display.set_caption("Snake 1.0")
    bg = background(win,600,20)
    run = True
    current_direction = "right"
    direction_lst = ["right","left","up","down"]
    snake = snake_class(win)
    snake.create_body_lst(5,bg.box_lst[185].x,bg.box_lst[185].y)
    clock = pg.time.Clock()
    while run:
        clock.tick(1)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
            if event.type == pg.KEYDOWN:
                if current_direction in direction_lst[0:2]:
                    if event.key == pg.K_UP:
                        snake.turn_up(current_direction)
                        current_direction = "up"
                    if event.key == pg.K_DOWN:
                        snake.turn_down(current_direction)
                        current_direction = "down"
                if current_direction in direction_lst[2:4]:
                    if event.key == pg.K_RIGHT:
                        snake.turn_right(current_direction)
                        current_direction = "right"
                    if event.key == pg.K_LEFT:
                        snake.turn_left(current_direction)
                        current_direction = "left"
                if event.key == pg.K_PAUSE:
                    time.sleep(100)
        bg.draw_boxes()
        snake.draw_snake()
        snake.move_snake()
        pg.display.update()


if __name__ == "__main__":
    main()
