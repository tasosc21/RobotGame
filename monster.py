class Monster:
    def __init__(self, rect, speed):
        self.rect = rect
        self.path_til = []
        self.path_pix = []
        self.target_pix = (rect.x, rect.y)
        self.next_pos = 0
        self.speed = speed
        self.current_tile = (self.rect.x//100, self.rect.y//100)

    def draw_monster(self, screen, image):
        """
        Draw the monster sprite on the screen.
        """
        screen.blit(image, self.rect)
        
    def is_clicked(self, mouse_pos):
        """
        Check if the monster was clicked by the mouse.

        Parameters:
            mouse_pos (tuple): The (x, y) position of the mouse click.

        Returns:
            bool: True if clicked, False otherwise.
        """
        return self.rect.collidepoint(mouse_pos)

    def move_monster(self, spawn_points):
        """
        Move the monster pixel-by-pixel along its path.

        The monster moves towards `target_pix`. When it reaches the target,
        it pops the next tile from `path_til` and sets a new pixel target.

        Parameters:
            spawn_points (list of lists): 2D list of pixel coordinates for tiles.
        """
        if self.path_til != []:
            if self.rect.x == self.target_pix[0] and self.rect.y == self.target_pix[1]:
                self.current_tile = self.path_til.pop(0)
                if self.path_til != []: 
                    target_tile = self.path_til[0]
                    self.target_pix = spawn_points[target_tile[0]][target_tile[1]]
    
            # Right
            if self.target_pix[0] > self.rect.x:
                self.rect.x += self.speed
                if self.rect.x > self.target_pix[0]:
                    self.rect.x = self.target_pix[0]
            # Left
            elif self.target_pix[0] < self.rect.x:
                self.rect.x -= self.speed
                if self.rect.x < self.target_pix[0]:
                    self.rect.x = self.target_pix[0]
            # Down
            elif self.target_pix[1] > self.rect.y:
                self.rect.y += self.speed
                if self.rect.y > self.target_pix[1]:
                    self.rect.y = self.target_pix[1]
            # Up
            elif self.target_pix[1] < self.rect.y:
                self.rect.y -= self.speed
                if self.rect.y < self.target_pix[1]:
                    self.rect.y = self.target_pix[1]