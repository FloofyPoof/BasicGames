import pygame
import random

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Rope test')
BG = pygame.transform.scale(pygame.image.load('sky.jpg'), (WIDTH, HEIGHT))
draw_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
cork = []
rect_cork = pygame.Rect(WIDTH/10, HEIGHT/10, WIDTH*8/10, HEIGHT*8/10)
cork.append(rect_cork)

def onCork():
    # bool
    pass

def draw(entities):
    WIN.blit(BG, (0,0))
    for entity in entities:
        if type(entity) is pygame.Rect:
            pygame.draw.rect(draw_surf, pygame.Color(0, 0, 255, 100), entity, 3)
        if type(entity) is tuple:
            pygame.draw.circle(draw_surf, pygame.Color(255, 0, 0, 200), entity, 5)

    WIN.blit(draw_surf, (0,0))

    pygame.display.update()

def main():
    run = True
    Y_START = random.randint(HEIGHT//10, HEIGHT*8//10)
    Y_FINISH = random.randint(HEIGHT//10, HEIGHT*8//10)

    entities = []
    entities.extend(cork)
    entities.append((WIDTH/10, Y_START))
    entities.append((WIDTH*9/10, Y_FINISH))

    while run:
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                run = False
                break

        draw(entities)

    pygame.quit()

if __name__ == "__main__":
    main()