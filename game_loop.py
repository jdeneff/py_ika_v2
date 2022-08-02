import pygame
import constants
from game_controllers import PlayerController, EnemyController

class Game:
    def __init__(self):
        self.playing = True
        self.score = 0

        self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        self.screen.fill(constants.BG_COLOR)

        self.p_group = pygame.sprite.GroupSingle()
        self.p_las_group = pygame.sprite.Group()
        
        self.e_group = pygame.sprite.Group()
        self.e_las_group = pygame.sprite.Group()

        self.all_sprites = pygame.sprite.Group()

        self.player_con = PlayerController(self.p_group)
        self.enemy_con = EnemyController()

        self.keys_pressed = []

        self.score_band = pygame.Surface((constants.WIDTH, 50))
        self.score_band.fill('white')
        self.score_band_rect = self.score_band.get_rect(topleft = (0, 0))
        self.font = pygame.font.SysFont('arial', 30, True)
        self.score_text = self.font.render(f'Score = {self.score}', False, 'black')
        self.score_rect = self.score_text.get_rect(topleft = (0, 0))

        self.splash_text_1 = self.font.render('PRESS SPACE TO START GAME', False, 'black')
        self.splash_rect_1 = self.splash_text_1.get_rect(center = (constants.WIDTH / 2, constants.HEIGHT / 4))

        self.splash_text_2 = self.font.render('GREEN KILLS RED', False, 'black')
        self.splash_rect_2 = self.splash_text_2.get_rect(midtop = (constants.WIDTH / 2, self.splash_rect_1.bottom + 10))

        self.splash_text_3 = self.font.render('RED KILLS GREEN', False, 'black')
        self.splash_rect_3 = self.splash_text_3.get_rect(midtop = (constants.WIDTH / 2, self.splash_rect_2.bottom))

        self.splash_text_4 = self.font.render('SHIFT TO SWITCH COLOR', False, 'black')
        self.splash_rect_4 = self.splash_text_4.get_rect(midtop = (constants.WIDTH / 2, self.splash_rect_3.bottom + 10))

        self.splash_text_5 = self.font.render('SPACE TO SHOOT', False, 'black')
        self.splash_rect_5 = self.splash_text_5.get_rect(midtop = (constants.WIDTH / 2, self.splash_rect_4.bottom))
        
    def get_input(self):
        self.keys_pressed = pygame.key.get_pressed()

    def run_player(self):
        self.player_con.keys_pressed = self.keys_pressed

        self.player_con.player_move()
        self.player_con.player_flip()
        self.player_con.player_fire(self.p_las_group, self.all_sprites)
        self.player_con.player_reset()

        for laser in self.p_las_group:
            laser.move_up(constants.L_SPD)
            if laser.rect.bottom < -5:
                laser.kill()

    def run_enemies(self):
        self.enemy_con.enemy_spawn(self.e_group, self.all_sprites)
        self.enemy_con.enemy_move(self.e_group)
        self.enemy_con.enemy_fire(self.e_group, self.e_las_group, self.all_sprites)
        self.enemy_con.enemy_reset_spawn()
        self.enemy_con.enemy_reset_fire(self.e_group)

        for laser in self.e_las_group:
            laser.move_down(constants.L_SPD)
            if laser.rect.top > constants.HEIGHT:
                laser.kill()

    def collisions(self):
        # Player collisions:
        p_state = self.p_group.sprite.state
        for enemy in self.e_group:
            hit = pygame.sprite.collide_rect(self.p_group.sprite, enemy)
            if hit and p_state != enemy.state:
                self.playing = False
                pygame.time.wait(200)
            elif hit:
                enemy.kill()

        for laser in self.e_las_group:
            hit = pygame.sprite.collide_rect(self.p_group.sprite, laser)
            if hit and p_state != laser.state:
                self.playing = False
            elif hit:
                laser.kill()

        # Enemy collisions:
        for laser in self.p_las_group:
            for enemy in self.e_group:
                hit = pygame.sprite.collide_rect(enemy, laser)
                if hit and enemy.state != laser.state:
                    enemy.kill()
                    laser.kill()
                    self.score += 1
                elif hit:
                    laser.kill()

    def restart(self):
        if self.keys_pressed[pygame.K_SPACE]:
            for sprite in self.all_sprites:
                sprite.kill()
            self.p_group.sprite.rect.midbottom = (constants.WIDTH / 2, constants.HEIGHT - 20)
            self.score = 0
            self.score_text = self.font.render(f'Score = {self.score}', False, 'black')
            self.playing = True
            pygame.time.wait(300)
        
    def draw_playing(self):
        self.screen.fill(constants.BG_COLOR)
        for sprite in self.all_sprites:
            sprite.draw(self.screen)
        for sprite in self.p_group:
            sprite.draw(self.screen)
        self.screen.blit(self.score_band, self.score_band_rect)
        self.score_text = self.font.render(f'Score = {self.score}', False, 'black')
        self.screen.blit(self.score_text, self.score_rect)
        
    def draw_static(self):
        self.screen.fill(constants.BG_COLOR)
        self.screen.blit(self.splash_text_1, self.splash_rect_1)
        self.screen.blit(self.splash_text_2, self.splash_rect_2)
        self.screen.blit(self.splash_text_3, self.splash_rect_3)
        self.screen.blit(self.splash_text_4, self.splash_rect_4)
        self.screen.blit(self.splash_text_5, self.splash_rect_5)

    def run(self):
        if self.playing:
            self.get_input()
            self.run_player()
            self.run_enemies()
            self.collisions()
            self.draw_playing()
            pygame.display.flip()
        else:
            self.get_input()
            self.draw_static()
            self.restart()
            pygame.display.flip()


if __name__ == '__main__':

    pygame.init()

    clock = pygame.time.Clock()

    game = Game()
    run = True

    while run:
        game.run()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        clock.tick(constants.FPS)

    pygame.quit()
















        
