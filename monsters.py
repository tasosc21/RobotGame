import pygame
import random
from monster import Monster

class Monsters:
    def __init__(self):
        self.monster = pygame.image.load("assets/monster.png")
        self.spawn_points, self.matrix_spawn_points = self.get_spawn_points()
        self.spawn_blocks = self.get_spawn_blocks()
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_delay = 22000
        self.monsters = []
        self.monsters_killed = 0
        self.speed = 1
    
    def get_spawn_blocks(self):
        """
        Define rectangular blocks (pygame.Rect) used as potential spawn zones.

        Returns:
            List[pygame.Rect]: Rectangles representing spawn blocks.
        """
        spawn_blocks = []
        for i in range(7):
            for j in range(12):
                x = 13 + j * 100
                y = 13 + i * 100
                spawn_blocks.append(pygame.Rect(x, y, 94, 94))
        return spawn_blocks

    def get_spawn_points(self):
        """
        Compute precise pixel positions for spawning monsters,
        both as a flat list and matrix form (rows x columns).

        Returns:
            Tuple[List[Tuple[int, int]], List[List[Tuple[int, int]]]]:
                - Flat list of spawn positions (x, y)
                - Matrix (2D list) of spawn positions indexed by row and column
        """
        spawn_points = []
        matrix_spawn_points = []
        for i in range(7):
            matrix_spawn_points.append([])
            for j in range(12):
                x = 10 + j * 100 + (100 - self.monster.get_width()) // 2
                y = 10 + i * 100 + (100 - self.monster.get_height()) // 2
                spawn_points.append((x, y))
                matrix_spawn_points[i].append((x, y))
        return spawn_points, matrix_spawn_points

    def get_monster_rect(self, x, y):
        """
        Generate a pygame.Rect for a monster at given pixel coordinates.

        Parameters:
            x (int): X coordinate.
            y (int): Y coordinate.

        Returns:
            pygame.Rect: Rectangle for the monster sprite at (x, y).
        """
        return self.monster.get_rect(topleft=(x,y))

    def spawn_monster(self, robot_rect):
        """
        Spawn a new monster in an available spawn block,
        avoiding proximity to the robot and existing monsters.

        Parameters:
            robot_rect (pygame.Rect): The player's collision rectangle.

        Returns:
            bool: True if a monster was spawned, False otherwise.
        """
        now = pygame.time.get_ticks()
        new = robot_rect.copy()
        new.x -= 150
        new.y -= 150
        new.width += 300
        new.height += 300

        if now - self.last_spawn_time >= self.spawn_delay:
            available_blocks = [i for i, block in enumerate(self.spawn_blocks)
                                   if not new.colliderect(block)]
            for monster in self.monsters:
                for i in available_blocks:
                    if self.spawn_blocks[i].colliderect(monster.rect):
                        available_blocks.remove(i)
            available_positions = [self.spawn_points[i] for i in available_blocks]
                 
            if available_positions:
                x, y = random.choice(available_positions)
                self.monsters.append(Monster(self.get_monster_rect(x, y), self.speed))
                self.last_spawn_time = now
                return True
        else:
            return False

    def draw_monsters(self, screen):
        """
        Draw all active monsters on the screen.
        """
        for monster in self.monsters:
            monster.draw_monster(screen, self.monster)

    def check_monster_killed_robot(self, robot_rect):
        """
        Check if any monster collides with the robot,
        indicating the robot is killed.

        Parameters:
            robot_rect (pygame.Rect): The robot's collision rectangle.

        Returns:
            bool: True if a monster collides with the robot, False otherwise.
        """
        new = robot_rect.copy()
        new.x += 16
        new.y += 16
        new.width -= 32
        new.height -= 32
        for monster in self.monsters:
            if new.colliderect(monster.rect):
                return True
        return False

    def check_click_kill(self, mouse_pos, current_coins):
        """
        Check if a monster was clicked, remove it,
        update coins and kills accordingly.

        Parameters:
            mouse_pos (tuple): The position of the mouse click.
            current_coins (int): The player's current coin count.

        Returns:
            int: Updated coin count after monster removal.
        """
        for monster in self.monsters:
            if monster.rect.collidepoint(mouse_pos):
                self.monsters.remove(monster)
                current_coins -= 5
                self.monsters_killed += 1
        return current_coins