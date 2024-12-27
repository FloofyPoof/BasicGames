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

    if dx == 0:
        return False

    if dx ** 2 + dy ** 2 >= L ** 2:
        #print("The string is too short!")
        return False

    r = math.sqrt(L**2 - dy**2) / dx
    da = 1e-10
    if r - 1 < 0:
        return False
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

def snap_to(pos1, pos2, distance):
    if (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 < distance**2:
        return pos2
    return pos1

def main():
    run = True
    Y_START = random.randint(HEIGHT//10, HEIGHT*6//10)
    Y_FINISH = random.randint(HEIGHT//10, HEIGHT*6//10)
    rope_length = 300
    rope_points = False
    mouse_on_cork = 0, 0
    mouse_pos_prev = 0, 0
    mouse_moved = False
    on_cork = True
    rope_last_good_rope_pos = [(0, 0), (0, 1)]
    rope_oob = False
    rope_minimal_x = 50
    rope_last_valid_pos = 0, 0
    mouse1 = False
    mouse2 = False
    selected_point = WIDTH/10, Y_START
    pin_points = [selected_point]
    rope_all_ropes = []
    rope_calculating = True

    while run:
        keys = pygame.key.get_pressed()
        draw_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        mouse1 = False
        mouse2 = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                run = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and rope_length < 500:
                    rope_length += 25
                if event.key == pygame.K_s and rope_length > 200:
                    rope_length -= 25
            elif event.type == pygame.MOUSEBUTTONDOWN: # mouse motion
                mouse_buttons = pygame.mouse.get_pressed()
                if mouse_buttons[0]:
                    mouse1 = True
                if mouse_buttons[2]:
                    mouse2 = True



        mouse_pos = pygame.mouse.get_pos()
        mouse_moved = True
        if mouse_pos == mouse_pos_prev:
            mouse_moved = False
        mouse_pos_prev = mouse_pos
        on_cork = False
        if onCork(mouse_pos[0], mouse_pos[1]):
            mouse_on_cork = mouse_pos
            on_cork = True

        WIN.blit(BG, (0, 0))
        t_length = FONT.render(f"Rope length: {rope_length}", 1, "white")
        WIN.blit(t_length, (10, 10))

        if mouse2 and len(pin_points) > 1:
            pin_points.pop()
            selected_point = pin_points[-1]
            rope_all_ropes.pop()
            rope_calculating = True
            rope_last_valid_pos = 0, 0

        if rope_calculating:
            if mouse_moved and on_cork:
                rope_points = catenary(selected_point[0], selected_point[1], mouse_on_cork[0], mouse_on_cork[1], rope_length, rope_calculation_points)
            if rope_points != False:
                for (x, y) in rope_points:
                    rope_oob = False
                    if not onCork(WIDTH//2, y):
                        rope_oob = True
                        break
                if not rope_oob and abs(selected_point[0] - mouse_on_cork[0]) > rope_minimal_x + 5:
                    rope_last_good_rope_pos = rope_points
                    if on_cork:
                        rope_last_good_rope_pos.append(mouse_pos)
                        rope_last_valid_pos = mouse_pos
            if mouse1 and rope_last_valid_pos[0] and rope_last_valid_pos != pin_points[-1]:
                if WIDTH*9/10 - rope_last_valid_pos[0] < rope_minimal_x:
                    rope_last_valid_pos = WIDTH*9/10, Y_FINISH
                    rope_calculating = False
                    rope_last_good_rope_pos = catenary(pin_points[-1][0], pin_points[-1][1], WIDTH*9/10, Y_FINISH, rope_length, rope_calculation_points)
                    if rope_last_good_rope_pos == False:
                        print("they are too far")
                    else:
                        rope_last_good_rope_pos.append((WIDTH*9/10, Y_FINISH))
                        pin_points.append(rope_last_valid_pos)
                        rope_all_ropes.append(rope_last_good_rope_pos)
                else:
                    pin_points.append(rope_last_valid_pos)
                    rope_all_ropes.append(rope_last_good_rope_pos)
                if rope_calculating:
                    selected_point = rope_last_valid_pos
                else:
                    rope_last_good_rope_pos = catenary(selected_point[0], selected_point[1], mouse_on_cork[0], mouse_on_cork[1], rope_length, rope_calculation_points)

        if rope_calculating and len(rope_last_good_rope_pos) > 0:
            pygame.draw.lines(draw_surf, pygame.Color(155, 155, 155, 200), False, rope_last_good_rope_pos, 3)
        for rope in rope_all_ropes:
            pygame.draw.lines(draw_surf, pygame.Color(200, 200, 200, 200), False, rope, 3)
        if rope_calculating:
            pygame.draw.line(draw_surf, pygame.Color(200, 0, 0, 200), (pin_points[-1][0] + rope_minimal_x, HEIGHT/10), (pin_points[-1][0] + rope_minimal_x, HEIGHT*9/10), 3)
        pygame.draw.rect(draw_surf, pygame.Color(0, 0, 200, 100), rect_cork, 3)
        pygame.draw.circle(draw_surf, pygame.Color(200, 0, 0, 200), (WIDTH/10, Y_START), 5)
        pygame.draw.circle(draw_surf, pygame.Color(100, 0, 0, 200), (WIDTH*9/10, Y_FINISH), 5)
        pygame.draw.circle(draw_surf, pygame.Color(0, 200, 0, 200), mouse_on_cork, 5)
        if rope_calculating:
            pygame.draw.circle(draw_surf, pygame.Color(255, 200, 0, 200), rope_last_valid_pos, 4)
        for point in pin_points:
            pygame.draw.circle(draw_surf, pygame.Color(200, 0, 0, 200), point, 5)
        WIN.blit(draw_surf, (0,0)) #TODO alpha
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()