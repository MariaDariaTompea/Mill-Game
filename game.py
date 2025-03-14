from exception import *
from board import Board
from coordinates import Coordinates
from random import randint


class Game:
    def __init__(self, board: Board, coord: Coordinates):
        self.__board = board
        self.__coord = coord

        self.__user_stage = 1
        self.__user_old_stage = 1
        self.__user_nr_placed = 0
        self.__user_nr_left = 0

        self.__computer_stage = 1
        self.__computer_nr_placed = 0
        self.__computer_nr_left = 0

        self.__nr_move = 0  # nr_move without taken piece = 10 => draw game

    def get_computer_stage(self):
        return self.__computer_stage

    def get_user_stage(self):
        return self.__user_stage

    def set_user_stage(self, current_user_stage):
        self.__user_stage = current_user_stage

    def get_user_old_stage(self):
        return self.__user_old_stage

    def set_user_old_stage(self, current_user_stage):
        self.__user_old_stage = current_user_stage

    def validate_position(self, position):
        valid_position = self.__coord.get_all_poz_on_board()
        if position not in valid_position:
            raise NotAValidPosition()

    def update_position(self, position: str, symbol: int):
        list_coord = self.__coord.get_matrix_coordinates(position)
        self.__board.set_symbol_at_postion(list_coord[0], list_coord[1], symbol)

    def move_user(self, position_1, position_2):
        self.update_position(position_1, 0)
        self.update_position(position_2, 1)

    def move_computer(self, position_1, position_2):
        self.update_position(position_1, 0)
        self.update_position(position_2, 2)

    def make_user_move_1(self, position: str):      # user - stage 1
        self.validate_position(position)
        free_position = self.get_free_position()
        if position not in free_position:
            raise PositionAlreadyTaken()
        self.update_position(position, 1)
        self.__user_nr_placed += 1
        self.__user_nr_left += 1
        if self.__user_nr_placed == 9:
            if self.__user_stage == 1:
                self.__user_stage = 2

    def make_user_move_2(self, position_1: str, position_2: str):   # user - stage 2
        self.validate_position(position_1)
        lin, col = self.__coord.get_matrix_coordinates(position_1)
        if self.__board.get_symbol_at_postion(lin, col) != 1:
            raise NotOwner()

        self.validate_position(position_2)
        lin, col = self.__coord.get_matrix_coordinates(position_2)
        if self.__board.get_symbol_at_postion(lin, col) != 0:
            raise NotFreePosition()

        if not self.__coord.is_adiacent_position(position_1, position_2):
            raise NotAdiacentPosition()

        self.move_user(position_1, position_2)
        self.__nr_move += 1

    def make_user_move_3(self, position_1: str, position_2: str):   # user - stage 3
        self.validate_position(position_1)
        lin, col = self.__coord.get_matrix_coordinates(position_1)
        if self.__board.get_symbol_at_postion(lin, col) != 1:
            raise NotOwner()

        self.validate_position(position_2)
        lin, col = self.__coord.get_matrix_coordinates(position_2)
        if self.__board.get_symbol_at_postion(lin, col) != 0:
            raise NotFreePosition()

        self.move_user(position_1, position_2)
        self.__nr_move += 1

    def make_user_take_piece(self, position):       # user stage 4
        self.validate_position(position)
        lin, col = self.__coord.get_matrix_coordinates(position)
        if self.__board.get_symbol_at_postion(lin, col) != 2:
            raise NotEnemy()
        if self.computer_has_free_position():
            if self.is_in_mill_of_computer(position):
                raise MillTakingPlace()
        self.update_position(position, 0)
        self.__computer_nr_left -= 1
        if self.__computer_nr_left <= 3 and self.__computer_nr_placed == 9:
            self.__computer_stage = 3
        self.__nr_move = 0

    def computer_has_free_position(self):   # position not in mils
        comp_poz = self.get_computer_position()
        for poz in comp_poz:
            if not self.is_in_mill_of_computer(poz):
                return True
        return False

    def player_has_free_position(self):  # position not in mils
        comp_poz = self.get_user_position()
        for poz in comp_poz:
            if not self.is_in_mill_of_player(poz):
                return True
        return False

    def made_player_mills(self) -> bool:
        triples = self.__coord.get_all_possible_mills()

        for triple in triples:
            list_coord = self.__coord.get_matrix_coordinates(triple[0])
            v0 = self.__board.get_symbol_at_postion(list_coord[0], list_coord[1])

            list_coord = self.__coord.get_matrix_coordinates(triple[1])
            v1 = self.__board.get_symbol_at_postion(list_coord[0], list_coord[1])

            list_coord = self.__coord.get_matrix_coordinates(triple[2])
            v2 = self.__board.get_symbol_at_postion(list_coord[0], list_coord[1])
            if v0 * v1 * v2 == 1:
                return True
        return False

    def is_in_mill_of_player(self, position):
        mills = self.__coord.get_all_possible_poz_in_mills()
        triples = mills[position]
        for triple in triples:
            list_coord = self.__coord.get_matrix_coordinates(triple[0])
            v0 = self.__board.get_symbol_at_postion(list_coord[0], list_coord[1])

            list_coord = self.__coord.get_matrix_coordinates(triple[1])
            v1 = self.__board.get_symbol_at_postion(list_coord[0], list_coord[1])

            list_coord = self.__coord.get_matrix_coordinates(triple[2])
            v2 = self.__board.get_symbol_at_postion(list_coord[0], list_coord[1])
            if v0 * v1 * v2 == 1:
                return True
        return False

    def get_free_position(self):
        all_poz_board = self.__coord.get_all_poz_on_board()
        free_list = []
        for position in all_poz_board:
            list_coord = self.__coord.get_matrix_coordinates(position)
            if self.__board.get_symbol_at_postion(list_coord[0], list_coord[1]) == 0:
                free_list.append(position)
        return free_list

    def get_user_position(self):
        all_poz_board = self.__coord.get_all_poz_on_board()
        user_list = []
        for position in all_poz_board:
            list_coord = self.__coord.get_matrix_coordinates(position)
            if self.__board.get_symbol_at_postion(list_coord[0], list_coord[1]) == 1:
                user_list.append(position)
        return user_list

    def get_computer_position(self):
        all_poz_board = self.__coord.get_all_poz_on_board()
        computer_list = []
        for position in all_poz_board:
            list_coord = self.__coord.get_matrix_coordinates(position)
            if self.__board.get_symbol_at_postion(list_coord[0], list_coord[1]) == 2:
                computer_list.append(position)
        return computer_list

    def make_computer_move_1(self):
        poz = self.try_block_moris_in_stage_1()
        if poz == "00":
            poz = self.try_make_moris_in_stage_1()
            if poz == "00":
                free_poz = self.get_free_position()
                nr_poz = len(free_poz)
                poz = free_poz[randint(0, nr_poz - 1)]
        self.update_position(poz, 2)
        self.__computer_nr_placed += 1
        self.__computer_nr_left += 1
        if self.__computer_nr_placed == 9:
            if self.__computer_stage == 1:
                self.__computer_stage = 2
        return poz

    def try_block_moris_in_stage_1(self):
        block_poz = self.__coord.get_poz_block_mills()
        free_poz = self.get_free_position()
        for poz in free_poz:
            set_semi_mils = block_poz[poz]
            for semi_mils in set_semi_mils:
                poz_1 = semi_mils[0]
                poz_2 = semi_mils[1]
                list_coord = self.__coord.get_matrix_coordinates(poz_1)
                symbol_1 = self.__board.get_symbol_at_postion(list_coord[0], list_coord[1])
                list_coord = self.__coord.get_matrix_coordinates(poz_2)
                symbol_2 = self.__board.get_symbol_at_postion(list_coord[0], list_coord[1])
                if symbol_1 == 1 and symbol_2 == 1:
                    return poz
        return "00"

    def try_make_moris_in_stage_1(self):
        block_poz = self.__coord.get_poz_block_mills()
        free_poz = self.get_free_position()
        for poz in free_poz:
            set_semi_mils = block_poz[poz]
            for semi_mils in set_semi_mils:
                poz_1 = semi_mils[0]
                poz_2 = semi_mils[1]
                list_coord = self.__coord.get_matrix_coordinates(poz_1)
                symbol_1 = self.__board.get_symbol_at_postion(list_coord[0], list_coord[1])
                list_coord = self.__coord.get_matrix_coordinates(poz_2)
                symbol_2 = self.__board.get_symbol_at_postion(list_coord[0], list_coord[1])
                if symbol_1 == 2 and symbol_2 == 2:
                    return poz
        return "00"

    def make_computer_move_2(self):
        poz_start, poz_final = self.try_block_moris_in_stage_2()
        if poz_start != "00":
            self.move_computer(poz_start, poz_final)
            self.__nr_move += 1
            return poz_start, poz_final
        else:
            poz_start, poz_final = self.try_make_moris_in_stage_2()
            if poz_start != "00":
                self.move_computer(poz_start, poz_final)
                self.__nr_move += 1
                return poz_start, poz_final
            else:  # random moves
                free_poz = self.get_free_position()
                computer_poz = self.get_computer_position()
                random_moves = []
                for poz_start in computer_poz:
                    for poz_final in free_poz:
                        if self.__coord.is_adiacent_position(poz_start, poz_final) and poz_final != poz_start:
                            random_moves.append([poz_start, poz_final])
                if len(random_moves) != 0:
                    index = randint(0, len(random_moves)-1)
                    poz_start = random_moves[index][0]
                    poz_final = random_moves[index][1]
                    self.move_computer(poz_start, poz_final)
                    self.__nr_move += 1
                    return poz_start, poz_final

    def try_block_moris_in_stage_2(self):
        block_poz = self.__coord.get_poz_block_mills()
        free_poz = self.get_free_position()
        comp_poz = self.get_computer_position()
        for poz in free_poz:
            set_semi_mils = block_poz[poz]
            for semi_mils in set_semi_mils:
                poz_1 = semi_mils[0]
                poz_2 = semi_mils[1]
                list_coord = self.__coord.get_matrix_coordinates(poz_1)
                symbol_1 = self.__board.get_symbol_at_postion(list_coord[0], list_coord[1])
                list_coord = self.__coord.get_matrix_coordinates(poz_2)
                symbol_2 = self.__board.get_symbol_at_postion(list_coord[0], list_coord[1])
                if symbol_1 == 1 and symbol_2 == 1:
                    for comp in comp_poz:
                        if self.__coord.is_adiacent_position(comp, poz):
                            if comp != poz_1 and comp != poz_2:
                                return comp, poz
        return ["00", "00"]

    def try_make_moris_in_stage_2(self):
        block_poz = self.__coord.get_poz_block_mills()
        free_poz = self.get_free_position()
        comp_poz = self.get_computer_position()
        for poz in free_poz:
            set_semi_mils = block_poz[poz]
            for semi_mils in set_semi_mils:
                poz_1 = semi_mils[0]
                poz_2 = semi_mils[1]
                list_coord = self.__coord.get_matrix_coordinates(poz_1)
                symbol_1 = self.__board.get_symbol_at_postion(list_coord[0], list_coord[1])
                list_coord = self.__coord.get_matrix_coordinates(poz_2)
                symbol_2 = self.__board.get_symbol_at_postion(list_coord[0], list_coord[1])
                if symbol_1 == 2 and symbol_2 == 2:
                    for comp in comp_poz:
                        if self.__coord.is_adiacent_position(comp, poz):
                            if comp != poz_1 and comp != poz_2:
                                return comp, poz
        return ["00", "00"]

    def make_computer_move_3(self):
        poz_start, poz_final = self.try_block_moris_in_stage_3()
        if poz_start != "00":
            self.move_computer(poz_start, poz_final)
            self.__nr_move += 1
            return poz_start, poz_final
        else:
            poz_start, poz_final = self.try_make_moris_in_stage_2()
            if poz_start != "00":
                self.move_computer(poz_start, poz_final)
                self.__nr_move += 1
                return poz_start, poz_final
            else:  # random moves
                free_poz = self.get_free_position()
                computer_poz = self.get_computer_position()
                random_moves = []
                for poz_start in computer_poz:
                    for poz_final in free_poz:
                        random_moves.append([poz_start, poz_final])
                if len(random_moves) != 0:
                    index = randint(0, len(random_moves)-1)
                    poz_start = random_moves[index][0]
                    poz_final = random_moves[index][1]
                    self.move_computer(poz_start, poz_final)
                    self.__nr_move += 1
                    return poz_start, poz_final

    def try_block_moris_in_stage_3(self):
        block_poz = self.__coord.get_poz_block_mills()
        free_poz = self.get_free_position()
        comp_poz = self.get_computer_position()
        for poz in free_poz:
            set_semi_mils = block_poz[poz]
            for semi_mils in set_semi_mils:
                poz_1 = semi_mils[0]
                poz_2 = semi_mils[1]
                list_coord = self.__coord.get_matrix_coordinates(poz_1)
                symbol_1 = self.__board.get_symbol_at_postion(list_coord[0], list_coord[1])
                list_coord = self.__coord.get_matrix_coordinates(poz_2)
                symbol_2 = self.__board.get_symbol_at_postion(list_coord[0], list_coord[1])
                if symbol_1 == 1 and symbol_2 == 1:
                    for comp in comp_poz:
                        if comp != poz_1 and comp != poz_2:
                            return comp, poz
        return ["00", "00"]

    def try_make_moris_in_stage_3(self):
        block_poz = self.__coord.get_poz_block_mills()
        free_poz = self.get_free_position()
        comp_poz = self.get_computer_position()
        for poz in free_poz:
            set_semi_mils = block_poz[poz]
            for semi_mils in set_semi_mils:
                poz_1 = semi_mils[0]
                poz_2 = semi_mils[1]
                list_coord = self.__coord.get_matrix_coordinates(poz_1)
                symbol_1 = self.__board.get_symbol_at_postion(list_coord[0], list_coord[1])
                list_coord = self.__coord.get_matrix_coordinates(poz_2)
                symbol_2 = self.__board.get_symbol_at_postion(list_coord[0], list_coord[1])
                if symbol_1 == 2 and symbol_2 == 2:
                    for comp in comp_poz:
                        if comp != poz_1 and comp != poz_2:
                            return comp, poz
        return ["00", "00"]

    def make_computer_take_piece(self):
        user_position = self.get_user_position()
        for position in user_position:
            if not self.is_in_mill_of_player(position) or not self.player_has_free_position():
                self.update_position(position, 0)
                self.__user_nr_left -= 1
                if self.__user_nr_left <= 3 and self.__user_nr_placed == 9:
                    self.__user_stage = 3
                print(self.__user_nr_placed, " ", self.__user_nr_left)
                self.__nr_move = 0
                return position


    def computer_is_blocked(self) -> bool:
        if self.get_computer_stage() != 2:
            return False
        free_poz = self.get_free_position()
        computer_poz = self.get_computer_position()
        for poz_start in computer_poz:
            for poz_final in free_poz:
                if self.__coord.is_adiacent_position(poz_start, poz_final) and poz_final != poz_start:
                    return False
        return True

    def user_is_blocked(self) -> bool:
        if self.get_user_stage() != 2:
            return False
        free_poz = self.get_free_position()
        user_poz = self.get_user_position()
        for poz_start in user_poz:
            for poz_final in free_poz:
                if self.__coord.is_adiacent_position(poz_start, poz_final) and poz_final != poz_start:
                    return False
        return True

    def is_in_mill_of_computer(self, position):
        mills = self.__coord.get_all_possible_poz_in_mills()
        triples = mills[position]
        for triple in triples:
            list_coord = self.__coord.get_matrix_coordinates(triple[0])
            v0 = self.__board.get_symbol_at_postion(list_coord[0], list_coord[1])

            list_coord = self.__coord.get_matrix_coordinates(triple[1])
            v1 = self.__board.get_symbol_at_postion(list_coord[0], list_coord[1])

            list_coord = self.__coord.get_matrix_coordinates(triple[2])
            v2 = self.__board.get_symbol_at_postion(list_coord[0], list_coord[1])
            if v0 * v1 * v2 == 8:
                return True
        return False

    def get_board_status(self):
        if self.__computer_nr_left < 3 and self.__computer_nr_placed == 9:
            return 1
        elif self.computer_is_blocked():
            return 1
        elif self.__user_nr_left < 3 and self.__user_nr_placed == 9:
            return 2
        elif self.user_is_blocked():
            return 2
        elif self.__nr_move == 10:
            return 0
        else:
            return 4

    def show_board(self):
        self.__board.draw_board()


"""
test_board = Board()
test_coord = Coordinates()
test_game = Game(test_board, test_coord)
test_game.make_user_move_1("02")
test_game.make_user_move_1("09")
test_game.make_user_move_1("03")
test_game.make_user_move_1("05")
test_game.make_user_move_1("08")

test_game.make_computer_move()
test_game.make_computer_move()
test_game.make_computer_move()
test_game.make_computer_move()
print(test_game.made_player_mills())
print(test_game.is_in_mill_of_player("09"))
test_game.show_board()
"""
