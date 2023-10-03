import pygame as pg

class Dice:

    def __init__(self, color, number):
        self.color = color
        self.number = number
        self.width = 100
        self.height = 100
        self.diceList = []
        self.set_dices()
        self.set_color(self.color)
        self.set_dice_number(self.number)
        self.dice_rect = self.dice_surf.get_rect(topleft = (self.width, self.height))

    def update(self, numberChange):
        self.set_dice_number(numberChange)

    def set_dice_number(self, numberChange):
        index = numberChange -1
        self.dice_surf = self.diceList[index]

    def set_position(self, width, height):
        self.width = width
        self.height = height

        self.dice_rect = self.dice_surf.get_rect(topleft = (self.width, self.height))

    def set_color(self, color):
        if color == 'green':
            self.diceList = self.greenDice
        elif color == 'magenta':
            self.diceList = self.magentaDice
        elif color == 'red':
            self.diceList = self.redDice

    def set_dices(self):

        greenDice_1 = pg.image.load('assets/dice_sprites/diceGreen1.png').convert_alpha()
        greenDice_2 = pg.image.load('assets/dice_sprites/diceGreen2.png').convert_alpha()
        greenDice_3 = pg.image.load('assets/dice_sprites/diceGreen3.png').convert_alpha()
        greenDice_4 = pg.image.load('assets/dice_sprites/diceGreen4.png').convert_alpha()
        greenDice_5 = pg.image.load('assets/dice_sprites/diceGreen5.png').convert_alpha()
        greenDice_6 = pg.image.load('assets/dice_sprites/diceGreen6.png').convert_alpha()
        self.greenDice = [greenDice_1, greenDice_2, greenDice_3, greenDice_4, greenDice_5, greenDice_6]

        magentaDice_1 = pg.image.load('assets/dice_sprites/diceMagenta1.png').convert_alpha()
        magentaDice_2 = pg.image.load('assets/dice_sprites/diceMagenta2.png').convert_alpha()
        magentaDice_3 = pg.image.load('assets/dice_sprites/diceMagenta3.png').convert_alpha()
        magentaDice_4 = pg.image.load('assets/dice_sprites/diceMagenta4.png').convert_alpha()
        magentaDice_5 = pg.image.load('assets/dice_sprites/diceMagenta5.png').convert_alpha()
        magentaDice_6 = pg.image.load('assets/dice_sprites/diceMagenta6.png').convert_alpha()
        self.magentaDice = [magentaDice_1, magentaDice_2, magentaDice_3, magentaDice_4, magentaDice_5, magentaDice_6]

        redDice_1 = pg.image.load('assets/dice_sprites/diceRed1.png').convert_alpha()
        redDice_2 = pg.image.load('assets/dice_sprites/diceRed2.png').convert_alpha()
        redDice_3 = pg.image.load('assets/dice_sprites/diceRed3.png').convert_alpha()
        redDice_4 = pg.image.load('assets/dice_sprites/diceRed4.png').convert_alpha()
        redDice_5 = pg.image.load('assets/dice_sprites/diceRed5.png').convert_alpha()
        redDice_6 = pg.image.load('assets/dice_sprites/diceRed6.png').convert_alpha()
        self.redDice = [redDice_1, redDice_2, redDice_3, redDice_4, redDice_5, redDice_6]

    def draw(self,screen):
        screen.blit(self.dice_surf, self.dice_rect)
