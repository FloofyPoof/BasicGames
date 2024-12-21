import pygame
import random
import math
import numpy as np

pygame.font.init()
FONT = pygame.font.SysFont('comicsans', 30)

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Rope test')
BG = pygame.transform.scale(pygame.image.load('sky.jpg'), (WIDTH, HEIGHT))
draw_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
rect_cork = pygame.Rect(WIDTH/10, HEIGHT/10, WIDTH*8/10, HEIGHT*8/10) # not here
rope_calculation_points = 1e2

def onCork(x, y):
        left = x > rect_cork.left
        right = x < rect_cork.left + rect_cork.width
        top = y > rect_cork.top
        bottom = y < rect_cork.top + rect_cork.height
        return left and right and top and bottom

def catenary(x1, y1, x2, y2, L, rope_calculation_points):
    dx = x2 - x1
    dy = y2 - y1
    x_mean = (x1 + x2) / 2
    y_mean = (y1 + y2) / 2

    if dx ** 2 + dy ** 2 >= L ** 2:
        #print("The string is too short!")
        return False

    r = math.sqrt(L**2 - dy**2) / dx
    da = 1e-10
    A0 = math.sqrt(6 * (r - 1))
    if r >= 3:
        A0 = math.log(2 * r) + math.log(math.log(2 * r))

    denominator = math.cosh(A0) - r
    if denominator:
        A1 = A0 - (math.sinh(A0) - r * A0) / denominator
    else:
        A1 = A0 - (math.sinh(A0) - r * A0) / 1e-4

    while abs(r - math.sinh(A1) / A1) > da:
        #print(abs(r - math.sinh(A1) / A1))
        A0 = A1
        A1 = A0 - (math.sinh(A0) - r * A0) / (math.cosh(A0) - r)

    a = dx / (2 * A1)
    b = x_mean - a * math.atanh(dy / L) # b is center of the curve
    c = y_mean - L / (2 * math.tanh(A1)) # c is vertical offset

    xpoints = np.arange(x1, x2, abs(x2 - x1) / rope_calculation_points)
    #ypoints = [a * math.cosh((x - b)/ a) + c for x in xpoints]
    ypoints = [y1 + y2 - a * math.cosh((x - x1 - x2 + b)/ a) - c for x in xpoints]
    return_val = []
    temp_touple = 0, 0
    for i in range(xpoints.size):
        temp_touple = xpoints[i], ypoints[i]
        return_val.append(temp_touple)
    return return_val

def main():
    run = True
    Y_START = random.randint(HEIGHT//10, HEIGHT*8//10)
    Y_FINISH = random.randint(HEIGHT//10, HEIGHT*8//10)
    rope_length = 200
    rope_points = [range(int(rope_calculation_points))]
    mouse_onCork = 0, 0
    mouse_pos_prev = 0, 0
    mouse_moved = False
    on_cork = True
    rope_last_good_pos = [(0, 0), (0, 1)]

    while run:
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    rope_length += 25
                if event.key == pygame.K_s and rope_length > 25:
                    rope_length -= 25

        mouse_pos = pygame.mouse.get_pos()
        mouse_moved = True
        if mouse_pos == mouse_pos_prev:
            mouse_moved = False
        mouse_pos_prev = mouse_pos
        on_cork = False
        if onCork(mouse_pos[0], mouse_pos[1]):
            mouse_onCork = mouse_pos
            on_cork = True

        WIN.blit(BG, (0, 0))
        t_length = FONT.render(f"Rope length: {rope_length}", 1, "white")
        WIN.blit(t_length, (10, 10))

        selected_point = WIDTH/10, Y_START
        if mouse_moved and on_cork:
            rope_points = catenary(selected_point[0], selected_point[1], mouse_onCork[0], mouse_onCork[1], rope_length, rope_calculation_points)
        if rope_points:
            rope_last_good_pos = rope_points
            if on_cork:
                rope_last_good_pos.append(mouse_pos)
        pygame.draw.lines(WIN, pygame.Color(200, 200, 200, 200), 0, rope_last_good_pos, 3)


        pygame.draw.rect(WIN, pygame.Color(0, 0, 200, 200), rect_cork, 3)
        pygame.draw.circle(WIN, pygame.Color(200, 0, 0, 200), (WIDTH/10, Y_START), 5)
        pygame.draw.circle(WIN, pygame.Color(200, 0, 0, 200), (WIDTH*9/10, Y_FINISH), 5)
        pygame.draw.circle(WIN, pygame.Color(0, 200, 0, 200), mouse_onCork, 5)
        #WIN.blit(draw_surf, (0,0)) #TODO alpha
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()