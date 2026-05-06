class Coin:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw_coin(self, screen):
        """
        Draw the coin on the provided screen surface.
        """
        screen.blit(self.image, self.rect)