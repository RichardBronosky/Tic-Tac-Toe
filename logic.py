#!/usr/bin/env python

import collections, itertools, random, logging

def move_player(player_attr):
    def set_any(self, value):
        try:
            del self.board[self.board.index(value)]
            moves = getattr(self, player_attr) + [value]
            setattr(self, player_attr, moves)
            if len(moves) > 2 and [player_attr for combo in itertools.combinations(moves, 3) if sum(combo) == 15]: self.winner = player_attr
        except ValueError: raise ValueError, ("Position %s is not available on the board." % value)
    return set_any

class magic_square(object):
    """
    The winning combinations of the game called tic-tac-toe add up to the magic
    constant of a http://en.wikipedia.org/wiki/Magic_Square
    """

    player1 = property(fset=move_player('_player1'), fget=lambda self: self._player1)
    player2 = property(fset=move_player('_player2'), fget=lambda self: self._player2)

    def __init__(self):
        """
        The arrangement of the board is not important. All that matters is that all
        winning combinations add up to 15. Allowing the magic square values to be
        indexed by their tic-tac-toe position is just the UI most people expect.
        """

        self.winner, self._player1, self._player2, self.board = None, [], [], [8, 1, 6,
                                                                               3, 5, 7,
                                                                               4, 9, 2]

    def get_win(self, combo, available):
        return [move for move in available if sum(combo, move) == 15]

    def best_moves(self, taken_moves, opponent_moves=[], moves=[]):
        for tactic in (taken_moves, opponent_moves):
            # 1st tactic, go for the win. 2nd tactic, block your opponent.
            if len(tactic) > 1:
                for combo in itertools.combinations(tactic, 2):
                    moves = moves + self.get_win(combo, self.board)
        if len(self.board) > 1:
            # 3rd look for opponent combo intersections that would position them to win 2 ways
            crafty = [available_combo for available_combo in itertools.combinations(self.board, 2) if self.get_win(available_combo, opponent_moves)]
            if len(crafty) == 2: moves = moves + list(set(crafty[0]) & set(crafty[1]))
            # 4th look for combos
            for available_combo in itertools.combinations(self.board, 2):
                if self.get_win(available_combo, taken_moves): moves = moves + [random.choice(list(available_combo))]
        elif len(self.board):
            moves = moves + [random.choice(self.board)]
        else: raise IndexError, 'game over'
        #return moves or [random.choice(self.board)]
        # below fails when 5,8,6,4,2 are all taken
        #return moves or [random.choice(list(set([5,8,6,4,2]) & set(self.board)))]
        return moves or list(set([5]) & set(self.board)) or [random.choice(list(set([5,8,6,4,2]) & set(self.board)))] or [random.choice(self.board)]

if __name__ == '__main__':
    def show(board):
        for k in range(0,len(board)):
            if board[k] in getattr(game, players[0]):
                board[k] = 'X'
            elif board[k] in getattr(game, players[1]):
                board[k] = 'O'
        print '-----------'
        print '| {0}  {1}  {2} |'.format(*board[0:3])
        print '| {0}  {1}  {2} |'.format(*board[3:6])
        print '| {0}  {1}  {2} |'.format(*board[6:9])
        print '-----------'

    logging.getLogger().setLevel(logging.DEBUG)
    players = ['player1', 'player2']
    player_queue = collections.deque(players)
    for match in range(30):
        game = magic_square()
        board = game.board[:]
        show(board)
        while len(game.board) and not game.winner:
            move1 = game.best_moves(getattr(game, player_queue[0]), getattr(game, player_queue[1])) 
            setattr(game, player_queue[0], move1[0])
            player_queue.rotate()
        show(board)
        print 'winner: ', game.winner
