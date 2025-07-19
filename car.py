import pygame
import random

pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Simple Car Dodge Game")
clock = pygame.time.Clock()

car = pygame.Rect(190, 360, 20, 40)
obstacles = []
score = 0
font = pygame.font.Font(None, 36)

def reset_game():
    global car, obstacles, score
    car.topleft = (190, 360)
    obstacles.clear()
    score = 0

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # FIXED here
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car.left > 0:
        car.x -= 5  # FIXED: move left
    if keys[pygame.K_RIGHT] and car.right < 400:
        car.x += 5  # NEW: move right

    # Increase difficulty as score rises
    spawn_rate = 0.02 + (score * 0.002)
    if random.random() < spawn_rate:
        obstacles.append(pygame.Rect(random.randrange(0, 380, 20), -40, 20, 40))

    for obs in obstacles[:]:
        obs.y += 4 + (score // 10)
        if obs.top > 400:
            obstacles.remove(obs)
            score += 1
        if car.colliderect(obs):
            reset_game()

    # Drawing everything
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 255), car)
    for obs in obstacles:
        pygame.draw.rect(screen, (255, 0, 0), obs)
    score_text = font.render(f'Score: {score}', True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
