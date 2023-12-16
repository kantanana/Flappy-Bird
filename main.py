from imports import *
from objects.bird import Bird
from objects.pipe import Pipe
from objects.ground import Ground
from constants import Const

# Initialize Pygame
pygame.init()

# Load images
background_image = pygame.image.load(Const.BACKGROUND)
background_image = pygame.transform.scale(background_image, (Const.WIDTH, Const.HEIGHT))

bird_image = pygame.image.load(Const.BIRD)
bird_image = pygame.transform.scale(bird_image, Const.BIRD_SIZE)

ground_image = pygame.image.load(Const.GROUND)
ground_image = pygame.transform.scale(ground_image, (Const.WIDTH, Const.GROUND_HEIGHT))

# Fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)


game_state = Const.START_SCREEN

# Bird
bird = Bird(Const.WIDTH // 4, Const.HEIGHT // 2, bird_image, Const.BIRD_SIZE, Const.GRAVITY, Const.JUMP_STRENGTH)

# Pipes
pipes = []
pipe_gap = 150
pipe_speed = 5
pipe_frequency = 60
pipe_counter = 0

# Ground
ground = Ground(0, Const.HEIGHT - Const.GROUND_HEIGHT, ground_image)

# Score
score = 0

def draw_objects():
    screen.blit(background_image, (0, 0))
    for pipe in pipes:
        pygame.draw.rect(screen, pipe.color, pipe.rect_top)
        pygame.draw.rect(screen, pipe.color, pipe.rect_bottom)
    screen.blit(ground_image, ground.rect)
    screen.blit(bird_image, bird.rect)

    # Display score
    score_text = font.render(str(score), True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(Const.WIDTH // 2, 50))
    screen.blit(score_text, score_rect)

def draw_start_screen():
    screen.blit(background_image, (0, 0))
    start_text = big_font.render("Flappy Bird", True, (255, 255, 255))
    start_rect = start_text.get_rect(center=(Const.WIDTH // 2, Const.HEIGHT // 3))
    screen.blit(start_text, start_rect)

    instruction_text = font.render("Press SPACE to Start", True, (255, 255, 255))
    instruction_rect = instruction_text.get_rect(center=(Const.WIDTH // 2, Const.HEIGHT // 2))
    screen.blit(instruction_text, instruction_rect)

def draw_end_screen():
    screen.blit(background_image, (0, 0))
    end_text = big_font.render("Game Over", True, (255, 255, 255))
    end_rect = end_text.get_rect(center=(Const.WIDTH // 2, Const.HEIGHT // 3))
    screen.blit(end_text, end_rect)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(Const.WIDTH // 2, Const.HEIGHT // 2))
    screen.blit(score_text, score_rect)

    restart_text = font.render("Press SPACE to Restart", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(Const.WIDTH // 2, Const.HEIGHT * 2 // 3))
    screen.blit(restart_text, restart_rect)



# Set up the display
screen = pygame.display.set_mode((Const.WIDTH, Const.HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Set up the clock
clock = pygame.time.Clock()
# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if game_state == Const.START_SCREEN or game_state == Const.GAME_OVER:
                # Start or restart the game
                game_state = Const.GAME_RUNNING
                bird.rect.y = Const.HEIGHT // 2
                pipes = []
                score = 0
                bird.jump()

            elif game_state == Const.GAME_RUNNING:
                # Jump only when the game is running
                bird.jump()

    if game_state == Const.START_SCREEN:
        draw_start_screen()
    elif game_state == Const.GAME_RUNNING:
        # Bird movement
        bird.update()

        # Pipe movement and generation
        if pipe_counter == 0:
            pipe_height = random.randint(50, Const.HEIGHT - Const.GROUND_HEIGHT - pipe_gap - 50)
            new_pipe = Pipe(Const.WIDTH, pipe_height, pipe_gap, Const.PIPE_WIDTH, Const.PIPE_COLOR)
            pipes.append(new_pipe)

        for pipe in pipes:
            pipe.move(pipe_speed)

        pipes = [pipe for pipe in pipes if pipe.rect_top.x > 0]

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

    elif game_state == Const.GAME_OVER:
        draw_end_screen()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(Const.FPS)

    # Increment pipe counter
    pipe_counter = (pipe_counter + 1) % pipe_frequency
