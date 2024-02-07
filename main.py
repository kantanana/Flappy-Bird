from imports import *
from objects.bird import Bird
from objects.pipe import Pipe
from objects.ground import Ground
from constants import Const
import time as t


# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((Const.WIDTH, Const.HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load images
background_image = pygame.image.load(Const.BACKGROUND).convert()
background_image = pygame.transform.scale(background_image, (Const.WIDTH, Const.HEIGHT))

bird_image = pygame.image.load(Const.BIRD).convert_alpha()
bird_image = pygame.transform.scale(bird_image, Const.BIRD_SIZE)

ground_image = pygame.image.load(Const.GROUND).convert()
ground_image = pygame.transform.scale(ground_image, (Const.WIDTH, Const.GROUND_HEIGHT))

# Fonts
font = pygame.font.Font("asset/font/DTM-Mono.otf", 36)
big_font = pygame.font.Font("asset/font/DTM-Mono.otf", 72)


game_state = Const.START_SCREEN

# Bird
bird = Bird(Const.WIDTH // 4, Const.HEIGHT // 2, bird_image, Const.BIRD_SIZE, Const.GRAVITY, Const.JUMP_STRENGTH)

# Pipes
pipes = []
pipe_gap = 180
pipe_speed = 5
pipe_frequency = 150
pipe_counter = 0

# Ground
ground = Ground(0, Const.HEIGHT - Const.GROUND_HEIGHT, ground_image)

# Score
score = 0


# Leaderboard
leaderboard = []


def load_leaderboard():
    try:
        with open(Const.LEADERBOARD_FILE, "r") as file:
            lines = file.readlines()
            leaderboard.extend([int(line.strip()) for line in lines])
    except FileNotFoundError:
        pass

def save_leaderboard():
    with open(Const.LEADERBOARD_FILE, "w") as file:
        for entry in leaderboard:
            file.write(f"{entry}\n")

def draw_objects():
    screen.blit(background_image, (0, 0))
    for pipe in pipes:
        pygame.draw.rect(screen, pipe.color, pipe.rect_top)
        pygame.draw.rect(screen, pipe.color, pipe.rect_bottom)
        pygame.draw.rect(screen, pipe.end_color, pipe.rect_top_end)
        pygame.draw.rect(screen, pipe.end_color, pipe.rect_bottom_end)
    screen.blit(ground_image, ground.rect)
    screen.blit(bird_image, bird.rect)

    # Display score
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(Const.WIDTH // 2, 50))
    score_surf = pygame.Surface((score_rect.w, score_rect.h))
    score_surf.set_alpha(128)
    score_surf.fill((100,100,100))
    screen.blit(score_surf, score_rect)
    screen.blit(score_text, score_rect)

def draw_start_screen():
    screen.blit(background_image, (0, 0))
    start_text = big_font.render("Flappy Bird", True, (255, 255, 255))
    start_rect = start_text.get_rect(center=(Const.WIDTH // 2, Const.HEIGHT // 3))
    screen.blit(start_text, start_rect)

    instruction_text = font.render("Press R to Start", True, (255, 255, 255))
    instruction_rect = instruction_text.get_rect(center=(Const.WIDTH // 2, Const.HEIGHT // 2))
    screen.blit(instruction_text, instruction_rect)

def draw_end_screen():
    screen.blit(background_image, (0, 0))
    end_text = big_font.render("Game Over", True, (255, 255, 255))
    end_rect = end_text.get_rect(center=(Const.WIDTH // 2, Const.HEIGHT // 3))
    screen.blit(end_text, end_rect)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(Const.WIDTH // 2, Const.HEIGHT - 450))
    screen.blit(score_text, score_rect)

    restart_text = font.render("Press R to Restart", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(Const.WIDTH // 2, Const.HEIGHT - 320))
    screen.blit(restart_text, restart_rect)
    leaderboard_text = font.render("Press L to View Leaderboard", True, (255, 255, 255))
    leaderboard_rect = leaderboard_text.get_rect(center=(Const.WIDTH // 2, Const.HEIGHT - 240))
    screen.blit(leaderboard_text, leaderboard_rect)

def draw_leaderboard():

    screen.blit(background_image, (0, 0))
    leaderboard_title_text = big_font.render("Leaderboard", True, (255, 255, 255))
    leaderboard_title_rect = leaderboard_title_text.get_rect(center=(Const.WIDTH // 2, (Const.HEIGHT // 6) - 20))

    leaderboard_surf = pygame.Surface((500, 110 + 32*len(leaderboard)))
    leaderboard_surf.set_alpha(128)
    leaderboard_surf.fill((100,100,100))
    leaderboard_surf_rect = leaderboard_surf.get_rect(midtop = (600, 70))
    screen.blit(leaderboard_surf, leaderboard_surf_rect)

    screen.blit(leaderboard_title_text, leaderboard_title_rect)

    y_position = (Const.HEIGHT // 4) - 20  # Set initial y position

    for i, entry in enumerate(leaderboard, start=1):
        entry_text = font.render(f"{i}. {entry}", True, (255, 255, 255))
        entry_rect = entry_text.get_rect(center=(Const.WIDTH // 2, y_position))
        screen.blit(entry_text, entry_rect)

        y_position += 32  # Move to the next row


    back_text = font.render("Press L to Go Back", True, (255, 255, 255))
    back_rect = back_text.get_rect(center=(Const.WIDTH // 2, Const.HEIGHT - 210))
    screen.blit(back_text, back_rect)

def update_leaderboard():
    # Save the score to the leaderboard
    global leaderboard
    leaderboard.append(score)
    leaderboard.sort(reverse=True)  # Sort in descending order
    if len(leaderboard) > 5:
        leaderboard = leaderboard[:12]  # Keep only the top 12 scores

    leaderboard_text = font.render("Press L to View Leaderboard", True, (255, 255, 255))
    leaderboard_rect = leaderboard_text.get_rect(center=(Const.WIDTH // 2, Const.HEIGHT - 50))
    screen.blit(leaderboard_text, leaderboard_rect)

    restart_text = font.render("Press R to Restart", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(Const.WIDTH // 2, Const.HEIGHT * 2 // 3))
    screen.blit(restart_text, restart_rect)

    # Save the updated leaderboard
    save_leaderboard()

# Load leaderboard on program start
load_leaderboard()

# Set up the clock
clock = pygame.time.Clock()

# Game loop
leaderboard_updated = False  # Add this line to initialize the variable
score = 0
diff = 0
while True:

    if (score - diff) >= (100):
        pipe_gap -= 5
        pipe_speed += 0.2
        if pipe_frequency > 80:
            pipe_frequency -= 3
        diff = score

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if game_state == Const.GAME_RUNNING:
                # Jump only when the game is running
                bird.jump()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            if game_state == Const.START_SCREEN or game_state == Const.GAME_OVER:
                # Start or restart the game
                game_state = Const.GAME_RUNNING
                bird.rect.y = Const.HEIGHT // 2
                pipes = []
                score = 0
                pipe_gap = 180
                pipe_speed = 5
                pipe_frequency = 150
                pipe_counter = 0
                diff = 0
                leaderboard_updated = False  # Reset the leaderboard update flag
                bird.jump()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
            if game_state == Const.GAME_OVER:
                game_state = Const.LEADERBOARD_SCREEN
            elif game_state == Const.LEADERBOARD_SCREEN:
                game_state = Const.GAME_OVER

    if game_state == Const.START_SCREEN:
        draw_start_screen()
    elif game_state == Const.GAME_RUNNING:
        # Bird movement
        bird.update()

        # Pipe movement and generation
        if pipe_counter == 0:
            pipe_height = random.randint(50, Const.HEIGHT - Const.GROUND_HEIGHT - pipe_gap - 50)
            new_pipe = Pipe(Const.WIDTH, pipe_height, pipe_gap, Const.PIPE_WIDTH, Const.PIPE_COLOR, Const.PIPE_END_COLOR)
            pipes.append(new_pipe)

        for pipe in pipes:
            pipe.move(pipe_speed)

        pipes = [pipe for pipe in pipes if pipe.rect_top.x > -50]

        # Check for collisions
        if bird.rect.colliderect(ground.rect) or bird.rect.y < 0:
            game_state = Const.GAME_OVER

        for pipe in pipes:
            if bird.rect.colliderect(pipe.rect_top) or bird.rect.colliderect(pipe.rect_bottom):
                game_state = Const.GAME_OVER

        # Check for scoring
        if pipes and bird.rect.x > pipes[0].rect_top.x + Const.PIPE_WIDTH:
            score += 1

        # Draw objects
        draw_objects()

   # elif game_state == Const.GAME_OVER:
  #      draw_end_screen()
   #     update_leaderboard()

    elif game_state == Const.GAME_OVER:
      draw_end_screen()
      if not leaderboard_updated:  # Add a flag to track if leaderboard is already updated
          update_leaderboard()  # Call the update_leaderboard function
          leaderboard_updated = True  # Set the flag to True

    elif game_state == Const.LEADERBOARD_SCREEN:
        draw_leaderboard()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(Const.FPS)

    # Increment pipe counter
    pipe_counter = (pipe_counter + 1) % pipe_frequency
