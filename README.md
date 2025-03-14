# Board Game

This project is a Python implementation of a board game. The game board is represented as a 2D list, and various symbols can be placed on the board.

## Features

- Initialize and draw the game board
- Set and get symbols at specific positions on the board

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/board-game.git
    ```
2. Navigate to the project directory:
    ```sh
    cd board-game
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Create an instance of the `Board` class:
    ```python
    from board import Board

    test_board = Board()
    ```

2. Set symbols at specific positions:
    ```python
    test_board.set_symbol_at_postion(1, 1, 2)
    test_board.set_symbol_at_postion(1, 13, 1)
    ```

3. Draw the board:
    ```python
    test_board.draw_board()
    ```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License.