import pygame as pg
from game.game import Game
from game.menu import StartMenu, GameMenu, Settings

def main():

    running = True

    pg.init()
    pg.mixer.init()
    #screen = pg.display.set_mode((1000,800))
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    clock = pg.time.Clock()

    # implement menus
    start_menu = StartMenu(screen, clock)
    game_menu = GameMenu(screen, clock)

    settings_menu = Settings(screen, clock)

    # implement game
    game = Game(screen, clock)
    game_ai = Game(screen, clock)

    while running:
        
        # start menu
        running_mode = start_menu.run()

        if running_mode != '':
            playing = True
        else:
            playing = False
        
        if running_mode == 'onePlayer':
            while playing:
                # game loop
                game_ai.run()
                #pause loop
                playing = game_menu.run()
            running_mode == ''

        if running_mode == 'twoPlayer':
            while playing:
                # game loop
                game.run()
                # pause loop
                playing = game_menu.run()
            running_mode == ''

        """if running_mode == 'tutorial':
            while playing:
                playing = tutorial_menu.run
            running_mode == ''"""
        
        if running_mode == 'settings':
            while playing:
                # menu loop
                settings_menu.run()
                # pause loop
                playing == settings_menu.run()
            running_mode == ''

        # reset game
        game.reset_game()


if __name__ == "__main__":
    main()