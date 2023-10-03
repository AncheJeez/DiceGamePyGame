import pygame as pg
import sys
import random as ran
from .board import Board
from .board_manager import Board_manager
from .dice import Dice
from .utils import *

class Game:

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.screen_size = self.screen.get_size()
        self.width, self.height = self.screen.get_size() # this for hud

        self.reset_game()

        dice_roll_1 = pg.mixer.Sound('assets/audio/dice_roll_1.flac')
        dice_roll_2 = pg.mixer.Sound('assets/audio/dice_roll_2.flac')
        dice_roll_3 = pg.mixer.Sound('assets/audio/dice_roll_3.flac')
        dice_roll_4 = pg.mixer.Sound('assets/audio/dice_roll_4.flac')

        self.dice_roll_list = [dice_roll_1, dice_roll_2, dice_roll_3, dice_roll_4]

    # method run
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    # method to register player's events
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.playing = False
                    play_click_sound()
                if event.key == pg.K_r:
                    self.number = ran.randrange(1,7)
                    self.play_ran_roll_sound()
            if self.playable == True:
                if event.type == pg.MOUSEBUTTONUP:
                    print("\nDETECTED INPUT IN:")
                    if self.turn_state == False:
                        if self.boardBot.boardFirstCol_rect.collidepoint(event.pos):
                            print("Bot First Column")
                            self.botBoardVar = 'first_column'
                            #self.turn_state = True
                        if self.boardBot.boardSecondCol_rect.collidepoint(event.pos):
                            print("Bot Second Column")
                            self.botBoardVar = 'second_column'
                            #self.turn_state = True
                        if self.boardBot.boardThirdCol_rect.collidepoint(event.pos):
                            print("Bot Third Column")
                            self.botBoardVar = 'third_column'
                            #self.turn_state = True
                    if self.turn_state == True:
                        if self.boardTop.boardFirstCol_rect.collidepoint(event.pos):
                            print("Top First Column")
                            self.topBoardVar = 'first_column'
                        if self.boardTop.boardSecondCol_rect.collidepoint(event.pos):
                            print("Top Second Column")
                            self.topBoardVar = 'second_column'
                        if self.boardTop.boardThirdCol_rect.collidepoint(event.pos):
                            print("Top Third Column")
                            self.topBoardVar = 'third_column'

    # method update
    def update(self):
        self.dice.update(self.number)
        self.turn()

    # method draw
    def draw(self):
        self.screen.fill((11, 167, 192))
        self.boardTop.draw(self.screen)
        self.boardBot.draw(self.screen)
        self.dice.draw(self.screen)
        color = get_color(self.turn_name)
        draw_text(self.screen, self.turn_name, 100, color, (self.screen_size[1]*0.15,self.screen_size[0]*0.35))
        if self.playable == False:
            draw_text(self.screen, self.win_message, 200, (255,0,255), (self.screen_size[1]*0.2, self.screen_size[0]*0.25))
        pg.display.flip()

    # method to check each players turn
    def turn(self):
        
        turn = self.turn_state

        #TURN OF PLAYER 1
        if turn == False and self.botBoardVar != '':
            self.turn_name = 'Player 1'

            self.play_ran_roll_sound()

            # we insert dice, request number of the dice and column inserted
            self.boardBot.board_manager.insert_dice(self.number, self.botBoardVar)

            # we check both boards
            self.check_boards(self.boardBot.board_manager, self.boardTop.board_manager)

            self.boardBot.update_dice_storage()
            self.boardTop.update_dice_storage()

            self.boardTop.board_manager.get_nested_dict_print()
            self.boardBot.board_manager.get_nested_dict_print()

            # we reset the column as we ended the turn
            self.botBoardVar = ''
            self.turn_state = True
            self.number = ran.randrange(1,7)

        #TURN OF PLAYER 2
        elif turn == True and self.topBoardVar != '':
            self.turn_name = 'Player 2'

            self.play_ran_roll_sound()

            # we insert dice, request number of the dice and column inserted
            self.boardTop.board_manager.insert_dice(self.number, self.topBoardVar)

            # we check both boards
            self.check_boards(self.boardTop.board_manager, self.boardBot.board_manager)

            self.boardTop.update_dice_storage()
            self.boardBot.update_dice_storage()

            self.boardTop.board_manager.get_nested_dict_print()
            self.boardBot.board_manager.get_nested_dict_print()

            # we reset the column as we ended the turn
            self.topBoardVar = ''
            self.turn_state = False
            self.number = ran.randrange(1,7)

        if self.boardTop.board_manager.check_if_full() == True or self.boardBot.board_manager.check_if_full() == True:
            topScore = self.boardTop.board_manager.get_total_score()
            botScore = self.boardBot.board_manager.get_total_score()
            
            if topScore > botScore:
                self.win_message = "TOP BOARD WON!!!"
            elif topScore < botScore:
                self.win_message = "BOT BOARD WON!!!"
            elif topScore == botScore:
                self.win_message = "IT'S A TIE!!!"
            self.playable = False

    # method to check both boards and delete dices if necessary
    def check_boards(self, turnsBoardManager, noTurnsBoardManager):
        
        for column_id, row_id in turnsBoardManager.nested_dict.items():
            for key, value in row_id.items():
                if value != 0:
                    for column_id_2, row_id_2 in noTurnsBoardManager.nested_dict.items():
                        if column_id == column_id_2:
                            for key_2, value_2 in row_id_2.items():
                                if value == value_2:
                                    print("THEY ARE THE SAME:", value, value_2, column_id, column_id_2, key, key_2)
                                    print("removing dices")
                                    noTurnsBoardManager.delete_dices(value_2, column_id_2)

    # method to reset the game if exited
    def reset_game(self):
        self.number = ran.randrange(1,7)
        self.dice = Dice('green', self.number)

        self.boardTop = Board('Player 1', self.screen_size[1]*0.65,self.screen_size[1]*0.08)
        self.boardBot = Board('Player 2', self.screen_size[1]*0.65,self.screen_size[1]*0.56)

        # True = Player's turn || False = A.I.'s turn
        self.turn_state = False
        self.turn_name = 'Player 2'

        self.topBoardVar = ''
        self.botBoardVar = ''

        self.playable = True
        self.win_message = ''

    # method to play random roll sound of the dice
    def play_ran_roll_sound(self):
        
        number = ran.randrange(0,4)

        self.dice_roll_list[number].play()

class Game_ai:
    
    def __init__(self, screen, clock):
        pass

    def run():
        pass
    