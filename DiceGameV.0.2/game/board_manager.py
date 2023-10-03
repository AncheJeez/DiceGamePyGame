
class Board_manager:

    def __init__(self):

        self.nested_dict = {
            'first_column': {'1row': 0, '2row': 0, '3row': 0},
            'second_column': {'1row': 0, '2row': 0, '3row': 0},
            'third_column': {'1row': 0, '2row': 0, '3row': 0}
        }

        self.duplicative_state = [False,False,False]
        self.triplicative_state = [False,False,False]
        self.score_list = [0,0,0]
        self.full_list = [False,False,False]

    # prints the nested_dict
    def get_nested_dict_print(self):

        for column_id, row_id in self.nested_dict.items():
            print("Id column:", column_id)

            for key in row_id:
                print(key + ':', row_id[key])

    # prints the state lists
    def get_state_list(self):
        print("DUPLICATIVE STATES:")
        for i in self.duplicative_state:
            print(i)
        print("TRIPLICATIVE STATES:")
        for j in self.triplicative_state:
            print(j)
        print("\n")

    # method to get an expecific state (to get the color in Board())
    def get_state(self, given_column, given_row):

        aux_list = [0,0]
        cont = 0
        DiceNumber = -1
        
        # we introduce the other 2 numbers in the same column in the list, so we can compare
        for column_id, row_id in self.nested_dict.items():
            
            column_int = self.get_numberFromString(column_id)

            if given_column == column_int:

                for key in row_id:

                    if key == given_row:
                        DiceNumber = row_id[key]
                    else:
                        aux_list[cont] = row_id[key]
                        cont+= 1
        
        if (aux_list[0] == DiceNumber or aux_list[1] == DiceNumber) and (aux_list[0] != 0):
            color = 'magenta'
            if aux_list[0] == aux_list[1]:
                color = 'red'
        else:
            color = 'green'
        
        return color
            
    # prints the score
    def print_score(self):
        score = self.get_total_score()
        print("SCORE:",score,"\n")

    # this method deletes a content of the nested_dict, given the number and column
    def delete_dices(self, number_given, column):
        for column_id, row_id in self.nested_dict.items():
            number = self.get_numberFromString(column_id)
            if column_id == column:
                for key in row_id:
                    if row_id[key] == number_given:
                        row_id[key] = 0
                        print("ELIMINADO DADO",number_given,"DE LA COLUMNA",column)
                        self.get_score_and_update_states()
    
    # this method sorts the nested_dict, so if it has a cero below, all the numbers above drop
    def sort_board(self):
        for column_id, row_id in self.nested_dict.items():
            sorted_rows = {k: v for k, v in sorted(row_id.items(), key=lambda item: item[1], reverse=True)}
            self.nested_dict[column_id] = sorted_rows

    # this method inserts a dice given the number and the column
    def insert_dice(self, number, column):
        for column_id, row_id in self.nested_dict.items():
            if column_id == column:
                for key in row_id:
                    if row_id[key] == 0:
                        row_id[key] = number
                        self.get_score_and_update_states()
                        self.sort_board()
                        if key == '3row':
                            self.full_list[self.get_numberFromString(column_id)] = True

                        break

    # this method translates a String into a integer number, in case the String is not readable it returns -1
    def get_numberFromString(self, String):
        if String == 'first_column':
            return 0
        elif String == 'second_column':
            return 1
        elif String == 'third_column':
            return 2
        else:
            return -1
    
    # this method gives the score of a column, given the column
    def get_score_and_update_states(self):
        
        # iteration of the nested_dict by column
        for column_id, row_id in self.nested_dict.items():

            column_int = self.get_numberFromString(column_id)

            # helpful atributes
            self.simple_sum_score = 0
            self.init_slot = -1
            self.comparing_slot = -2
            self.save_number = -3

            # we reset the states of the column
            self.duplicative_state[column_int] = False
            self.triplicative_state[column_int] = False

            # iteration of the nested_dict by row
            for key in row_id:

                # when last check slot or the first slot saved is equal as the current slot
                if self.comparing_slot == row_id[key] or self.init_slot == row_id[key]:

                    # if conditions of Triplicative state
                    if self.duplicative_state[column_int] == True and self.init_slot == row_id[key]:
                        self.triplicative_state[column_int] = True
                        self.duplicative_state[column_int] = False
                    # if conditions of Duplicative state
                    elif self.duplicative_state[column_int] == False:
                        self.duplicative_state[column_int] = True
                        # we save the number so in case we have 2 duplicating number but 1 number which is not, we know the duplicating one
                        self.save_number = row_id[key]
                # when no match the current slot, reset the comparing slot
                else:
                    self.comparing_slot = -2

                # we save the initial slot
                if self.init_slot == -1 and row_id[key] != 0:
                    self.init_slot = row_id[key]
                # we save the current slot so we can check next slot
                if self.comparing_slot == -2 and row_id[key] != 0:
                    self.comparing_slot = row_id[key]

                # each turn we sum the current slot number for calculation purposes
                self.simple_sum_score += row_id[key]
                
                # we declare if the column is false
                if row_id['3row'] == 0:
                    self.full_list[column_int] = False

            # we calculate the score of the column and save in the score_list
            score_column = self.calculate_score(column_int)
            self.score_list[column_int] = score_column

    # this method gives the total score of the board
    def get_total_score(self):
        total_score = 0
        for score in self.score_list:
            total_score += score
        return total_score

    # this method calculates the score of the column, used by get_score_column()
    def calculate_score(self, column):
        if self.duplicative_state[column]:
            return (self.simple_sum_score - (self.save_number*2) + (self.save_number*2)*2)
        if self.triplicative_state[column]:
            return self.simple_sum_score * 3
        else:
            return self.simple_sum_score

    # method to know if the nested_dict is full
    def check_if_full(self):
        cont = 0
        for state in self.full_list:
            if state == True:
                cont += 1
        if cont >= 3:
            return True
        else:
            return False

"""Board_one = Board_manager()


Board_one.insert_dice(5,'first_column')
Board_one.insert_dice(5,'first_column')
Board_one.insert_dice(2,'second_column')
Board_one.insert_dice(5,'second_column')
Board_one.insert_dice(2,'second_column')

Board_one.delete_dices(2,'second_column')

Board_one.get_nested_dict_print()
score = Board_one.get_total_score()
print("THE TOTAL SCORE IS:", score,"\n")
Board_one.get_state_list()"""

