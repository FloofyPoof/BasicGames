import pygame

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
x_mouse, y_mouse = 0, 0

color = 255, 0, 0
first = True
prev_x, prev_y = 0, 0
pxarray = pygame.PixelArray(WIN)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    x_mouse, y_mouse = pygame.mouse.get_pos()
    WIN.fill((0,0,0))

    #calculate if mouse moves
    for y, py in enumerate(pxarray):
        for x, px in enumerate(py):
            if int(x) == (int(y) * int(y)) - 30 * int(y) + 450:
                #pxarray[y][x] = 0xFFFFFF

                if first:
                    first = False
                    prev_x, prev_y = x, y
                    continue

                pygame.draw.line(WIN, color, (prev_y, prev_x), (y, x), 3)
                prev_x, prev_y = x, y

    first = True

    pygame.draw.circle(WIN, (0, 255, 0), (x_mouse, y_mouse), 5)
    pygame.draw.circle(WIN, (255, 0, 0), (WIDTH//2, HEIGHT//2), 5)
    pygame.display.update()