import pygame
import sys
from tic_tac_toe_ai import TicTacToeAI
from tic_tac_toe_human import TicTacToeHuman

pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
GREEN = (60, 179, 113)
RED = (220, 20, 60)
GRAY = (200, 200, 200)

# Font
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 32)

# Button setup
buttons = [
    {"label": "Play vs AI", "color": BLUE, "rect": pygame.Rect(150, 100, 300, 60), "action": "ai"},
    {"label": "Play vs Human", "color": GREEN, "rect": pygame.Rect(150, 180, 300, 60), "action": "human"},
    {"label": "Exit", "color": RED, "rect": pygame.Rect(150, 260, 300, 60), "action": "exit"},
]

def draw_menu():
    screen.fill(WHITE)

    # Title
    title_text = font.render("TIC TAC TOE", True, BLACK)
    screen.blit(title_text, title_text.get_rect(center=(WIDTH//2, 40)))

    # Buttons
    mouse_pos = pygame.mouse.get_pos()
    for button in buttons:
        rect = button["rect"]
        color = button["color"]
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, GRAY, rect)
        else:
            pygame.draw.rect(screen, color, rect)
        
        text = small_font.render(button["label"], True, WHITE)
        screen.blit(text, text.get_rect(center=rect.center))

def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        draw_menu()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    if button["rect"].collidepoint(event.pos):
                        if button["action"] == "ai":
                            pygame.quit()
                            TicTacToeAI().play()
                            pygame.init()
                        elif button["action"] == "human":
                            pygame.quit()
                            TicTacToeHuman().play()
                            pygame.init()
                        elif button["action"] == "exit":
                            running = False

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
