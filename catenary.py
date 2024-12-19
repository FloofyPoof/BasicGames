import pygame
import math

from pygame.examples.moveit import HEIGHT

pygame.font.init()

FONT = pygame.font.SysFont('comicsans', 30)
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
x_mouse, y_mouse = 0, 0
x_mouse_prev, y_mouse_prev = 0, 0
text_width = FONT.render(f"Width: {0}", 1, "white")
text_height = FONT.render(f"Height: {0}", 1, "white")
a = 50
text_a = FONT.render(f"A: {a}", 1, "white")
point_count = 100
catenary_points = [(0, 0) for _ in range(point_count + 1)]
run = True
while run:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            run = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                a -= 15
                text_a = FONT.render(f"A: {a}", 1, "white")
            if event.key == pygame.K_s:
                a += 15
                text_a = FONT.render(f"A: {a}", 1, "white")

    x_mouse, y_mouse = pygame.mouse.get_pos()
    WIN.fill((0,0,0))

    if x_mouse != x_mouse_prev or y_mouse != y_mouse_prev:
        text_width = FONT.render(f"Width: {int(abs(WIDTH/2 - x_mouse))}", 1, "white")
        text_height = FONT.render(f"Height: {int(abs(HEIGHT/2 - y_mouse))}", 1, "white")

    x_mouse_prev, y_mouse_prev = x_mouse, y_mouse

    WIN.blit(text_width, (10, 10)) # to a list or something
    WIN.blit(text_height, (10, 50))
    WIN.blit(text_a, (10, 90))
    temp_distance = WIDTH//2 - x_mouse
    for i in range(point_count + 1):
        xx = x_mouse+i/point_count*temp_distance*2
        yy = - a * math.cosh((xx - WIDTH/2) / a) + HEIGHT/2 + a
        catenary_points[i] = (xx, yy)
    del temp_distance
    for pos in catenary_points:
        pygame.draw.circle(WIN, (99, 99, 99), pos, 3)
    pygame.draw.lines(WIN, (77, 77, 77), False, catenary_points, 2)
    #pygame.draw.line(WIN, (88, 88, 88), (WIDTH - x_mouse, y_mouse), (WIDTH//2, HEIGHT//2), 3)
    #pygame.draw.line(WIN, (133, 133, 133), (x_mouse, y_mouse), (WIDTH//2, HEIGHT//2), 3)
    pygame.draw.circle(WIN, (0, 150, 0), (WIDTH - x_mouse, y_mouse), 5)
    pygame.draw.circle(WIN, (0, 255, 0), (x_mouse, y_mouse), 5)
    pygame.draw.circle(WIN, (255, 0, 0), (WIDTH//2, HEIGHT//2), 5)
    pygame.draw.line(WIN, (255, 255, 0), (0, HEIGHT//2 + a), (WIDTH, HEIGHT//2 + a), 6)
    pygame.display.update()