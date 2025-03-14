from coordinates import Coordinates
from board import Board
from game import Game
from ui import UI


new_board = Board()
new_coord = Coordinates()
new_game = Game(new_board, new_coord)

ui = UI(new_game)
ui.start()
