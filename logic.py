#!/usr/bin/env python

import itertools

def move_player(player_attr):
    def set_any(self, value):
        try:
            del self.board[[k for k, v in self.board.iteritems() if v == value][0]]
            setattr(self, player_attr, getattr(self, player_attr)+[value])
        except ValueError: raise ValueError, "That position is not available on the board."
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

        self.board,self._player1, self._player2 = dict(zip(range(1,10),
                                                             [8, 1, 6,
                                                              3, 5, 7,
                                                              4, 9, 2])), [], []

    def get_win(self, combo, available):
        return [move for move in available if sum(combo, move) ==15 ]

    def _best_move(self, combo, available):
        return self.get_win(combo, available) + [combo]

    def best_move(self, taken_moves):
        if len(taken_moves) > 1:
            for taken_combo in itertools.combinations(taken_moves, 2):
                move = self._best_move(taken_combo, self.board.values())[0]
        if not 'move' in locals():
            for available_combo in itertools.combinations(self.board.values(), 2):
                test = self._best_move(available_combo, taken_moves)
                if len(test) > 1: return test[1]
        return move

if __name__ == '__main__':
    game = magic_square()

    game.player1 = 5
    game.player2 = 8
    print 'board 1: ', game.board
    print 'player 1: ', game.player1
    print 'player 2: ', game.player2
    print game.best_move(game.player1)
    print game.best_move(game.player2)


"""
def every_combo(list):
    out = []
    for i in list[0:-1]:
        for e in list[1:]:
            out.append((list[0], e))
        list = list[1:]
    return out
print every_combo([1,2,3,4,5,6,7,8,9])
print [c for c in itertools.combinations([1,2,3,4,5,6,7,8,9], 2)]
"""
