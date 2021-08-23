import random as rd
import pygame as pg
import time

win = pg.display.set_mode((600, 600))
apple = pg.transform.scale(pg.image.load("Assets/appleimage.png"), (40, 40))
mouth = pg.transform.scale(pg.image.load("Assets/mouth.png"), (55, 58))
mouth1 = pg.transform.scale(pg.image.load("Assets/mouth1.png"), (30, 58))
mouth2 = pg.transform.scale(pg.image.load("Assets/mouth2.png"), (30, 58))
joint = pg.transform.scale(pg.image.load("Assets/joint.png"), (43, 43))
joint_box = pg.Rect(0, 0, 30, 30)
body = pg.transform.scale(pg.image.load("Assets/body.png"), (35, 34))
tail = pg.transform.scale(pg.image.load("Assets/tail.png"), (40,38))
apple_box = pg.Rect(350, 350, 30, 30)
bg = pg.Rect(0, 0, 600, 600)
x_pos, y_pos = 200, 200
box_lst = []
draw_lst = []
val = 4
move_direction = "right"
index1, index2 = 185, 183
snake_vel = 30
val = 0
val2 = 1

class block:
    def __init__(self, type, x, y, direction, image):
        self.type = type
        self.x = x
        self.y = y
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


def generate_boxes():
    global box_lst
    x, y = 0, 0
    for i in range(20):
        for j in range(20):
            box_lst.append(pg.Rect(x, y, 30, 30))
            x += 30
        y += 30
        x = 0


def slide(lst, index1, index2):
    temp = lst[index1]
    lst[index1] = lst[index2]
    lst[index2] = temp


def draw_snake():
    global val,draw_lst,val2
    r = range(len(draw_lst)-1)
    val = 0
    for i in r:
        if draw_lst[i+1].type == "joint" and val == 0:
            if val == 0:
                slide(draw_lst,i+1,i+2)
                val = 1
            if draw_lst[i-1].type == "joint":
                temp_direction = draw_lst[i-2].direction
            else:
                temp_direction = draw_lst[i-1].direction
            if temp_direction == "up":
                draw_lst[i].change_y(draw_lst[i].y-30)
                draw_lst[i].change_x(draw_lst[i].x+30)
                draw_lst[i].handler = 1
                draw_lst[i].image = pg.transform.rotate(draw_lst[i].original_image,90)
                draw_lst[i].direction = "up"
            if temp_direction == "down":
                draw_lst[i].image = pg.transform.rotate(draw_lst[i].original_image,270)
                draw_lst[i].direction = "down"
            if temp_direction == "right":
                draw_lst[i].image = pg.transform.rotate(draw_lst[i].original_image,0)
                draw_lst[i].direction = "right"
            if temp_direction == "left":
                draw_lst[i].image = pg.transform.rotate(draw_lst[i].original_image,180)
                draw_lst[i].direction = "left"
        if draw_lst[i].type == "mouth":
            win.blit(draw_lst[i].image,(draw_lst[i].x-13,draw_lst[i].y-12))
        if draw_lst[i].type == "joint":
            win.blit(draw_lst[i].image,(draw_lst[i].x-5,draw_lst[i].y-4))
        if draw_lst[i].type == "body":
            win.blit(draw_lst[i].image,(draw_lst[i].x-1,draw_lst[i].y))
        if draw_lst[i].type == "tail":
            win.blit(draw_lst[i].image,(draw_lst[i].x-3,draw_lst[i].y-2))
        time.sleep(0.5)
        pg.display.update()
    if draw_lst[-1].type == "joint":
        draw_lst.pop(-1)
        val = 0



def eat_apple():
    pass


def draw_window():
    global index1
    pg.draw.rect(win, "#000000", bg)
    val = 0
    val2 = 0
    for j in range(20):
        for i in range(20):
            if (i + val) % 2 == 0:
                pg.draw.rect(win, "#66ff33", box_lst[val2])
            else:
                pg.draw.rect(win, "#39e600", box_lst[val2])
            val2 += 1
        if j % 2 == 0:
            val = 1
        else:
            val = 0
    if apple_box.colliderect(draw_lst[0].rect):
        eat_apple()
    apple_box.x, apple_box.y = a.x + 5, a.y + 5
    pg.draw.rect(win, "#39e600", apple_box)
    draw_snake()
    if draw_lst[0].x < 570:
        temp_draw_lst = draw_lst[::-1]
        for i in range(1,len(draw_lst)):
            if temp_draw_lst[i].type == "mouth":
                if draw_lst[0].direction == "right":
                    draw_lst[0].change_x(draw_lst[0].x + snake_vel)
                if draw_lst[0].direction == "left":
                    draw_lst[0].change_x(draw_lst[0].x - snake_vel)
                if draw_lst[0].direction == "down":
                    draw_lst[0].change_y(draw_lst[0].y + snake_vel)
                if draw_lst[0].direction == "up":
                    draw_lst[0].change_y(draw_lst[0].y - snake_vel)
            if temp_draw_lst[i].type != "joint" and i < len(draw_lst)-1:
                if temp_draw_lst[i+1].type == "mouth" and temp_draw_lst[i+1].handler == 1:
                    print(temp_draw_lst[i].type,1)
                    temp_draw_lst[i+1].handler = 0
                    temp_draw_lst[i].change_x(temp_draw_lst[i+1].last_cod[0])
                    temp_draw_lst[i].change_y(temp_draw_lst[i+1].last_cod[1])
                    continue
                elif temp_draw_lst[i+1].type != "joint":
                    print(temp_draw_lst[i].type,temp_draw_lst[i+1].type,2)
                    temp_draw_lst[i].change_x(temp_draw_lst[i+1].x)
                    temp_draw_lst[i].change_y(temp_draw_lst[i+1].y)
                if temp_draw_lst[i].handler == 1:
                    temp_draw_lst[i].handler = 0
                elif temp_draw_lst[i+1].type == "joint":
                    print(temp_draw_lst[i].type,temp_draw_lst[i+1].type,temp_draw_lst[i+2].x,temp_draw_lst[i+2].y,3)
                    b = i+1
                    while temp_draw_lst[b].type == "joint":
                        b += 1
                    b -= i
                    temp_draw_lst[i].change_x(temp_draw_lst[i+b].x)
                    temp_draw_lst[i].change_y(temp_draw_lst[i+b].y)
        print("e")
    win.blit(apple, (apple_box.x - 13, apple_box.y - 13))
    pg.display.update()


