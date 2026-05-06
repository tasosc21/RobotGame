import pygame

class Robot:
    def __init__(self):
        self.robot = pygame.image.load("assets/robot.png")
        self.rect = self.robot.get_rect()
        self.rect.topleft = (12, 12) # Starting position
        self.speed = 6

    def draw_robot(self, screen):
        """
        Draw the robot on the given screen surface.
        """
        screen.blit(self.robot, self.rect)

    def move(self, direction, walls):
        """
        Move the robot in the specified direction if no collision occurs.
        
        Parameters:
            direction (str): One of 'left', 'right', 'up', 'down'.
            walls (list of pygame.Rect): Rectangles representing obstacles.
        """
        new_rect = self.rect.copy()

        if direction == 'left':
            new_rect.x -= self.speed        
        if direction == 'right':
            new_rect.x += self.speed
        if direction == 'up':
            new_rect.y -= self.speed        
        if direction == 'down':
            new_rect.y += self.speed

        if not any(new_rect.colliderect(wall) for wall in walls):
            self.rect = new_rect  # Only move if no collision