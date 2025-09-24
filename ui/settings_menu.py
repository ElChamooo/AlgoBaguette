import pygame
from game.settings import WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, BLACK, GRAY, DARK_GRAY

def draw_slider(screen, x, y, width, value, min_value, max_value, label, font):
    """Dessine une slide bar."""
    pygame.draw.rect(screen, GRAY, (x, y, width, 10))  # Barre de fond
    slider_x = x + int((value - min_value) / (max_value - min_value) * width)
    pygame.draw.circle(screen, DARK_GRAY, (slider_x, y + 5), 8)  # Curseur
    text = font.render(f"{label}: {value}", True, WHITE)
    screen.blit(text, (x, y - 30))

def settings_menu(current_settings):
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game - Settings")
    font = pygame.font.Font(None, 36)

    # Charger les paramètres actuels
    game_speed = current_settings["game_speed"]
    apple_count = current_settings["apple_count"]

    # Valeurs minimales et maximales
    game_speed_min, game_speed_max = 1, 10
    apple_count_min, apple_count_max = 1, 5

    running = True
    while running:
        screen.fill(BLACK)
        title = font.render("Settings", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 50))
        screen.blit(title, title_rect)

        # Dessiner les sliders
        draw_slider(screen, 100, 120, 200, game_speed, game_speed_min, game_speed_max, "Game Speed", font)
        draw_slider(screen, 100, 200, 200, apple_count, apple_count_min, apple_count_max, "Apple Count", font)

        # Bouton "Back"
        back_button = pygame.Rect(WINDOW_WIDTH // 2 - 60, 280, 120, 40)
        pygame.draw.rect(screen, GRAY, back_button)
        pygame.draw.rect(screen, DARK_GRAY, back_button, 2)
        back_text = font.render("Back", True, BLACK)
        back_text_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_text_rect)

        pygame.display.flip()

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Vérifier si le bouton "Back" est cliqué
                if back_button.collidepoint(mouse_pos):
                    return {"game_speed": game_speed, "apple_count": apple_count}
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                # Ajuster la valeur de game_speed si la souris est sur le slider
                if 100 <= mouse_pos[0] <= 300 and 115 <= mouse_pos[1] <= 125:
                    game_speed = int((mouse_pos[0] - 100) / 200 * (game_speed_max - game_speed_min) + game_speed_min)
                # Ajuster la valeur de apple_count si la souris est sur le slider
                if 100 <= mouse_pos[0] <= 300 and 195 <= mouse_pos[1] <= 205:
                    apple_count = int((mouse_pos[0] - 100) / 200 * (apple_count_max - apple_count_min) + apple_count_min)

    pygame.quit()
    return {"game_speed": game_speed, "apple_count": apple_count}