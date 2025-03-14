from game import Game
from colorama import Fore, Style
from exception import MoveException


class UI:
    def __init__(self,  game: Game):
        self.__game = game

    def start(self):
        is_running = True
        user_turn = True
        self.__game.show_board()
        while is_running:
            try:
                if user_turn:
                    user_stage = self.__game.get_user_stage()
                    if user_stage == 1:
                        print(Fore.RED + "USER : new positon: " + Style.RESET_ALL, end="")
                        user_input = input()
                        self.__game.make_user_move_1(user_input)
                        if self.__game.is_in_mill_of_player(user_input):
                            self.__game.show_board()
                            self.__game.set_user_old_stage(self.__game.get_user_stage())
                            self.__game.set_user_stage(4)
                        else:
                            user_turn = not user_turn

                    elif user_stage == 2:
                        print(Fore.RED + "USER : move from: " + Style.RESET_ALL, end="")
                        user_input_1 = input()
                        print(Fore.RED + "USER : move to: " + Style.RESET_ALL, end="")
                        user_input_2 = input()
                        self.__game.make_user_move_2(user_input_1, user_input_2)
                        if self.__game.is_in_mill_of_player(user_input_2):
                            self.__game.show_board()
                            self.__game.set_user_old_stage(self.__game.get_user_stage())
                            self.__game.set_user_stage(4)
                        else:
                            user_turn = not user_turn
                    elif user_stage == 3:
                        print(Fore.RED + "USER : move from: " + Style.RESET_ALL, end="")
                        user_input_1 = input()
                        print(Fore.RED + "USER : move to: " + Style.RESET_ALL, end="")
                        user_input_2 = input()
                        self.__game.make_user_move_3(user_input_1, user_input_2)
                        if self.__game.is_in_mill_of_player(user_input_2):
                            self.__game.show_board()
                            self.__game.set_user_old_stage(self.__game.get_user_stage())
                            self.__game.set_user_stage(4)
                        else:
                            user_turn = not user_turn
                    elif user_stage == 4:    # user take a piece
                        print(Fore.MAGENTA + "USER : take a piece: " + Style.RESET_ALL, end="")
                        user_input = input()
                        self.__game.make_user_take_piece(user_input)
                        self.__game.set_user_stage(self.__game.get_user_old_stage())
                        user_turn = not user_turn
                        self.__game.show_board()
                else:
                    computer_stage = self.__game.get_computer_stage()
                    if computer_stage == 1:
                        last_move_computer = self.__game.make_computer_move_1()
                        print(Fore.BLUE + "COMPUTER : new positon: " + last_move_computer + Style.RESET_ALL)
                        if self.__game.is_in_mill_of_computer(last_move_computer):
                            take_computer_piece = self.__game.make_computer_take_piece()
                            print(Fore.LIGHTMAGENTA_EX + 'Computer take ' + take_computer_piece + Style.RESET_ALL)
                        print(Fore.LIGHTBLACK_EX+'The current board is:'+Style.RESET_ALL)
                        self.__game.show_board()
                        user_turn = not user_turn
                    elif computer_stage == 2:
                        poz_start, poz_final = self.__game.make_computer_move_2()
                        print(Fore.BLUE + "COMPUTER : move from: " + poz_start + " to " + poz_final + Style.RESET_ALL)
                        if self.__game.is_in_mill_of_computer(poz_final):
                            take_computer_piece = self.__game.make_computer_take_piece()
                            print(Fore.LIGHTMAGENTA_EX + 'Computer take ' + take_computer_piece + Style.RESET_ALL)
                        print(Fore.LIGHTBLACK_EX + 'The current board is:' + Style.RESET_ALL)
                        self.__game.show_board()
                        user_turn = not user_turn
                    elif computer_stage == 3:
                        poz_start, poz_final = self.__game.make_computer_move_3()
                        print(Fore.BLUE + "COMPUTER : move from: " + poz_start + " to " + poz_final + Style.RESET_ALL)
                        if self.__game.is_in_mill_of_computer(poz_final):
                            take_computer_piece = self.__game.make_computer_take_piece()
                            print(Fore.LIGHTMAGENTA_EX + 'Computer take ' + take_computer_piece + Style.RESET_ALL)
                        print(Fore.LIGHTBLACK_EX + 'The current board is:' + Style.RESET_ALL)
                        self.__game.show_board()
                        user_turn = not user_turn
            except MoveException as msg:
                print(msg)
            else:
                board_status = self.__game.get_board_status()
                if board_status == 1:
                    print(Fore.YELLOW + 'Game was won by human player.' + Style.RESET_ALL)
                    return
                elif board_status == 2:
                    print(Fore.YELLOW + 'Game was won by computer player.' + Style.RESET_ALL)
                    return
                elif board_status == 0:
                    print(Fore.YELLOW + 'Game results in a draw.' + Style.RESET_ALL)
                    return
