class TicTacToe(object):
    """
    Initializes a 3x3 matrix for game play
    """
    def __init__(self):
        self.__game_board = [
            [' ',' ',' '],
            [' ',' ',' '],
            [' ',' ',' ']
            ]
        
        self.is_users_play = False

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

    def get_user_move(self):
        input_isvalid = False
        mark = 'X'
        if self.is_users_play:
            mark = 'O'
            self.is_users_play = False
        else:
            #get computer move
            self.is_users_play = True
            mark = 'X'

        while not(input_isvalid):
            print "Enter input in the format x,y"
            input = raw_input("--> ")
            coordinates = input.split(",")
            if len(coordinates) == 2 and coordinates[0].isdigit() and coordinates[1].isdigit():
                if self.__is_empty_area(coordinates):
                    input_isvalid = True
                    self.__game_board[int(coordinates[0])][int(coordinates[1])] = mark

            if not(input_isvalid):
                print "Invalid coordinates!"

    
    """
    Determines if the give coordinates maps to an empty slot
    in: list of coordinates ['x','y'] where x and y are both integer strings
    output: None
    returns: True if the coordinates are empty
    """
    def __is_empty_area(self, coordinates):
        x = int(coordinates[0])
        y = int(coordinates[1])
        valid_values = (0,1,2)

        if x in valid_values and y in valid_values and self.__game_board[x][y] == ' ':
            return True
        else:
            return False

    """
    Determines if game is complete by checking for a win or tie game
    A tie game is one in which no more moves remain and there is no winner
    in: None
    output: None
    returns: tuple defined as follows
             (True, player) game is over and player 'X' or 'O' wins or ' '  for tie
             (False,None) game has more moves
    """
    def is_game_over(self):
        total_empty = 0
        #check rows
        for row in self.__game_board:
            if row.count('O') == 3 or row.count('X') == 3:
                return (True, row[0])
            else:
                total_empty =  total_empty = total_empty + row.count(' ')

        #check diagonals
        if self.__game_board[0][0] != ' ' or self.__game_board[0][2] != ' ':
            if (self.__game_board[0][0] == self.__game_board[1][1] and self.__game_board[0][0] == self.__game_board[2][2]) or \
               (self.__game_board[2][0] == self.__game_board[1][1] and self.__game_board[2][0] == self.__game_board[0][2]):
               return (True, self.__game_board[1][1])

        #check columns (this is checked last since it requires a little more overhead)
        rotated_board = zip(*self.__game_board)
        for row in rotated_board:
            if row.count('O') == 3 or row.count('X') == 3:
                return (True, row[0])
            else:
                total_empty =  total_empty = total_empty + row.count(' ')

        if total_empty == 0:
            return (True, ' ')
        return (False, None)
        
if __name__ == "__main__":
    game = TicTacToe()    
    game_over = False
    result = ()
    while not(game_over):
        game.get_user_move()
        result = game.is_game_over()
        game_over = result[0]
        game.display_game_area()
        
    if result[1] in 'XO':
        print "%s wins!" % result[1]
    else:
        print "tie"
