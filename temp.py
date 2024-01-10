import pygame
import sys
import random
from pygame_textinput import TextInput

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
FPS = 60
WHITE = (255, 255, 255)
GROUND_HEIGHT = 50
BIRD_SIZE = (34, 24)  # Bird image size
GRAVITY = 0.6
JUMP_STRENGTH = -10
PIPE_WIDTH = 50
PIPE_COLOR = (0, 255, 0)  # Green
LEADERBOARD_FILE = "leaderboard.txt"

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Set up the clock
clock = pygame.time.Clock()

# Load images
background_image = pygame.image.load('background.jpg')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

bird_image = pygame.image.load('bird.png')
bird_image = pygame.transform.scale(bird_image, BIRD_SIZE)

ground_image = pygame.image.load('ground.png')
ground_image = pygame.transform.scale(ground_image, (WIDTH, GROUND_HEIGHT))

# Fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# Game states
START_SCREEN = 0
GAME_RUNNING = 1
GAME_OVER = 2
LEADERBOARD_SCREEN = 3
game_state = START_SCREEN

# Bird
bird_rect = bird_image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
bird_speed = 0

# Pipes
pipes = []
pipe_gap = 150
pipe_speed = 5
pipe_frequency = 60
pipe_counter = 0

# Ground
ground_rect = ground_image.get_rect(topleft=(0, HEIGHT - GROUND_HEIGHT))

# Score
score = 0

# Player name
player_name = ""

# Leaderboard
leaderboard = []

# Text input
textinput = TextInput()

def get_player_name():
  global screen
  input_box = pygame.Rect(Const.WIDTH//4, Const.HEIGHT//2, Const.WIDTH//2, 32)
  color_inactive = pygame.Color('lightskyblue3')
  color_active = pygame.Color('dodgerblue2')
  color = color_inactive
  active = False
  text = ''
  font = pygame.font.Font(None, 32)
  input_text = font.render(text, True, color)
  input_text_rect = input_text.get_rect()
  input_text_rect.x = input_box.x
  input_text_rect.y = input_box.y

  return_text = font.render("Enter your name and press Enter:", True, (255, 255, 255))
  return_text_rect = return_text.get_rect(center=(Const.WIDTH // 2, Const.HEIGHT // 3))
  screen.blit(return_text, return_text_rect)

  while True:
      for event in pygame.event.get():
          if event.type == pygame.KEYDOWN:
              if active:
                  if event.key == pygame.K_RETURN:
                      player_name = text
                      return player_name
                  elif event.key == pygame.K_BACKSPACE:
                      text = text[:-1]
                  else:
                      text += event.unicode
                  input_text = font.render(text, True, color)
          elif event.type == pygame.MOUSEBUTTONDOWN:
              if input_box.collidepoint(event.pos):
                  active = not active
              else:
                  active = False
          if event.type == pygame.QUIT:
              return None

      color = color_active if active else color_inactive
      pygame.draw.rect(screen, color, input_box)
      screen.blit(input_text, (input_text_rect.x, input_text_rect.y))

      pygame.display.flip()

# Functions for leaderboard
def load_leaderboard():
    try:
        with open(LEADERBOARD_FILE, "r") as file:
            lines = file.readlines()
            leaderboard.extend([line.strip().split(":") for line in lines])
    except FileNotFoundError:
        pass

def save_leaderboard():
    with open(LEADERBOARD_FILE, "w") as file:
        for entry in leaderboard:
            file.write(f"{entry[0]}:{entry[1]}\n")

# Load leaderboard on program start
load_leaderboard()

# ... (unchanged)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_leaderboard()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if game_state == START_SCREEN or game_state == GAME_OVER:
                # Start or restart the game
                game_state = GAME_RUNNING
                bird_rect.y = HEIGHT // 2
                pipes = []
                score = 0
                bird_speed = 0
                player_name = textinput.get_text()

            elif game_state == GAME_RUNNING:
                # Jump only when the game is running
                bird_speed = JUMP_STRENGTH

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_L:
            if game_state == GAME_OVER:
                game_state = LEADERBOARD_SCREEN
            elif game_state == LEADERBOARD_SCREEN:
                game_state = GAME_OVER

        # Feed it with events every frame
        textinput.update(events)

    if game_state == START_SCREEN:
        draw_start_screen()

        # Draw the text input
        screen.blit(textinput.get_surface(), (WIDTH // 4, HEIGHT // 2))

    elif game_state == GAME_RUNNING:
        # ... (unchanged)
    elif game_state == GAME_OVER:
        draw_end_screen()

        # Save the score to the leaderboard only once
        if not leaderboard_updated:
            leaderboard.append((player_name, score))
            leaderboard.sort(key=lambda x: x[1], reverse=True)  # Sort in descending order
            if len(leaderboard) > 5:
                leaderboard = leaderboard[:5]  # Keep only the top 5 scores
            leaderboard_updated = True

        leaderboard_text = font.render("Press L to View Leaderboard", True, (255, 255, 255))
        leaderboard_rect = leaderboard_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        screen.blit(leaderboard_text, leaderboard_rect)

        restart_text = font.render("Press SPACE to Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT * 2 // 3))
        screen.blit(restart_text, restart_rect)

        # Save the updated leaderboard
        save_leaderboard()

    elif game_state == LEADERBOARD_SCREEN:
        draw_leaderboard()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

    # Increment pipe counter
    pipe_counter = (pipe_counter + 1) % pipe_frequency
