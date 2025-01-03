import math
import numpy as np
import pygame
from enum import Enum

def onCork(x, y, rect_cork):
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
    for i in range(xpoints.size):
        temp_tuple = float(xpoints[i]), float(ypoints[i])
        return_val.append(temp_tuple)
    return return_val

def snap_to(pos1, pos2, distance):
    if (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 < distance**2:
        return pos2
    return pos1

def draw_transparent_line(surface, color, pos1, pos2, width): #TODO with smaller surface
    temp_surf = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
    pygame.draw.line(temp_surf, color, pos1, pos2, width)
    surface.blit(temp_surf, (0,0))

def draw_transparent_rect(surface, color, rect, width=0): #TODO with smaller surface
    temp_surf = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
    pygame.draw.rect(temp_surf, color, rect, width)
    surface.blit(temp_surf, (0,0))

def distance_2d(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

def point_in_range_of_list(point, items2, distance):
    for items in items2:
        for item in items:
            if distance_2d(point, item) < distance:
                return True
    return False

class Button:
    growth = 1.3
    def __init__(self, surface, FONT, text="base", pos=(0.5, 0.5), color_rect=(128, 128, 128)):
        self.surface = surface
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.color_rect = color_rect

        self.t_length = FONT.render(text, 1, (222, 222, 222))
        self.win_width = surface.get_width()
        self.win_height = surface.get_height()
        self.x_size = self.t_length.get_width()
        self.y_size = self.t_length.get_height()
        self.rect = pygame.Rect(self.win_width*self.pos_x - self.x_size*self.growth/2, self.win_height*self.pos_y - self.y_size*self.growth/2, self.x_size * self.growth, self.y_size * self.growth)

    def draw(self):
        pygame.draw.rect(self.surface, self.color_rect, self.rect)
        self.surface.blit(self.t_length, (self.win_width * self.pos_x - self.x_size / 2, self.win_height * self.pos_y - self.y_size / 2))

    def on_button(self, mouse_pos):
        output = self.rect.collidepoint(mouse_pos)
        if output:
            self.get_darker()
        return output

    def get_darker(self):
        self.color_rect = [int(color * 0.7) for color in self.color_rect]

class Turret:
    pass

class GameStage(Enum):
    pregame = 0
    ropes = 1
    post_ropes = 2
    pins = 3