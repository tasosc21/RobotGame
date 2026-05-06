import pygame
import json
import os
from map import Map
from robot import Robot
from doors import Doors
from coins import Coins
from monsters import Monsters

class Game:
    """
    Main game class to handle game initialization, loop, events, rendering, scoring,
    and interaction between robot, monsters, coins, doors, and the map.
    """

    def __init__(self):
        pygame.init()
        self.map = Map()
        self.doors = Doors()
        self.robot = Robot()
        self.coins = Coins()
        self.monsters = Monsters()
        self.counter = 10 # For monster speed increment threshold
        self.path_update_time = pygame.time.get_ticks()
        self.window = pygame.display.set_mode((self.map.width, self.map.height+self.map.status_bar_height))
        pygame.display.set_caption("Game")
        self.font = pygame.font.SysFont(None, 60)
        self.small_font = pygame.font.SysFont(None, 40)
        self.show_start_screen()

    def monster_speed(self):
        """
        Increases monster speed based on totals coins spawned.
        Speed increases every 'counter' coins spawned.
        """
        if self.coins.total_spawned == self.counter:
            self.counter += 10
            self.monsters.speed += 1
            for monster in self.monsters.monsters:
                monster.speed += 1

    def load_high_scores(self):
        """
        Load high scores from a JSON file.
        Returns a list of score dictionaries.
        """
        if os.path.exists("highscores.json"):
            with open("highscores.json", "r") as f:
                return json.load(f)
        return []

    def save_high_scores(self, high_scores):
        """
        Save top 5 high scores to a JSON file.
        """
        with open("highscores.json", "w") as f:
            json.dump(high_scores[:5], f)  # Save only top 5

    def get_player_name(self):
        """
        Display a prompt for the player to enter their name.
        Handles basic text input and returns the entered name.
        """
        name = ""
        font = pygame.font.SysFont(None, 50)
        input_active = True

        while input_active:
            self.window.fill((230, 230, 230))
            prompt = font.render("Enter your name:", True, (0, 0, 0))
            name_text = font.render(name, True, (0, 0, 255))
            self.window.blit(prompt, (self.map.width // 2 - 150, self.map.height // 2 - 50))
            self.window.blit(name_text, (self.map.width // 2 - 150, self.map.height // 2))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name.strip() != "":
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 10:
                            name += event.unicode
        return name

    def convert_pix2til(self, rect):
        """
        Convert pixel coordinates to tile coordinates.
        """
        return (rect.y//100, rect.x//100)

    def convert_til2pix(self, path):
        """
        Convert tile coordinates path to pixel coordinates path.
        Adds 10 pixels offset for better positioning.
        """
        if path is not []:
            return [(x * 100 + 10, y * 100 + 10) for (x, y) in path]

    def score(self):
        """
        Calculate the player's score.
        """
        return self.coins.total_collected + 5 * self.monsters.monsters_killed 

    def stats_bar(self):
        """
        Draw the status bar at the bottom of the window showing stats.
        """
        pygame.draw.rect(self.window, (220, 220, 220), (0, self.map.height, self.map.width, self.map.status_bar_height))
        font = pygame.font.SysFont(None, 36)
        font2 = pygame.font.SysFont(None, 72)
        current = self.coins.current_coins
        total = self.coins.total_collected
        killed = self.monsters.monsters_killed
        score = self.score()
        text1 = font.render(f"Current Coins: {current}", True, (0, 0, 0))
        text2 = font.render(f"Total Collected: {total}", True, (0, 0, 0))
        text3 = font.render(f"Monsters Killed: {killed}", True, (0, 0, 0))
        text4 = font2.render(f"Score: {score}", True, (0, 0, 0))
        self.window.blit(text1, (20, self.map.height + 15))
        self.window.blit(text2, (20, self.map.height + 45))
        self.window.blit(text3, (300, self.map.height + 30))
        self.window.blit(text4, (700, self.map.height + 20))

    def draw_window(self):
        """
        Draw all game elements on the window and update the display.
        """
        self.map.draw_map(self.window)
        self.stats_bar()
        self.doors.draw_doors(self.window)
        self.coins.draw_coins(self.window)
        self.robot.draw_robot(self.window)
        self.monsters.draw_monsters(self.window)
        pygame.display.flip()
    
    def through_door(self, event):
        """
        Teleport robot through a door if the spacebar is pressed and robot is on a door.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                door_index = self.doors.get_door_index(self.robot.rect)
                if door_index is not None:
                    target_pos = self.doors.get_target_position(door_index)
                    if target_pos:
                        self.robot.rect.topleft = target_pos

    def robot_movement(self):
        """
        Move robot based on keyboard input and wall collision.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.robot.move('left', self.map.walls)
        if keys[pygame.K_d]:
            self.robot.move('right', self.map.walls)
        if keys[pygame.K_w]:
            self.robot.move('up', self.map.walls)
        if keys[pygame.K_s]:
            self.robot.move('down', self.map.walls)

    def update_paths(self):
        """
        Update monsters' paths towards the robot using A* every 1 second.
        """
        now = pygame.time.get_ticks()
        update_timer = 1000 - self.monsters.monsters_killed*100 if 1000 - self.monsters.monsters_killed*50 > 100 else 100
        if now - self.path_update_time > update_timer:
            for monster in self.monsters.monsters:
                monster.path_til = self.map.a_star(self.convert_pix2til(monster.rect), self.convert_pix2til(self.robot.rect))
                if monster.path_til is not []:
                    monster.path_pix = self.convert_til2pix(monster.path_til)
            self.path_update_time = now

    def game_over(self):
        """
        Check if robot is killed by any monster, display game over,
        save high score, and show score screen.
        """
        if self.monsters.check_monster_killed_robot(self.robot.rect):
            font = pygame.font.SysFont(None, 100)
            text = font.render("YOU DIED!", True, (200, 0, 0))
            rect = text.get_rect(center=(self.map.width // 2, self.map.height // 2))
            self.window.blit(text, rect)
            pygame.display.flip()
            pygame.time.wait(2000)

            player_name = self.get_player_name()
            current_score = self.score()

            high_scores = self.load_high_scores()
            high_scores.append({"name": player_name, "score": current_score})
            high_scores.sort(key=lambda x: x["score"], reverse=True)
            self.save_high_scores(high_scores)

            self.running = False
            self.show_score_screen()    
        
    def exit_game(self, event):
        """
        Quit the game if the window is closed.
        """
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    def monster_killed(self, event):
        """
        Check for mouse clicks on monsters to kill them if player has enough coins.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.coins.current_coins >= 5:
                self.coins.current_coins = self.monsters.check_click_kill(mouse_pos, self.coins.current_coins)

    def monster_movment(self):
        """
        Move each monster along its computed path.
        """
        for monster in self.monsters.monsters:
            if monster.path_til != []:
                monster.move_monster(self.monsters.matrix_spawn_points)

    def check_events(self):
        """
        Process pygame events, update game state.
        """
        for event in pygame.event.get():
            self.exit_game(event)
            self.through_door(event)
            self.monster_killed(event)
        
        self.coins.spawn_coin(self.robot.rect)
        self.monsters.spawn_monster(self.robot.rect)
        self.update_paths()
        self.robot_movement()
        self.monster_movment()
        self.coins.check_collection_robot(self.robot.rect)
        self.monster_speed()
        self.coins.check_collection_monsters(self.monsters)
        self.game_over()

    def main_loop(self):
        """
        Main game loop running at 60 FPS.
        """
        clock = pygame.time.Clock()
        self.running = True
        while True:
            self.draw_window()
            self.check_events()     
            clock.tick(60)

    def show_start_screen(self):
        """
        Display start screen with New Game and Scores buttons.
        """
        new_game_button = pygame.Rect(self.map.width // 2 - 100, 200, 200, 60)
        scores_button = pygame.Rect(self.map.width // 2 - 100, 300, 200, 60)

        while True:
            self.window.fill((240, 240, 240))

            pygame.draw.rect(self.window, (100, 200, 100), new_game_button)
            pygame.draw.rect(self.window, (100, 100, 200), scores_button)

            self.draw_text("New Game", new_game_button, self.font)
            self.draw_text("Scores", scores_button, self.font)

            pygame.display.flip()

            for event in pygame.event.get():
                self.exit_game(event)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if new_game_button.collidepoint(event.pos):
                        self.main_loop()
                        return
                    elif scores_button.collidepoint(event.pos):
                        self.show_score_screen()

    def draw_text(self, text, rect, font, color=(255, 255, 255)):
        """
        Helper function to draw centered text inside a rectangle.
        """
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.window.blit(text_surface, text_rect)

    def show_score_screen(self):
        """
        Show top 5 high scores for 5 seconds, then return to start screen.
        """
        self.window.fill((230, 230, 230))
        font = pygame.font.SysFont(None, 50)
        header = font.render("Top 5 Scores", True, (0, 0, 0))
        self.window.blit(header, (self.map.width // 2 - 100, 50))

        high_scores = self.load_high_scores()

        for i, entry in enumerate(high_scores[:5]):
            text = font.render(f"{i + 1}. {entry['name']} - {entry['score']}", True, (0, 0, 0))
            self.window.blit(text, (self.map.width // 2 - 150, 120 + i * 50))

        pygame.display.flip()
        pygame.time.wait(5000)
        self.show_start_screen()