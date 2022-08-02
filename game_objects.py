import pygame
import constants
from random import randint

# State 0 is green
# State 1 is red

class GameObject(pygame.sprite.Sprite):
    def __init__(self, spawn_pos):
        super().__init__()

        # State determines green or red
        self.state = randint(0,1)

        # Internal variables for firing lasers
        self.fire_ready = False
        self.fire_time = 0

        # Internal variables for flipping state
        self.flip_ready = False
        self.flip_time = 0

        # Placeholder image and rect
        self.images = pygame.Surface(constants.L_DIM)
        self.rect = self.images.get_rect(midbottom = spawn_pos)
        
    def move_left(self, spd):
        self.rect.move_ip(-spd, 0)
        
    def move_right(self, spd):
        self.rect.move_ip(spd, 0)
        
    def move_up(self, spd):
        self.rect.move_ip(0, -spd)
        
    def move_down(self, spd):
        self.rect.move_ip(0, spd)

    def flip_state(self):
        # Get from red to green or vice versa
        if self.state == 0:
            self.state = 1
        elif self.state == 1:
            self.state = 0

    def draw(self, surf):
        # A way to draw the correct image from self.images
        surf.blit(self.images[self.state], self.rect)


class PlayerSprite(GameObject):
    def __init__(self, spawn_pos):

        super().__init__(spawn_pos)
        self.images = [pygame.image.load('assets/ship_green.png'), pygame.image.load('assets/ship_red.png')]
        for image in self.images:
            image.set_colorkey((255, 65, 255))
        self.rect = self.images[0].get_rect(midbottom = spawn_pos)

class EnemySprite(GameObject):
    def __init__(self, spawn_pos):
        super().__init__(spawn_pos)

        self.images = [pygame.image.load('assets/enemy_green.png'), pygame.image.load('assets/enemy_red.png')]
        for image in self.images:
            image.set_colorkey((255, 65, 255))
        self.rect = self.images[0].get_rect(midbottom = spawn_pos)
        
class LaserSprite(GameObject):
    def __init__(self, spawn_pos):
        super().__init__(spawn_pos)

        self.images = [pygame.image.load('assets/laser_green.png'), pygame.image.load('assets/laser_red.png')]
        for image in self.images:
            image.set_colorkey((255, 65, 255))
        self.rect = self.images[0].get_rect(midbottom = spawn_pos)





        
