import pygame
import random
pygame.font.init()
FONT = pygame.font.SysFont('comicsans', 30)

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Rope test')
BG = pygame.transform.scale(pygame.image.load('sky.jpg'), (WIDTH, HEIGHT))
draw_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
rect_cork = pygame.Rect(WIDTH/10, HEIGHT/10, WIDTH*8/10, HEIGHT*8/10) # not here

def onCork(x, y):
        left = x > rect_cork.left
        right = x < rect_cork.left + rect_cork.width
        top = y > rect_cork.top
        bottom = y < rect_cork.top + rect_cork.height
        return left and right and top and bottom

def catenary(x1, y1, x2, y2, L):
    dx = x2 - x1
    dy = y2 - y1
    x_mean = (x1 + x2) / 2
    y_mean = (y1 + y2) / 2

    if dx ** 2 + dy ** 2 > L ** 2:
        exit("The string is too short!")

    r = math.sqrt(L**2 - dy**2) / dx
    da = 1e-10
    A0 = math.sqrt(6 * (r - 1))
    if r >= 3:
        A0 = math.log(2 * r) + math.log(math.log(2 * r))

    A1 = A0 - (math.sinh(A0) - r * A0) / (math.cosh(A0) - r)

    while abs(r - math.sinh(A1) / A1) > da:
        print(abs(r - math.sinh(A1) / A1))
        A0 = A1
        A1 = A0 - (math.sinh(A0) - r * A0) / (math.cosh(A0) - r)

    a = dx / (2 * A1)
    b = x_mean - a * math.atanh(dy / L) # b is center of the curve
    c = y_mean - L / (2 * math.tanh(A1)) # c is vertical offset

    xpoints = np.arange(x1, x2, 1e-2)
    ypoints = [a * math.cosh((x - b)/ a) + c for x in xpoints]
    return xpoints, ypoints

def main():
    run = True
    Y_START = random.randint(HEIGHT//10, HEIGHT*8//10)
    Y_FINISH = random.randint(HEIGHT//10, HEIGHT*8//10)
    rope_length = 200

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
        WIN.blit(BG, (0, 0))
        t_length = FONT.render(f"Rope length: {rope_length}", 1, "white")
        WIN.blit(t_length, (10, 10))

        pygame.draw.rect(WIN, pygame.Color(0, 0, 200, 200), rect_cork, 3)
        pygame.draw.circle(WIN, pygame.Color(200, 0, 0, 200), (WIDTH/10, Y_START), 5)
        pygame.draw.circle(WIN, pygame.Color(200, 0, 0, 200), (WIDTH*9/10, Y_FINISH), 5)
        pygame.draw.circle(WIN, pygame.Color(0, 200, 0, 200), mouse_pos, 5)
        #WIN.blit(draw_surf, (0,0)) #TODO alpha
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()