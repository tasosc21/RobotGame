import pygame

class Doors:
    def __init__(self):
        self.door_image = pygame.image.load('assets/door.png')
        self.w = self.door_image.get_width()
        self.h = self.door_image.get_height()

        # Predefined door positions (top-left coordinates of the tiles)
        self.positions = [
            (212, 12),     # door1
            (312, 512),    # door2
            (1012, 112),   # door3
            (912, 612),    # door4
        ]

        # Center doors inside blocks
        self.rects = [pygame.Rect(x + (100 - self.w) // 2, y + (100 - self.h) // 2, self.w, self.h)
                      for x, y in self.positions]

        # Define door links: door1 <-> door4, door2 <-> door3
        self.pairs = {
            0: 3,
            1: 2,
            2: 1,
            3: 0,
        }

    def draw_doors(self, screen):
        """Draw all doors on the given surface."""
        for rect in self.rects:
            screen.blit(self.door_image, rect.topleft)

    def get_door_index(self, robot_rect):
        """
        Check if the robot is currently overlapping any door.
        
        Parameters:
            robot_rect (pygame.Rect): The robot's rectangular position.
        
        Returns:
            int or None: The index of the door the robot is on, or None if not on any door.
        """
        for i, door_rect in enumerate(self.rects):
            if robot_rect.colliderect(door_rect):
                return i
        return None

    def get_target_position(self, door_index):
        """Return the position of the door linked to this index"""
        target_index = self.pairs.get(door_index)
        if target_index is not None:
            pos = list(self.rects[target_index].topleft)
            pos[1] = pos[1]-12
            return pos
        return None