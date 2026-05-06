import pygame
import random
import pygame
import random
from coin import Coin

class Coins:
    def __init__(self):
        self.coin_image = pygame.image.load('assets/coin.png')
        self.coins = []
        self.total_collected = 0
        self.current_coins = 0
        self.total_spawned = 0
        self.spawn_points = self.get_spawn_points()
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_delay = 5000

    def get_spawn_points(self):
        """
        Generate a grid of possible coin spawn positions
        centered inside 100x100 blocks.

        Returns:
            List of (x, y) tuples for spawn locations.
        """
        spawn_points = []
        for i in range(7):
            for j in range(12):
                x = 10 + j * 100 + (100 - self.coin_image.get_width()) // 2
                y = 10 + i * 100 + (100 - self.coin_image.get_height()) // 2
                spawn_points.append((x, y))
        return spawn_points

    def spawn_coin(self, robot_rect):
        """
        Spawn a coin at a random available spawn point,
        avoiding overlap with existing coins and the robot's position.

        Parameters:
            robot_rect (pygame.Rect): The robot's collision rectangle.
        """
        now = pygame.time.get_ticks()
        if now - self.last_spawn_time >= self.spawn_delay:
            available_positions = [pos for pos in self.spawn_points
                                   if not any(coin.rect.topleft == pos for coin in self.coins)
                                   and not robot_rect.collidepoint(pos[0] + 10, pos[1] + 10)]  

            if available_positions:
                x, y = random.choice(available_positions)
                self.coins.append(Coin(x, y, self.coin_image))
                self.total_spawned += 1
                self.last_spawn_time = now
    
    def draw_coins(self, screen):
        """
        Draw all active coins on the screen.
        """
        for coin in self.coins:
            coin.draw_coin(screen)

    def check_collection_robot(self, robot_rect):
        """
        Check if the robot has collected any coins,
        update counters, and remove collected coins.

        Parameters:
            robot_rect (pygame.Rect): The robot's collision rectangle.

        Returns:
            int: Total number of coins collected so far.
        """
        collected = []
        for coin in self.coins:
            if robot_rect.colliderect(coin.rect):
                collected.append(coin)
                self.total_collected += 1
                self.current_coins += 1
        for coin in collected:
            self.coins.remove(coin)
        return self.total_collected
    
    def check_collection_monsters(self, monsters):
        """
        Check if any monsters collected coins,
        remove those coins and increase monster speed.

        Parameters:
            monsters (object): Object with attribute `monsters`, a list of monster objects
                               each having `rect` and `speed` attributes.
        """
        for monster in monsters.monsters:
            for coin in self.coins:
                if monster.rect.colliderect(coin.rect):
                    self.coins.remove(coin)
                    monster.speed += 1
                
    def current_count(self, monsters_killed=0):
        """
        Calculate current effective coin count considering monsters killed.

        Parameters:
            monsters_killed (int): Number of monsters killed.

        Returns:
            int: Adjusted current coin count.
        """
        return max(0, self.total_collected - 5 * monsters_killed)