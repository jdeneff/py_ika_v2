import pygame
import constants
from game_objects import GameObject, PlayerSprite, EnemySprite, LaserSprite
from random import randint
from pygame.locals import K_SPACE, K_LSHIFT, K_LEFT, K_RIGHT

class PlayerController:
    def __init__(self, p_group):
        # The game loop will pass in input directly to this variable
        self.keys_pressed = []

        # Create a sprite, add to its own group and the all sprites group
        self.player_sprite = PlayerSprite((constants.WIDTH / 2, constants.HEIGHT - 20))
        p_group.add(self.player_sprite)

    def player_move(self):
        # Movement in response to keyboard input
        if self.keys_pressed[K_LEFT]:
            self.player_sprite.move_left(constants.P_SPD)
        if self.keys_pressed[K_RIGHT]:
            self.player_sprite.move_right(constants.P_SPD)

        # Set wall boundaries
        if self.player_sprite.rect.left < 0:
            self.player_sprite.rect.left = 0
        if self.player_sprite.rect.right > constants.WIDTH:
            self.player_sprite.rect.right= constants.WIDTH

    def player_flip(self):
        # Change player color in response to keyboard input
        if self.keys_pressed[K_LSHIFT] and self.player_sprite.flip_ready:
            self.player_sprite.flip_state()
            # Get ready for recharge
            self.player_sprite.flip_ready = False
            self.player_sprite.flip_time = pygame.time.get_ticks()

    def player_fire(self, p_las_group, all_group):
        p_state = self.player_sprite.state
        
        if self.keys_pressed[K_SPACE] and self.player_sprite.fire_ready:
            new_laser = LaserSprite(self.player_sprite.rect.midtop)
            new_laser.state = p_state
            p_las_group.add(new_laser)
            all_group.add(new_laser)

            # Get ready for recharge
            self.player_sprite.fire_ready = False
            self.player_sprite.fire_time = pygame.time.get_ticks()

    def player_reset(self):
        time_now = pygame.time.get_ticks()
        if not self.player_sprite.flip_ready and time_now - self.player_sprite.flip_time >= constants.P_FLIP_T:
            self.player_sprite.flip_ready = True
        if not self.player_sprite.fire_ready and time_now - self.player_sprite.fire_time >= constants.P_RECHARGE_T:
            self.player_sprite.fire_ready = True

class EnemyController:
    def __init__(self):

        self.spawn_ready = True
        self.spawn_time = 0

    def enemy_spawn(self, e_group, all_group):
        spawn_x = randint(20, constants.WIDTH - 20)
        if self.spawn_ready:
            new_enemy = EnemySprite((spawn_x, 50))
            e_group.add(new_enemy)
            all_group.add(new_enemy)
            self.spawn_ready = False
            self.spawn_time = pygame.time.get_ticks()

    def enemy_move(self, e_group):
        for enemy in e_group:
            enemy.move_down(constants.E_SPD)

    def enemy_fire(self, e_group, e_las_group, all_group):
        for enemy in e_group:
            e_state = enemy.state
            if enemy.fire_ready and enemy.rect.bottom < constants.HEIGHT / 2:
                new_laser = LaserSprite(enemy.rect.midbottom)
                new_laser.state = e_state
                e_las_group.add(new_laser)
                all_group.add(new_laser)

                enemy.fire_ready = False
                enemy.fire_time = pygame.time.get_ticks()

    def enemy_reset_spawn(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.spawn_time >= constants.E_SPAWN_T:
            self.spawn_ready = True

    def enemy_reset_fire(self, e_group):
        time_now = pygame.time.get_ticks()
        for enemy in e_group:
            if time_now - enemy.fire_time >= constants.E_RECHARGE_T:
                enemy.fire_ready = True














        
