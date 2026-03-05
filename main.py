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
    """Display the difficulty selection menu and return (depth, label) for the chosen difficulty."""
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
                        label, depth = DIFFICULTY_BUTTONS[i][0], DIFFICULTY_BUTTONS[i][1]
                        return (depth, label)

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


def draw_game_over(win, winner_color, game, difficulty_label):
    """Display the game-over screen and return 'menu' or 'quit'."""
    clock = pygame.time.Clock()

    winner_font = pygame.font.SysFont(None, 80)
    stats_font = pygame.font.SysFont(None, 36)
    btn_font = pygame.font.SysFont(None, 44)

    # Determine winner text and color
    if winner_color == RED:
        winner_text = "RED Wins!"
        text_color = RED
    elif winner_color == WHITE:
        winner_text = "WHITE Wins!"
        text_color = WHITE
    else:
        winner_text = "It's a Draw!"
        text_color = (255, 220, 0)

    # Piece counts from the board
    board = game.get_board()
    red_pieces = board.red_left
    white_pieces = board.white_left

    stats_text = f"RED: {red_pieces} pieces  |  WHITE: {white_pieces} pieces"
    diff_text = f"Difficulty: {difficulty_label}"

    # Button definitions: (label, action, normal_color, hover_color)
    GAMEOVER_BUTTONS = [
        ("Play Again", "menu", (0, 180, 0),   (0, 220, 0)),
        ("Quit",       "quit", (200, 0, 0),   (240, 0, 0)),
    ]

    btn_spacing = 20
    total_btn_height = len(GAMEOVER_BUTTONS) * BUTTON_H + (len(GAMEOVER_BUTTONS) - 1) * btn_spacing
    btn_start_y = HEIGHT // 2 + 80

    button_rects = []
    for i in range(len(GAMEOVER_BUTTONS)):
        rect = pygame.Rect(
            WIDTH // 2 - BUTTON_W // 2,
            btn_start_y + i * (BUTTON_H + btn_spacing),
            BUTTON_W,
            BUTTON_H,
        )
        button_rects.append(rect)

    # Semi-transparent overlay surface
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))

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
                        return GAMEOVER_BUTTONS[i][1]  # return action string

        # Draw overlay on top of whatever is already on the window
        win.blit(overlay, (0, 0))

        # Winner announcement
        winner_surf = winner_font.render(winner_text, True, text_color)
        win.blit(winner_surf, (WIDTH // 2 - winner_surf.get_width() // 2, HEIGHT // 2 - 160))

        # Stats
        stats_surf = stats_font.render(stats_text, True, (200, 200, 200))
        win.blit(stats_surf, (WIDTH // 2 - stats_surf.get_width() // 2, HEIGHT // 2 - 60))

        diff_surf = stats_font.render(diff_text, True, (200, 200, 200))
        win.blit(diff_surf, (WIDTH // 2 - diff_surf.get_width() // 2, HEIGHT // 2 - 10))

        # Buttons
        for i, (label, action, color, hover_color) in enumerate(GAMEOVER_BUTTONS):
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


def main(depth, difficulty_label):
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
            game.update()
            return draw_game_over(WIN, winner, game, difficulty_label)

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
    selected_depth, difficulty_label = draw_menu(WIN)
    result = main(selected_depth, difficulty_label)
    if result == "quit":
        pygame.quit()
        raise SystemExit