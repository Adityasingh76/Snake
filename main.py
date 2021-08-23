import pygame as pg
from game import *
from sys import exit as exit_program

def main():
    win = pg.display.set_mode((600, 600))
    pg.display.set_caption("Snake 1.0")
    bg = background(win, 600, 20)
    bg.draw_boxes()
    run = True
    mouth = 0
    val1 = 1
    val = 0
    start_font = pg.font.SysFont("Arial",80,1)
    snake = snake_class(win)
    snake.create_snake(5, (bg.box_lst[185].x, bg.box_lst[185].y))
    snake.draw_snake([snake.mouth,0],0)
    apple1 = apple(win, bg.box_lst, snake.body_lst, snake.snake_vel, bg.box_lst[196].x, bg.box_lst[196].y)
    apple1.draw_apple(snake.body_lst[0])
    pg.display.update()
    current_direction = "right"
    direction_lst = ["right", "left", "up", "down"]
    clock = pg.time.Clock()
    while run:
        clock.tick(6)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if snake.pause_rect.collidepoint(mouse_pos):
                    if val1 == 2:
                        val1 = 0
                    elif val1 == 0:
                        val1 = 2
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    val1 = 0
                if event.key == pg.K_ESCAPE:
                    if val1 == 2:
                        val1 = 0
                    elif val1 == 0:
                        val1 = 2
                if current_direction in direction_lst[0:2] and val1 == 0:
                    if event.key == pg.K_UP:
                        snake.turn_up()
                        current_direction = "up"
                    if event.key == pg.K_DOWN:
                        snake.turn_down()
                        current_direction = "down"
                if current_direction in direction_lst[2:4] and val1 == 0:
                    if event.key == pg.K_RIGHT:
                        snake.turn_right()
                        current_direction = "right"
                    if event.key == pg.K_LEFT:
                        snake.turn_left()
                        current_direction = "left"

        if snake.body_lst[0].x in apple1.range_lst[0] and snake.body_lst[0].y in apple1.range_lst[1]:
            mouth = [snake.mouth1, 1]
        else:
            mouth = [snake.mouth, 0]
        if val1 == 0:
            bg.draw_boxes()
        val1 = snake.draw_snake(mouth,val1)
        if val1 == 0:
            val = snake.move_snake(apple1.score)
        if val == 1:
            main()
        if val1 == 0:
            apple1.draw_apple(snake.body_lst[0])
        pg.display.update()
    pg.display.quit()
    exit_program()

if __name__ == "__main__":
    main()
