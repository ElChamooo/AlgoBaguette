import pygame
from ui.menu import main_menu
from ui.settings_menu import settings_menu
from snake import main_game

# global settings
game_settings = {"game_speed": 5, "apple_count": 1}  # default values

def main():
    pygame.init()

    while True:
        action = main_menu()
        if action == "play":
            main_game(game_settings["game_speed"], game_settings["apple_count"])
        elif action == "settings":
            game_settings.update(settings_menu(game_settings))  # Update global settings
        elif action == "exit":
            break

    pygame.quit()

if __name__ == "__main__":
    main()

