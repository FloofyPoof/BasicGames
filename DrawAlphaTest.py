# from https://github.com/pygame/pygame/issues/2178
import pygame

#pygame.init() # this is slow AF, why even use this

window_surf = pygame.display.set_mode((800, 600))

# Setup a background
background_surf = pygame.image.load('sky.jpg')

# Setup an drawing surface with alpha
draw_surf = pygame.Surface((800, 600), pygame.SRCALPHA)
draw_surf.fill(pygame.Color('#00000000'))

# Draw shapes with alpha
pygame.draw.line(draw_surf, pygame.Color(255, 0, 0, 50), (1000, 1000), (-1000, -1000))
pygame.draw.aaline(draw_surf, pygame.Color(255, 0, 0, 150), (400, 1000), (400, -1000))
pygame.draw.circle(draw_surf, pygame.Color(255, 0, 0, 120), (600, 500), 50)

clock = pygame.time.Clock()
running = True

while running:
    frame_time = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window_surf.blit(background_surf, (0, 0))
    window_surf.blit(draw_surf, (0, 0))

    pygame.display.update()