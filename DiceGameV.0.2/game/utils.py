import pygame as pg
import random as ran


def draw_text(screen, text, size, colour, pos):

    font = pg.font.SysFont(None, size)
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect(topleft=pos)

    screen.blit(text_surface, text_rect)

def randomize_boolean():

    random_number = ran.randrange(0,2)

    if random_number == 0:
        return False
    if random_number == 1:
        return True
    else: return True

def get_color(turn_name):
    if turn_name == 'Player 1':
        color = (0,128,0)
    elif turn_name == 'Player 2':
        color = (255, 64, 0)
    else:
        color = (255, 255, 255)
    return color

def play_click_sound():

    click_sound = pg.mixer.Sound('assets/audio/Toom_Click.wav')

    click_sound.play()