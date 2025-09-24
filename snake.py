import pygame
import random

pygame.init()

# window dimensions & cell size (can be changed)
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
CELL_SIZE = 50

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Créer la fenêtre
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")

# load textures
background_texture = pygame.image.load("textures/background2.png")
background_texture = pygame.transform.scale(background_texture, (CELL_SIZE, CELL_SIZE)) # scale to cell size
apple_texture = pygame.image.load("textures/apple.png")
apple_texture = pygame.transform.scale(apple_texture, (CELL_SIZE, CELL_SIZE)) # scale to cell size

# Load snake textures
snake_head_texture = pygame.image.load("textures/head.png")
snake_head_texture = pygame.transform.scale(snake_head_texture, (CELL_SIZE, CELL_SIZE))
snake_eat_texture = pygame.image.load("textures/eat.png")
snake_eat_texture = pygame.transform.scale(snake_eat_texture, (CELL_SIZE, CELL_SIZE))
snake_body_texture = pygame.image.load("textures/body.png")
snake_body_texture = pygame.transform.scale(snake_body_texture, (CELL_SIZE, CELL_SIZE))
snake_tail_texture = pygame.image.load("textures/end.png")
snake_tail_texture = pygame.transform.scale(snake_tail_texture, (CELL_SIZE, CELL_SIZE))
snake_left_texture = pygame.image.load("textures/left.png")
snake_left_texture = pygame.transform.scale(snake_left_texture, (CELL_SIZE, CELL_SIZE))
snake_right_texture = pygame.image.load("textures/right.png")
snake_right_texture = pygame.transform.scale(snake_right_texture, (CELL_SIZE, CELL_SIZE))

def get_direction(from_pos, to_pos):
    """Get direction from one position to another"""
    dx = to_pos[0] - from_pos[0]
    dy = to_pos[1] - from_pos[1]
    
    if dx == 1: return 'right'
    elif dx == -1: return 'left'
    elif dy == 1: return 'down'
    elif dy == -1: return 'up'
    return None

def draw_grid():
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            screen.blit(background_texture, (x, y)) # draw bkg texture

def draw_snake(snake, is_eating=False):
    if len(snake) == 0:
        return
    
    for i, (x, y) in enumerate(snake):
        pos_x = x * CELL_SIZE
        pos_y = y * CELL_SIZE
        
        if i == 0:  # Head
            # Use eating texture if snake is eating, otherwise normal head
            if is_eating:
                # Determine head direction for eat texture rotation
                if len(snake) > 1:
                    head_dir = get_direction(snake[1], snake[0])
                else:
                    head_dir = direction
                
                texture = snake_eat_texture
                if head_dir == 'up':
                    texture = pygame.transform.rotate(snake_eat_texture, -90)
                elif head_dir == 'down':
                    texture = pygame.transform.rotate(snake_eat_texture, 90)
                elif head_dir == 'right':
                    texture = pygame.transform.rotate(snake_eat_texture, 180)
                # left is default orientation
            else:
                # Normal head logic
                if len(snake) > 1:
                    head_dir = get_direction(snake[1], snake[0])
                else:
                    head_dir = direction
                
                texture = snake_head_texture
                if head_dir == 'up':
                    texture = pygame.transform.rotate(snake_head_texture, -90)
                elif head_dir == 'down':
                    texture = pygame.transform.rotate(snake_head_texture, 90)
                elif head_dir == 'right':
                    texture = pygame.transform.rotate(snake_head_texture, 180)
                # left is default orientation
            
            screen.blit(texture, (pos_x, pos_y))
            
        elif i == len(snake) - 1:  # Tail
            # Determine tail direction based on previous segment
            tail_dir = get_direction(snake[i], snake[i-1])
            
            texture = snake_tail_texture
            if tail_dir == 'up':
                texture = pygame.transform.rotate(snake_tail_texture, -90)
            elif tail_dir == 'down':
                texture = pygame.transform.rotate(snake_tail_texture, 90)
            elif tail_dir == 'right':
                texture = pygame.transform.rotate(snake_tail_texture, 180)
            # left is default orientation (from left side)
            
            screen.blit(texture, (pos_x, pos_y))
            
        else:  # Body segments
            # Determine directions from previous and to next segment
            from_dir = get_direction(snake[i+1], snake[i])
            to_dir = get_direction(snake[i], snake[i-1])
            
            # Check if this is a turn segment
            if from_dir != to_dir:
                # This is a turn segment, use left.png or right.png
                if (from_dir == 'up' and to_dir == 'right') or (from_dir == 'left' and to_dir == 'down'):
                    # Bottom to right turn
                    texture = snake_right_texture
                elif (from_dir == 'up' and to_dir == 'left') or (from_dir == 'right' and to_dir == 'down'):
                    # Bottom to left turn
                    texture = snake_left_texture
                elif (from_dir == 'down' and to_dir == 'right') or (from_dir == 'left' and to_dir == 'up'):
                    # Top to right turn
                    texture = pygame.transform.rotate(snake_right_texture, 90)
                elif (from_dir == 'down' and to_dir == 'left') or (from_dir == 'right' and to_dir == 'up'):
                    # Top to left turn
                    texture = pygame.transform.rotate(snake_left_texture, -90)
                else:
                    texture = snake_body_texture
            else:
                # Straight body segment
                texture = snake_body_texture
                if from_dir in ['up', 'down']:
                    # Vertical body segment
                    texture = pygame.transform.rotate(snake_body_texture, 90)
                # horizontal is default orientation
            
            screen.blit(texture, (pos_x, pos_y))

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
