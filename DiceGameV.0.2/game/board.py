import pygame as pg
from .utils import draw_text
from .board_manager import Board_manager
from .dice import Dice
from .utils import *

class Board:

    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height
        self.set_board(width, height)
        self.board_manager = Board_manager()
        self.nested_dict = self.board_manager.nested_dict
        
        self.firstColList = []
        self.secondColList = []
        self.thirdColList = []
        self.dicesStored_byColumn = [self.firstColList ,self.secondColList, self.thirdColList]

    # this method sets the board surface and rectangle
    def set_board(self, width, height):
        GrayBoard = pg.image.load('assets/tablero.png').convert_alpha()
        self.board_surf = pg.transform.scale(GrayBoard, (351, 351))
        self.board_rect = self.board_surf.get_rect(topleft = (width, height))

        width = (self.board_rect.width / 3 ) # = 117
        height = self.board_rect.height # 351
        self.boardFirstCol_surf = pg.Surface((width, height))
        self.boardFirstCol_surf.fill('Red')
        self.boardFirstCol_rect = self.boardFirstCol_surf.get_rect(topleft = (self.board_rect.x, self.board_rect.y))

        self.boardSecondCol_surf = pg.Surface((width, height))
        self.boardSecondCol_surf.fill('Blue')
        self.boardSecondCol_rect = self.boardSecondCol_surf.get_rect(topleft = ((self.board_rect.x)+117, self.board_rect.y))

        self.boardThirdCol_surf = pg.Surface((width, height))
        self.boardThirdCol_surf.fill('Green')
        self.boardThirdCol_rect = self.boardThirdCol_surf.get_rect(topleft = ((self.board_rect.x)+234, self.board_rect.y))

    #this method will store the dices from the nested_dict into a Dice() object list
    def update_dice_storage(self):

        self.clear_storageList()
        
        # we iterate through the nested_dict
        for column_id, row_id in self.nested_dict.items():
            
            column = self.board_manager.get_numberFromString(column_id)

            for key in row_id:
                if row_id[key] != 0:

                    # we get the color for the dice
                    color = self.board_manager.get_state(column, key)

                    # we create the dice
                    self.dice = Dice(color, row_id[key])
                    self.dice.dice_surf = pg.transform.scale(self.dice.diceList[row_id[key]-1], (114,114))

                    # introduce in the "dicesStored_byColumn" list
                    self.put_dice_board(column)
    
    # this method will put the dice in the list and set positions x and y
    def put_dice_board(self, given_column):

        # we append it to the list
        self.dicesStored_byColumn[given_column].append(self.dice)
        
        row = len(self.dicesStored_byColumn[given_column])-1
        position_x = self.width + (given_column) * 114
        position_y = (self.height) + 234 - (row * 114)

        # it sets the position and creates the dice's rectangle
        self.dice.set_position(position_x, position_y)

    # this method clears the stored dices, reseting it to empty
    def clear_storageList(self):
        
        self.firstColList.clear()
        self.secondColList.clear()
        self.thirdColList.clear()

    # this method draws the board and the dices + the collision boxes
    def draw(self, screen):

        # this draws the colission with cursos boxes, but we redraw above the board so i cannot be seen
        screen.blit(self.boardFirstCol_surf, self.boardFirstCol_rect)
        screen.blit(self.boardSecondCol_surf, self.boardSecondCol_rect)
        screen.blit(self.boardThirdCol_surf, self.boardThirdCol_rect)
        
        # the board
        screen.blit(self.board_surf, self.board_rect)

        # we place  the dices from the lists
        for dice_obj in self.firstColList:
            dice_to_place = dice_obj
            screen.blit(dice_to_place.dice_surf,dice_to_place.dice_rect)

        for dice_obj in self.secondColList:
            dice_to_place = dice_obj
            screen.blit(dice_to_place.dice_surf, dice_to_place.dice_rect)

        for dice_obj in self.thirdColList:
            dice_to_place = dice_obj
            screen.blit(dice_to_place.dice_surf, dice_to_place.dice_rect)

        # we draw the name and the score of each board
        color = get_color(self.name)
        draw_text(screen, self.name, 40, color, (self.width, (self.height)-30))
        draw_text(screen, str(self.board_manager.get_total_score()), 40, (255, 255, 255), ((self.width)+300, (self.height)-30))
