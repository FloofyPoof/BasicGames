import time
import random
import pygame
pygame.font.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hello")

BG = pygame.transform.scale(pygame.image.load("sky.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40
PLAYER_VEL = 5
PROJECTILE_WIDTH = 15
PROJECTILE_HEIGHT = 25
PROJECTILE_VEL = 3

FONT = pygame.font.SysFont("comicsans", 30)

def draw(player, elapsed_time, projectiles):
    WIN.blit(BG, (0,0))

    time_text = FONT.render(f"Time {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, (255, 0, 0), player)

    for projectile in projectiles:
        pygame.draw.rect(WIN, 'white', projectile)

    pygame.display.update()

def main():
    run = True

    player = pygame.Rect(WIDTH/2, HEIGHT/2, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    projectile_add_increment = 2000
    projectile_count = 0

    projectiles = []
    hit = False

    while run:
        projectile_count += clock.tick(60)
        keys = pygame.key.get_pressed()
        elapsed_time = time.time() - start_time

        if projectile_count > projectile_add_increment:
            for _ in range(3):
                projectile_x = random.randint(0, WIDTH - PROJECTILE_WIDTH)
                projectile = pygame.Rect(projectile_x, -PROJECTILE_HEIGHT, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
                projectiles.append(projectile)

            projectile_add_increment = max(200, projectile_add_increment - 50)
            projectile_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_f]:
                run = False
                break

        if keys[pygame.K_a] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_d] and player.x + player.width + PLAYER_VEL <= WIDTH:
            player.x += PLAYER_VEL
        if keys[pygame.K_w] and player.y - PLAYER_VEL >= 0:
            player.y -= PLAYER_VEL
        if keys[pygame.K_s] and player.y + player.height + PLAYER_VEL <= HEIGHT:
            player.y += PLAYER_VEL

        for projectile in projectiles[:]:
            projectile.y += PROJECTILE_VEL
            if projectile.y > HEIGHT:
                projectiles.remove(projectile)
            elif projectile.y + projectile.height >= player.y and projectile.colliderect(player):
                projectiles.remove(projectile)
                hit = True
                break

        if hit:
            lost_text = FONT.render('You lost!', 1, 'red')
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)
            break

        draw(player, elapsed_time, projectiles)

    pygame.quit()

if __name__ == "__main__":
    main()