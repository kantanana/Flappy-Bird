from imports import *
from constants import Const

class Pipe:
    def __init__(self, x, height, gap, width, color, end_color):
        self.rect_top = pygame.Rect(x, 0, width, height)
        self.rect_bottom = pygame.Rect(x, height + gap, width, Const.HEIGHT - (height + gap))
        self.color = color

        self.rect_top_end = pygame.Rect(x - 5, height - 30, width + 10, 30)
        self.rect_bottom_end = pygame.Rect(x - 5, height + gap, width + 10, 30)
        self.end_color = end_color

    def move(self, speed):
        self.rect_top.x -= speed
        self.rect_bottom.x -= speed
        self.rect_top_end.x -= speed
        self.rect_bottom_end.x -= speed
