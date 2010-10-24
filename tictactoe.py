class TicTacToe(object):
    """
    Initializes a 3x3 matrix for game play
    """
    def __init__(self):
        self.__game_board = [
            [' ',' ', ' '],
            [' ',' ', ' '],
            [' ',' ', ' ']
            ]

    """
    Displays the current playing area
    in: the game board to display                                                                                                                                      
    returns: None                                                                                                                                                      
    output: Displays the current state of the game board to the console
    """
    def display_game_area(self):
        for index, row in enumerate(self.__game_board):
            print "%s|%s|%s" % (row[0],row[1],row[2])
            if index != 2:
                print "-" * 6


if __name__ == "__main__":
    game = TicTacToe()
    game.display_game_area()
