import pygame
import sys
import subprocess
import os

pygame.init()

# Window setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game Launcher")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
LIGHT_BLUE = (100, 180, 255)

# Fonts
title_font = pygame.font.SysFont("Arial", 64, bold=True)
button_font = pygame.font.SysFont("Arial", 36, bold=True)

# Buttons (text, rect)
buttons = {
    "Play vs AI": pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 60, 300, 60),
    "Play vs Human": pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 20, 300, 60)
}

def draw_menu():
    screen.fill(WHITE)

    # Title
    title_surface = title_font.render("Chess Game", True, BLACK)
    screen.blit(title_surface, (WIDTH//2 - title_surface.get_width()//2, 100))

    # Buttons
    mouse_pos = pygame.mouse.get_pos()
    for text, rect in buttons.items():
        color = LIGHT_BLUE if rect.collidepoint(mouse_pos) else GRAY
        pygame.draw.rect(screen, color, rect, border_radius=10)
        label = button_font.render(text, True, BLACK)
        screen.blit(label, (rect.centerx - label.get_width()//2, rect.centery - label.get_height()//2))

    pygame.display.flip()

def run_game(script_path):
    """Launch another Python script in the correct folder."""
    pygame.quit()
    abs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_path)
    subprocess.run(["python", abs_path])
    sys.exit()

def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for text, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        if text == "Play vs AI":
                            run_game("ai/ai_bot.py")
                        elif text == "Play vs Human":
                            run_game("gui/pygame_gui.py")

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
