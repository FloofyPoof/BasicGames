import time
import random
import pygame
pygame.font.init()
#add projectile angle later
#add AI

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('My version')

BG = pygame.transform.scale(pygame.image.load('sky.jpg'), (WIDTH, HEIGHT))

PLAYER_RAD = 20
PLAYER_VEL = 5
PROJ_RAD = 10
PROJ_VEL = 3

FONT = pygame.font.SysFont('comicsans', 30)

def draw(player, elapsed_time, projectiles):
    WIN.blit(BG, (0,0))

    time_text = FONT.render(f"Time {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    pygame.draw.circle(WIN, 'red', (player[0], player[1]), player[2])

    for proj in projectiles:
        pygame.draw.circle(WIN, 'blue', (proj[0], proj[1]), proj[2])

    pygame.display.update()

def overlap(player, proj):
    return (player[0] - proj[0]) ** 2 + (player[1] - proj[1]) ** 2 < (player[2] + proj[2] - 5) ** 2

def main():
    run = True

    player = [WIDTH/2, HEIGHT/2, PLAYER_RAD]

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    projectile_add_increment = 1000
    projectile_count = 0
    hit = False

    projectiles = []
    for _ in range(3):
        proj_x = random.randint(0, WIDTH)
        proj = [proj_x, 0, PROJ_RAD]
        projectiles.append(proj)

    while run:
        projectile_count += clock.tick(60)
        keys = pygame.key.get_pressed()
        elapsed_time = time.time() - start_time

        if projectile_count > projectile_add_increment:
            for _ in range(3):
                proj_x = random.randint(0, WIDTH)
                proj = [proj_x, 0, PROJ_RAD]
                projectiles.append(proj)

            projectile_add_increment = max(200, projectile_add_increment - 100)
            projectile_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_f]:
                run = False
                break

        if keys[pygame.K_a] and player[0] - PLAYER_VEL >= 0:
            player[0] -= PLAYER_VEL
        if keys[pygame.K_d] and player[0] + PLAYER_VEL <= WIDTH:
            player[0] += PLAYER_VEL
        if keys[pygame.K_w] and player[1] - PLAYER_VEL >= 0:
            player[1] -= PLAYER_VEL
        if keys[pygame.K_s] and player[1] + PLAYER_VEL <= HEIGHT:
            player[1] += PLAYER_VEL

        for proj in projectiles[:]:
            proj[1] += PROJ_VEL
            if proj[1] > HEIGHT:
                projectiles.remove(proj)
            if overlap(player, proj):
                hit = True
                break

        if hit:
            lost_text = FONT.render('You lost!', 1, 'red')
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(500)
            break

        draw(player, elapsed_time, projectiles)

    pygame.quit()
    print(f'Your score was {elapsed_time}!')

if __name__ == "__main__":
    main()