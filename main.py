# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minimax.algorithm import minimax

FPS = 60

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

# Difficulty button definitions: (label, depth, normal_color, hover_color)
DIFFICULTY_BUTTONS = [
    ("Easy",   2, (0, 180, 0),   (0, 220, 0)),
    ("Medium", 4, (220, 160, 0), (255, 190, 0)),
    ("Hard",   6, (200, 0, 0),   (240, 0, 0)),
]

BUTTON_W, BUTTON_H = 250, 60
BUTTON_SPACING = 20
MENU_VERTICAL_OFFSET = 60
MENU_BG = (30, 30, 30)


def draw_menu(win):
    """Display the difficulty selection menu and return the chosen depth value."""
    title_font = pygame.font.SysFont(None, 80)
    subtitle_font = pygame.font.SysFont(None, 48)
    btn_font = pygame.font.SysFont(None, 44)

    clock = pygame.time.Clock()

    # Vertical layout: title, subtitle, then buttons spaced evenly
    total_buttons_height = len(DIFFICULTY_BUTTONS) * BUTTON_H + (len(DIFFICULTY_BUTTONS) - 1) * BUTTON_SPACING
    start_y = HEIGHT // 2 - total_buttons_height // 2 + MENU_VERTICAL_OFFSET

    button_rects = []
    for i in range(len(DIFFICULTY_BUTTONS)):
        rect = pygame.Rect(
            WIDTH // 2 - BUTTON_W // 2,
            start_y + i * (BUTTON_H + BUTTON_SPACING),
            BUTTON_W,
            BUTTON_H,
        )
        button_rects.append(rect)

    while True:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(mouse_pos):
                        return DIFFICULTY_BUTTONS[i][1]  # return depth

        # Draw background
        win.fill(MENU_BG)

        # Draw title
        title_surf = title_font.render("Python Checkers", True, (255, 255, 255))
        win.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, HEIGHT // 4 - title_surf.get_height() // 2))

        # Draw subtitle
        sub_surf = subtitle_font.render("Select Difficulty", True, (200, 200, 200))
        win.blit(sub_surf, (WIDTH // 2 - sub_surf.get_width() // 2, HEIGHT // 4 + title_surf.get_height() // 2 + 10))

        # Draw buttons
        for i, (label, depth, color, hover_color) in enumerate(DIFFICULTY_BUTTONS):
            rect = button_rects[i]
            current_color = hover_color if rect.collidepoint(mouse_pos) else color
            pygame.draw.rect(win, current_color, rect, border_radius=8)
            pygame.draw.rect(win, (255, 255, 255), rect, width=2, border_radius=8)
            btn_surf = btn_font.render(label, True, (255, 255, 255))
            win.blit(btn_surf, (rect.centerx - btn_surf.get_width() // 2, rect.centery - btn_surf.get_height() // 2))

        pygame.display.update()


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main(depth):
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), depth, WHITE, float('-inf'), float('inf'))
            game.ai_move(new_board)

        if game.winner() != None:
            winner = game.winner()
            if winner == RED:
                msg = "RED Wins!"
            else:
                msg = "WHITE Wins!"
            font = pygame.font.SysFont(None, 72)
            text = font.render(msg, True, winner, (0, 0, 0))
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(3000)
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()


while True:
    selected_depth = draw_menu(WIN)
    main(selected_depth)