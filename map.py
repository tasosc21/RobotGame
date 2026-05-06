import pygame
from collections import defaultdict
import heapq

class Map:
    def __init__(self):
        # Dimensions of the overall map display area
        self.width = 1220
        self.height = 720
        self.status_bar_height = 80

        # 2D grid representing the map layout:
        # 0 = empty space, 1 = horizontal wall, 2 = vertical wall, 3 = corner (both)
        self.map_data = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
            [0, 3, 1, 1, 0, 1, 3, 1, 0, 2, 3, 0, 0],
            [0, 2, 2, 3, 1, 2, 2, 3, 0, 2, 2, 2, 0],
            [0, 0, 2, 2, 2, 0, 2, 2, 2, 2, 0, 0, 0],
            [1, 1, 0, 0, 2, 1, 0, 2, 2, 0, 1, 1, 0],
            [0, 2, 2, 1, 0, 2, 3, 0, 1, 1, 0, 2, 0],
            [0, 0, 1, 1, 0, 2, 0, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.walls = []
        self.create_walls()
        self.connectivity = self.grid_connectivity()

    def grid_connectivity(self):
        """
        Constructs a connectivity dictionary for each tile in the grid.
        Each tile (row, col) maps to a dict indicating whether movement
        is allowed in the four cardinal directions.
        Initially, all directions are allowed (True).
        Walls modify connectivity by blocking specific directions.
        """
        connectivity = defaultdict(lambda: {"up": True, "down": True, "left": True, "right": True})

        for wall in self.walls:
            wx, wy = wall.x, wall.y
            # Get tile coordinates of the wall
            col = wx // 100
            row = wy // 100

            # Horizontal wall (blocks top or bottom)
            if wall.width > wall.height:  # wall is horizontal
                    connectivity[(row, col)]["up"] = False
                    if row > 0:
                        connectivity[(row - 1, col)]["down"] = False

            # Vertical wall (blocks left or right)
            elif wall.height > wall.width:
                    connectivity[(row, col)]["left"] = False
                    if col > 0:
                        connectivity[(row, col - 1)]["right"] = False
        return connectivity

    def create_walls(self, border_thickness=10, wall_thickness=2, block_size=100):
        """
        Constructs pygame.Rect objects representing the walls and borders on the map.
        Walls are created according to map_data:
         - 1 indicates a horizontal wall segment,
         - 2 indicates a vertical wall segment,
         - 3 indicates a corner (both horizontal and vertical wall segments).
        Additionally, border walls around the map edges are created.
        """
        for i, row in enumerate(self.map_data):
            for j, cell in enumerate(row):
                x = border_thickness + j * block_size
                y = border_thickness + i * block_size
                if i == 0 :
                    self.walls.append(pygame.Rect(x-border_thickness, y-border_thickness, block_size, border_thickness))
                if i == 7:
                    self.walls.append(pygame.Rect(x-border_thickness, y, block_size, border_thickness))
                if j == 0:
                    self.walls.append(pygame.Rect(x-border_thickness, y-border_thickness, border_thickness, block_size))
                if j == 12:
                    self.walls.append(pygame.Rect(x, y-border_thickness, border_thickness, block_size))


                if cell == 1:  # Horizontal wall
                    self.walls.append(pygame.Rect(x, y, block_size, wall_thickness))
                elif cell == 2:  # Vertical wall
                    self.walls.append(pygame.Rect(x, y, wall_thickness, block_size))
                elif cell == 3:  # Corner: both
                    self.walls.append(pygame.Rect(x, y, block_size, wall_thickness))
                    self.walls.append(pygame.Rect(x, y, wall_thickness, block_size))

    def draw_map(self, surface):
        """
        Draws the map on the given pygame surface.
        Clears the surface with white color, then draws all walls as black rectangles.
        """
        surface.fill((255, 255, 255))  # White background
        for wall in self.walls:
            pygame.draw.rect(surface, (0, 0, 0), wall)

    def a_star(self, start, goal):
        """
        Implements the A* pathfinding algorithm on the grid to find a path
        from start to goal tiles.

        Args:
            start (tuple): Starting(Monster) tile coordinates (row, col)
            goal (tuple): Goal(Robot) tile coordinates (row, col)

        Returns:
            list: List of tile coordinates from start to goal representing the path,
                  or empty list if no path found.
        """
        def heuristic(a, b):
            # Manhattan distance
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        open_set = []
        heapq.heappush(open_set, (0, start))  # (f_score, node)

        came_from = {}  # For reconstructing path
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]  # reversed

            neighbors = []
            directions = self.connectivity.get(current, {"up": False, "down": False, "left": False, "right": False})
            row, col = current
            if directions["up"]:
                neighbors.append((row - 1, col))
            if directions["down"]:
                neighbors.append((row + 1, col))
            if directions["left"]:
                neighbors.append((row, col - 1))
            if directions["right"]:
                neighbors.append((row, col + 1))

            for neighbor in neighbors:
                tentative_g_score = g_score[current] + 1  # All moves cost 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                
        return []