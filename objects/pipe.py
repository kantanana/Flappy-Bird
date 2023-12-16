from imports import *
from constants import Const

class Pipe:
    def __init__(self, x, height, gap, width, color):
        self.rect_top = pygame.Rect(x, 0, width, height)
        self.rect_bottom = pygame.Rect(x, height + gap, width, Const.HEIGHT - (height + gap))
        self.color = color

    def move(self, speed):
        self.rect_top.x -= speed
        self.rect_bottom.x -= speed