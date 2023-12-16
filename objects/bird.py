from imports import *

class Bird:
    def __init__(self, x, y, image, size, gravity, jump_strength):
        self.rect = image.get_rect(center=(x, y))
        self.speed = 0
        self.gravity = gravity
        self.jump_strength = jump_strength

    def jump(self):
        self.speed = self.jump_strength

    def update(self):
        self.speed += self.gravity
        self.rect.y += self.speed
