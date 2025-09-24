import pygame
import random

pygame.init()

# Dimensions de la fenêtre
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 200
CELL_SIZE = 20

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Créer la fenêtre
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")

def draw_grid():
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)

def draw_snake(snake):
    for x, y in snake:
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GREEN, rect)

def draw_apples(apples):
    for apple in apples:
        x, y = apple
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, rect)

def generate_apples(grid_width, grid_height, snake, apple_count):
    apples = []
    while len(apples) < apple_count:
        x = random.randint(0, grid_width - 1)
        y = random.randint(0, grid_height - 1)
        if (x, y) not in snake and (x, y) not in apples:
            apples.append((x, y))
    return apples

def main_game(game_speed, apple_count):
    # Initialisation du jeu
    grid_width = WINDOW_WIDTH // CELL_SIZE
    grid_height = WINDOW_HEIGHT // CELL_SIZE
    snake = [(5, 5), (4, 5)]
    direction = 'right'
    apples = generate_apples(grid_width, grid_height, snake, apple_count)

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'down':
                    direction = 'up'
                elif event.key == pygame.K_DOWN and direction != 'up':
                    direction = 'down'
                elif event.key == pygame.K_LEFT and direction != 'right':
                    direction = 'left'
                elif event.key == pygame.K_RIGHT and direction != 'left':
                    direction = 'right'

        # Déplacer le serpent
        head_x, head_y = snake[0]
        if direction == 'up':
            new_head = (head_x, head_y - 1)
        elif direction == 'down':
            new_head = (head_x, head_y + 1)
        elif direction == 'left':
            new_head = (head_x - 1, head_y)
        elif direction == 'right':
            new_head = (head_x + 1, head_y)

        # Vérifier les collisions
        if new_head in snake or new_head[0] < 0 or new_head[1] < 0 or new_head[0] >= grid_width or new_head[1] >= grid_height:
            print("Game Over!")
            running = False
            continue

        snake.insert(0, new_head)
        if new_head in apples:
            apples.remove(new_head)
            apples.extend(generate_apples(grid_width, grid_height, snake, apple_count - len(apples)))
        else:
            snake.pop()

        screen.fill(BLACK)
        draw_grid()
        draw_snake(snake)
        draw_apples(apples)
        pygame.display.flip()

        clock.tick(game_speed)

pygame.quit()