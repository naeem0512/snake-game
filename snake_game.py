import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Define colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Define display dimensions
display_width = 600
display_height = 400

# Create the display
display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game')

# Define clock for controlling the frame rate
clock = pygame.time.Clock()

# Define snake block size and speed
snake_block = 10
initial_speed = 15

# Define font style
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Load sounds
eat_sound = pygame.mixer.Sound("eat_sound.wav")
game_over_sound = pygame.mixer.Sound("game_over_sound.wav")

# Load high score
try:
    with open("high_score.txt", "r") as f:
        high_score = int(f.read())
except FileNotFoundError:
    high_score = 0

def save_high_score(score):
    global high_score
    if score > high_score:
        high_score = score
        with open("high_score.txt", "w") as f:
            f.write(str(high_score))

def score_display(score):
    value = score_font.render(f"Your Score: {score}  High Score: {high_score}", True, black)
    display.blit(value, [0, 0])

def snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(display, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color, y_offset=0):
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [display_width / 6, display_height / 3 + y_offset])

def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        message("Game Paused. Press P to Resume or Q to Quit.", yellow)
        pygame.display.update()
        clock.tick(5)

def game_over_screen(score):
    display.fill(blue)
    message("Game Over! Press C to Play Again or Q to Quit", red, -30)
    message(f"Your Score: {score}", white, 10)
    message(f"High Score: {high_score}", white, 50)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_c:
                    return

def main_menu():
    menu = True
    while menu:
        display.fill(blue)
        message("Welcome to Snake Game! Press S to Start or Q to Quit", yellow, -30)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    menu = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def game_loop():
    game_over = False
    game_close = False
    pause = False

    x1 = display_width / 2
    y1 = display_height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0

    snake_speed = initial_speed
    level = 1

    while not game_over:

        while game_close:
            game_over_screen(length_of_snake - 1)
            save_high_score(length_of_snake - 1)
            game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_p:
                    pause_game()

        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
            pygame.mixer.Sound.play(game_over_sound)
            game_close = True

        x1 += x1_change
        y1 += y1_change
        display.fill(blue)
        pygame.draw.rect(display, green, [foodx, foody, snake_block, snake_block])
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                pygame.mixer.Sound.play(game_over_sound)
                game_close = True

        snake(snake_block, snake_list)
        score_display(length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            pygame.mixer.Sound.play(eat_sound)
            foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1
            if length_of_snake % 5 == 0:
                level += 1
                snake_speed += 2

        clock.tick(snake_speed)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main_menu()
    game_loop()

