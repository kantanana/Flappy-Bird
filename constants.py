class Const:
    # Constants
    WIDTH, HEIGHT = 1200, 800
    FPS = 60
    WHITE = (255, 255, 255)
    GROUND_HEIGHT = 50
    BIRD_SIZE = (34, 24)  # Bird image size
    GRAVITY = 0.3
    JUMP_STRENGTH = -5.5
    PIPE_WIDTH = 50
    PIPE_COLOR = (0, 255, 0)  # Green
    # Game states
    START_SCREEN = 0
    GAME_RUNNING = 1
    GAME_OVER = 2
    LEADERBOARD_SCREEN = 3
    # image files
    BIRD = 'asset/bird.png'
    GROUND = 'asset/ground.png'
    BACKGROUND = 'asset/background.png'
    LEADERBOARD_FILE = "asset/leaderboard.txt"

