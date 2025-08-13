import pygame
import sys
from checkers import Game, SQUARE_SIZE, BLACK
from ai import minimax

WIDTH, HEIGHT = 800, 800

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def menu_screen(win):
    font = pygame.font.SysFont("comicsans", 50)
    run = True
    mode = None

    while run:
        win.fill((30, 30, 30))
        title = font.render("CHECKERS", True, (255, 255, 255))
        pvp = font.render("1. Player vs Player", True, (200, 200, 200))
        pvai = font.render("2. Player vs AI", True, (200, 200, 200))
        win.blit(title, (WIDTH//2 - title.get_width()//2, 200))
        win.blit(pvp, (WIDTH//2 - pvp.get_width()//2, 350))
        win.blit(pvai, (WIDTH//2 - pvai.get_width()//2, 450))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mode = "pvp"
                    run = False
                elif event.key == pygame.K_2:
                    mode = "pvai"
                    run = False
    return mode

def main():
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Checkers")
    clock = pygame.time.Clock()

    mode = menu_screen(WIN)
    game = Game(WIN)

    run = True
    while run:
        clock.tick(60)

        if game.board.winner() is not None:
            print(f"{game.board.winner()} wins!")
            run = False

        if mode == "pvai" and game.turn == BLACK:
            value, new_board = minimax(game.board, 3, True, game)
            game.board = new_board
            game.change_turn()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
