import pygame
from game.settings import WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, BLACK, GRAY, DARK_GRAY
from ui.settings_menu import settings_menu  # Importer le menu des paramètres

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game - Menu")
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        screen.fill(BLACK)
        title = font.render("Snake Game", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 50))
        screen.blit(title, title_rect)

        # Définir les boutons
        buttons = [
            {"label": "Play", "rect": pygame.Rect(WINDOW_WIDTH // 2 - 60, 100, 120, 40)},
            {"label": "Settings", "rect": pygame.Rect(WINDOW_WIDTH // 2 - 60, 160, 120, 40)},
            {"label": "Exit", "rect": pygame.Rect(WINDOW_WIDTH // 2 - 60, 220, 120, 40)},
        ]

        # Dessiner les boutons
        for button in buttons:
            pygame.draw.rect(screen, GRAY, button["rect"])
            pygame.draw.rect(screen, DARK_GRAY, button["rect"], 2)
            text = font.render(button["label"], True, BLACK)
            text_rect = text.get_rect(center=button["rect"].center)
            screen.blit(text, text_rect)

        pygame.display.flip()

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for button in buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        if button["label"] == "Play":
                            return "play"
                        elif button["label"] == "Settings":
                            return "settings"
                        elif button["label"] == "Exit":
                            return "exit"

    pygame.quit()
    return "exit"