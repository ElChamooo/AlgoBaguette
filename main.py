import os
import pygame
from game.settings import WINDOW_WIDTH, WINDOW_HEIGHT
from ui.menu import main_menu
from ui.settings_menu import settings_menu
from snake import main_game

# Paramètres globaux
game_settings = {"game_speed": 5, "apple_count": 1}  # Valeurs par défaut

def main():
    pygame.init()
    # Initialiser la fenêtre en mode plein écran
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # (0, 0) pour s'adapter à la résolution de l'écran
    pygame.display.set_caption("Snake Game")

    while True:
        action = main_menu(screen)  # Passer l'écran aux menus
        if action == "play":
            main_game(screen, game_settings["game_speed"], game_settings["apple_count"])
        elif action == "settings":
            game_settings.update(settings_menu(screen, game_settings))  # Passer l'écran aux paramètres
        elif action == "exit":
            break

    pygame.quit()

if __name__ == "__main__":
    main()