def main():
    global a, index1, draw_lst, move_direction
    run = True
    clock = pg.time.Clock()
    a = box_lst[196]
    draw_lst = [block("mouth", box_lst[index1].x, box_lst[index1].y, "right", mouth),
                block("body", box_lst[index1 - 1].x, box_lst[index1 - 1].y, "right", body),
                block("body", box_lst[index1 - 2].x, box_lst[index1 - 2].y, "right", body),
                block("body", box_lst[index1 - 3].x, box_lst[index1 - 3].y, "right", body),
                block("tail", box_lst[index1 - 4].x, box_lst[index1 - 4].y, "right", tail),
                block("null", box_lst[index1 - 3].x, box_lst[index1 - 3].y, "null", tail)]

    while run:
        clock.tick(1)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP and move_direction != "up" and move_direction != "down":
                    if move_direction == "right":
                        draw_lst.insert(1,block("joint",draw_lst[0].x,draw_lst[0].y,"null",pg.transform.rotate(joint,270)))
                    else:
                        draw_lst.insert(1,block("joint",draw_lst[0].x,draw_lst[0].y,"null",pg.transform.rotate(joint,180)))
                    move_direction = "up"
                    draw_lst[0].handler = 1
                    draw_lst[0].change_cod(draw_lst[0].x,draw_lst[0].y)
                    draw_lst[0].change_y(draw_lst[0].y-30)
                    draw_lst[0].image = pg.transform.rotate(draw_lst[0].original_image,90)
                    draw_lst[0].direction = "up"
                if event.key == pg.K_DOWN and move_direction != "up" and move_direction != "down":
                    if move_direction == "right":
                        draw_lst.insert(1,block("joint",draw_lst[0].x,draw_lst[0].y,"null",pg.transform.rotate(joint,0)))
                    else:
                        draw_lst.insert(1,block("joint",draw_lst[0].x,draw_lst[0].y,"null",pg.transform.rotate(joint,90)))
                    move_direction = "down"
                    draw_lst[0].handler = 1
                    draw_lst[0].change_cod(draw_lst[0].x,draw_lst[0].y)
                    draw_lst[0].change_y(draw_lst[0].y+30)
                    draw_lst[0].image = pg.transform.rotate(draw_lst[0].original_image, 270)
                    draw_lst[0].direction = "down"
                if event.key == pg.K_RIGHT and move_direction != "right" and move_direction != "left":
                    if move_direction == "up":
                        draw_lst.insert(1,block("joint",draw_lst[0].x,draw_lst[0].y,"null",pg.transform.rotate(joint,90)))
                    else:
                        draw_lst.insert(1,block("joint",draw_lst[0].x,draw_lst[0].y,"null",pg.transform.rotate(joint,180)))
                    move_direction = "right"
                    draw_lst[0].handler = 1
                    draw_lst[0].change_cod(draw_lst[0].x,draw_lst[0].y)
                    draw_lst[0].change_x(draw_lst[0].x+30)
                    draw_lst[0].image = pg.transform.rotate(draw_lst[0].original_image, 0)
                    draw_lst[0].direction = "right"
                if event.key == pg.K_LEFT and move_direction != "right" and move_direction != "left":
                    if move_direction == "up":
                        draw_lst.insert(1,block("joint",draw_lst[0].x,draw_lst[0].y,"null",pg.transform.rotate(joint,0)))
                    else:
                        draw_lst.insert(1,block("joint",draw_lst[0].x,draw_lst[0].y,"null",pg.transform.rotate(joint,270)))
                    move_direction = "left"
                    draw_lst[0].handler = 1
                    draw_lst[0].change_cod(draw_lst[0].x,draw_lst[0].y)
                    draw_lst[0].change_x(draw_lst[0].x-30)
                    draw_lst[0].image = pg.transform.rotate(draw_lst[0].original_image, 180)
                    draw_lst[0].direction = "left"
        draw_window()
    pg.display.quit()
    pg.quit()


if __name__ == "__main__":
    generate_boxes()
    main()
