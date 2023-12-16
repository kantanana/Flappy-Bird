class Ground:
    def __init__(self, x, y, image):
        self.rect = image.get_rect(topleft=(x, y))