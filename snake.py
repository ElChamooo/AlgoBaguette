import pygame
import random

pygame.init()
pygame.font.init()

# Dimensions de la fenêtre
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 200
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

#scoreboard
SCORE = 0
font = pygame.font.SysFont('Arial', 18)
font = pygame.font.Font('font.ttf', 18)

# Create window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT + CELL_SIZE))
pygame.display.set_caption("Snake Game")

def draw_grid():
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        for y in range(CELL_SIZE, WINDOW_HEIGHT + CELL_SIZE, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)

def draw_snake(snake):
    for x, y in snake:
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GREEN, rect)

def draw_apple(apple):
    x, y = apple
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, RED, rect)

def draw_scoreboard():
    score_text = font.render(f"Score: {SCORE}", True, (255, 255, 255))
    text_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 8))
    screen.blit(score_text, text_rect)

def generate_apple(grid_width, grid_height, snake):
    while True:
        x = random.randint(0, grid_width - 1)
        y = random.randint(1, grid_height - 1)
        if (x, y) not in snake:
            return (x, y)

# Game initialization
grid_width = WINDOW_WIDTH // CELL_SIZE
grid_height = (WINDOW_HEIGHT) // CELL_SIZE
snake = [(5, 5), (4, 5)]
direction = 'right'
apples = [generate_apple(grid_width, grid_height, snake)]
last_apple_score = 0

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

    # Move the snake
    head_x, head_y = snake[0]
    if direction == 'up':
        new_head = (head_x, head_y - 1)
    elif direction == 'down':
        new_head = (head_x, head_y + 1)
    elif direction == 'left':
        new_head = (head_x - 1, head_y)
    elif direction == 'right':
        new_head = (head_x + 1, head_y)

    # Check collisions
    if new_head in snake or new_head[0] < 0 or new_head[1] < 1 or new_head[0] >= grid_width or new_head[1] >= grid_height:
        print("Game Over!")
        running = False
        continue

    snake.insert(0, new_head)
    ate_apple = False
    for i, apple in enumerate(apples):
        if new_head == apple:
            apples[i] = generate_apple(grid_width, grid_height, snake)
            SCORE += 1
            ate_apple = True
    if not ate_apple:
        snake.pop()

    # Add a new apple every time the score increase by 10
    if SCORE // 10 > last_apple_score:
        apples.append(generate_apple(grid_width, grid_height, snake))
        last_apple_score = SCORE // 10

    screen.fill(BLACK)
    draw_grid()
    draw_snake(snake)
    for apple in apples:
        draw_apple(apple)
    draw_scoreboard()
    pygame.display.flip()

    clock.tick(3)

pygame.quit()