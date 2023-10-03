import pygame as pg
import sys
import random as ran
from .dice import Dice
from .utils import *

class StartMenu:

    def __init__(self,screen, clock):
        self.screen = screen
        self.clock = clock
        self.screen_size = self.screen.get_size()

        self.onePlayer_surf = pg.Surface((300,50))
        self.onePlayer_surf.fill((19, 116, 60))
        self.onePlayer_rect = self.onePlayer_surf.get_rect(topleft=(self.screen_size[0]*0.4, self.screen_size[1]*0.5))

        self.twoPlayer_surf = pg.Surface((300, 50)) 
        self.twoPlayer_surf.fill((19, 116, 60))
        self.twoPlayer_rect = self.twoPlayer_surf.get_rect(topleft=(self.screen_size[0]*0.4, self.screen_size[1]*0.6))

        self.tutorial_surf = pg.Surface((300, 50))
        self.tutorial_surf.fill((19, 116, 60))
        self.tutorial_rect = self.tutorial_surf.get_rect(topleft=(self.screen_size[0]*0.4, self.screen_size[1]*0.7))

        self.settings_surf = pg.Surface((300, 50))
        self.settings_surf.fill((19, 116, 60))
        self.settings_rec = self.settings_surf.get_rect(topleft=(self.screen_size[0]*0.4, self.screen_size[1]*0.8))

        self.number_dice = ran.randrange(1,7)

        self.number_dice = self.menuDice_management.get_random_number()
        self.number_color = self.menuDice_management.get_random_color()
        self.dice = Dice(self.number_color, self.number_dice)
        self.dice.dice_surf = pg.transform.scale(self.dice.dice_surf,(150,150))

        # randomize starting position
        self.x_move = ran.randrange(0,self.screen_size[0])
        self.y_move = ran.randrange(0,self.screen_size[1])

        # [x,y,randomize_dice]
        self.movementAndColor_list = [randomize_boolean(), randomize_boolean(), False]

        self.clicked_button = ''

        #(1536, 864)
        

    def run(self):
        self.menu_running = True
        while self.menu_running:
            self.clock.tick(60)
            self.update()
            self.draw(self.screen)
        return self.clicked_button
    
    def update(self):

        if self.movementAndColor_list[0] == True:
            self.x_move += 5
        if self.movementAndColor_list[0] == False:
            self.x_move -= 5
        if self.movementAndColor_list[1] == True:
            self.y_move -= 5
        if self.movementAndColor_list[1] == False:
            self.y_move += 5

        self.dice.set_position(self.x_move, self.y_move)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                #if event.key == pg.K_RETURN:
                #    self.menu_running = False
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            if event.type == pg.MOUSEBUTTONUP:
                if self.onePlayer_rect.collidepoint(event.pos):
                    play_click_sound()
                    self.clicked_button = 'onePlayer'
                if self.twoPlayer_rect.collidepoint(event.pos):
                    self.menu_running = False
                    play_click_sound()
                    self.clicked_button = 'twoPlayer'
                if self.tutorial_rect.collidepoint(event.pos):
                    play_click_sound()
                    self.clicked_button = 'tutorial'
                if self.settings_rec.collidepoint(event.pos):
                    self.menu_running = False
                    play_click_sound()
                    self.clicked_button = 'settings'

        if self.movementAndColor_list[2] == True:
            self.number_dice = self.menuDice_management.get_random_number()
            self.number_color = self.menuDice_management.get_random_color()
            self.dice.set_color(self.number_color)
            self.dice.set_dice_number(self.number_dice)
            self.dice.dice_surf = pg.transform.scale(self.dice.dice_surf,(150,150))
            self.movementAndColor_list[2] = False

        self.movementAndColor_list  = self.menuDice_management.border_colision_detect(self.screen_size, self.movementAndColor_list, self.x_move, self.y_move)

    def draw(self,screen):

        self.screen.fill((34, 153, 84))

        self.dice.draw(self.screen)

        screen.blit(self.onePlayer_surf, self.onePlayer_rect)
        screen.blit(self.twoPlayer_surf, self.twoPlayer_rect)
        screen.blit(self.tutorial_surf, self.tutorial_rect)
        screen.blit(self.settings_surf, self.settings_rec)
        draw_text(self.screen, 'Dice Game', 200, (255, 255, 255), (self.screen_size[0]*0.25, self.screen_size[1]*0.2))
        draw_text(self.screen, 'One Player', 75, (255, 255, 255), (self.screen_size[0]*0.4, self.screen_size[1]*0.5))
        draw_text(self.screen, 'Two Players', 75, (255, 255, 255), (self.screen_size[0]*0.4, self.screen_size[1]*0.6))
        draw_text(self.screen, 'Tutorial', 75, (255,255,255), (self.screen_size[0]*0.4, self.screen_size[1]*0.7))
        draw_text(self.screen, 'Settings', 75, (255,255,255), (self.screen_size[0]*0.4, self.screen_size[1]*0.8))

        pg.display.flip()

    class menuDice_management:

        def get_random_number():
            number_dice = ran.randrange(1,7)
            return number_dice
        
        def get_random_color():
            color_list = ['green','magenta','red']
            number_color = ran.randrange(0,3)
            return color_list[number_color]

        def border_colision_detect(screen_size, movementAndColor_list, x_move, y_move):
            
            aux_move_list = movementAndColor_list

            if x_move >= screen_size[0]:
                aux_move_list[0] = False
                aux_move_list[2] =True
            if x_move <= screen_size[0]*-0.1:
                aux_move_list[0] = True
                aux_move_list[2] =True
            if y_move >= screen_size[1]:
                aux_move_list[1] = True
                aux_move_list[2] =True
            if y_move <= screen_size[1]*-0.1:
                aux_move_list[1] = False
                aux_move_list[2] =True

            return aux_move_list


class GameMenu:

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.screen_size = self.screen.get_size()
        self.playing = True

    def run(self):
        self.menu_running = True
        while self.menu_running:
            self.clock.tick(60)
            self.update()
            self.draw()
        return self.playing
    
    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.menu_running = False
                    self.playing = True
                if event.key == pg.K_ESCAPE:
                    self.playing = False
                    self.menu_running = False

    def draw(self):

        #self.screen.fill((0, 0, 0))

        draw_text(self.screen,
                  'PAUSE',
                  100,
                  (0,0,0),
                  (0, self.screen_size[1]*0.3)
                  )
        draw_text(self.screen,
                  'ESC to quit, ENTER to play',
                  60,
                  (0,0,0),
                  (0, self.screen_size[1]*0.5)
                  )

        pg.display.flip()



class Settings:
    
    def __init__(self,screen, clock):
        self.screen = screen
        self.clock = clock
        self.screen_size = self.screen.get_size()
        

    def run(self):
        self.menu_running = True
        while self.menu_running:
            self.clock.tick(60)
            self.update()
            self.draw(self.screen)
        return self.playing
    
    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                """if event.key == pg.K_RETURN:
                    self.menu_running = False
                    self.playing = True"""
                if event.key == pg.K_ESCAPE:
                    self.playing = False
                    self.menu_running = False

    def draw(self,screen):
        self.screen.fill((255, 255, 255))
        pg.display.flip()