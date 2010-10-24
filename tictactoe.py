import sys
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
        self.__X = 'X'
        self.__O = 'O'
        self.__corners = [(0,0), (0,2), (2,0), (2,2)]
        self.__sides = [(0,1),(1,2),(2,1), (1,0)]

    def display_instructions(self):
        print 'Welcome to tic-tac-toe'
        print 'In order to make your mark you must input x,y coordinate'
        print 'values when prompted. Valid values are in the range 0-2.'
        print 'The computer always gets the first move. Good luck!!'

    """
    Displays the current playing area
    in: the game board to display                                                                                                                                      
    returns: None                                                                                                                                                      
    output: Displays the current state of the game board to the console
    """
    def display_game_area(self):
        for index, row in enumerate(self.__game_board):
            print "%s | %s | %s" % (row[0],row[1],row[2])
            if index != 2:
                print "-" * 10

    def get_user_move(self):
        input_isvalid = False
        mark = 'X'
        if self.is_users_play:
            mark = 'O'
            self.is_users_play = False
        else:
            result = self.__get_computer_move()
            self.is_users_play = True
            self.__game_board[result[0]][result[1]] = self.__X
            return
        
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
    Determines the next move to be made by the computer
    Algorithm was adapted from the strategy at http://en.wikipedia.org/wiki/Tic_tac_toe
    This use a brute force approach. We could optimize by using the minimax algorithm
    in: None
    output: None
    returns: tuple of coordinates for the next move
    """
    def __get_computer_move(self):
        #1 if we have 2 in a row anywhere play for the win
        result = self.__row_has_two(self.__X)
        if result is not None:
            return result
        #2 attempt to block player
        result = self.__row_has_two(self.__O)
        if result is not None:
            return result

        #3 move in the center
        if self.__game_board[1][1] == ' ':
            return (1,1)


        #4 play a corner
        result = self.__get_empty_corner()
        if result is not None:
            return result
        #5 play in center of row or column
        result = self.__get_empty_side()
        if result is not None:
            return result

    
    def __row_has_two(self, mark):
        #look for 2 in row
        for index, row in enumerate(self.__game_board):
            if row.count(mark) == 2 and ' ' in row:
                return (index, row.index(' '))

        #look for 2 in columns
        rotated_board = zip(*self.__game_board)
        for index, row in enumerate(rotated_board):
            if row.count(mark) == 2 and ' ' in row:
                return (row.index(' '), index)

        #check diagonals
        diagonals = []
        diagonals.append([self.__game_board[0][0], self.__game_board[1][1], self.__game_board[2][2]])
        diagonals.append([self.__game_board[0][2], self.__game_board[1][1], self.__game_board[2][0]])

        if diagonals[0].count(mark) == 2 and ' ' in diagonals[0]:
            index = diagonals[0].index(' ')
            return (index, index)
        elif diagonals[1].count(mark) == 2 and ' ' in diagonals[1]:
            index = diagonals[1].index(' ')
            if index == 0:
                return (index, 2)
            elif index == 1:
                return (1,1)
            else:
                return (index, 0)

        return None

    
    """
    Gets the first empty corner coordinates
    in: None
    output: None
    returns: coordinate tuple of empty corner or None if all corners are occupied
    """
    def __get_empty_corner(self):
        for corner in self.__corners:
            if self.__is_empty_area(corner):
                return corner
            
        return None

    """
    Gets the first empty side coordinates
    in: None
    output: None
    returns: coordinate tuple of empty side or None if all sides are occupied
    """
    def __get_empty_side(self):
        for side in self.__sides:
            if self.__is_empty_area(side):
                return side
            
        return None
    
    """
    Determines if the given coordinates maps to an empty slot
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
    game.display_instructions()
    game_over = False
    result = ()
    try:
        while not(game_over):
            game.get_user_move()
            result = game.is_game_over()
            game_over = result[0]
            game.display_game_area()
            print ' '
    except(KeyboardInterrupt, SystemExit):
        print "\nThanks for playing"
        sys.exit(0)
        
    if result[1] in 'XO':
        print "%s wins!" % result[1]
    else:
        print "Tie Game!"
