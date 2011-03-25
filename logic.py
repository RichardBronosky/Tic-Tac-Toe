#!/usr/bin/env python

import collections, itertools, random, logging

class player(object):

    def __init__(self, game, move_picker, char='X'):
        self.moves, self.game, self.move_picker, self.char = [], game, move_picker, char

    def move(self, move):
        self.moves += [self.game.take(move)]
        if len(self.moves) >= 3 and [self.game.get_win(combo) for combo in itertools.combinations(self.moves, 3)][0]:
            self.game.winner = self

class magic_square(object):

    """
    The winning combinations of the game called tic-tac-toe add up to the magic
    constant of a http://en.wikipedia.org/wiki/Magic_Square

    The arrangement of the board is not important. All that matters is that all
    winning combinations add up to 15. Allowing the magic square values to be
    indexed by their tic-tac-toe position is just the UI most people expect.
    """

    fresh_board = [8, 1, 6,
                   3, 5, 7,
                   4, 9, 2]

    def __init__(self):
        self.winner, self.board = None, self.fresh_board[:]

    def take(self, move):
        try:
            del self.board[self.board.index(move)]
        except ValueError:
            raise ValueError, ("Position %s is not available on the board." % move)
        return move

    def get_win(self, combo, available=[0]):
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
            if len(crafty) == 2:
                moves = moves + list(set(crafty[0]) & set(crafty[1]))
            # 4th look for combos
            for available_combo in itertools.combinations(self.board, 2):
                if self.get_win(available_combo, taken_moves):
                    moves = moves + [random.choice(list(available_combo))]
        elif len(self.board):
            moves = moves + [random.choice(self.board)]
        else:
            raise IndexError, 'game over'
        return moves or list(set([5]) & set(self.board)) or [random.choice(list(set([5,8,6,4,2]) & set(self.board)) or self.board)]

if __name__ == '__main__':
    """
    Executing this library directory runs a series of unit tests. If you'd like
    to hear even more noise, uncomment one of the following lines.
    """
    #logging.getLogger().setLevel(logging.DEBUG)
    #logging.getLogger().setLevel(logging.INFO)

    def board(players):
        board = magic_square.fresh_board[:]
        for k in range(0,len(board)):
            for player in players:
                if board[k] in player.moves:
                    board[k] = player.char
        for row in ['-----------'] + ['| {0}  {1}  {2} |'.format(*board[i:i+3]) for i in range(0, len(board), 3)] + ['-----------']:
            logging.info(row)

    def random_factory(game):
        return lambda x,y: [random.choice(game.board)]

    def play(move_picker0, move_picker1):
            game = magic_square()
            winner = game.winner
            players = [player(game, eval(move_picker0), 'X'), player(game, eval(move_picker1), 'O')]
            player_queue = collections.deque(players)
            while len(game.board) and not game.winner:
                move = player_queue[0].move_picker(player_queue[0].moves, player_queue[1].moves) 
                player_queue[0].move(move[0])
                logging.debug('%s: %s' % (player_queue[0].char, player_queue[0].moves))
                player_queue.rotate()
            board(players)
            if game.winner:
                winner = game.winner.char
            logging.info('winner: %s' % winner)
            return winner

    print "\nplay('game.best_moves', 'game.best_moves')"
    test = collections.defaultdict(int)
    for match in range(1000):
        test[play('game.best_moves', 'game.best_moves')] += 1
    print dict(test)
    print "\nplay('random_factory(game)', 'random_factory(game)')"
    test = collections.defaultdict(int)
    for match in range(1000):
        test[play('random_factory(game)', 'random_factory(game)')] += 1
    print dict(test)
    print "\nplay('game.best_moves', 'random_factory(game)')"
    test = collections.defaultdict(int)
    for match in range(1000):
        test[play('game.best_moves', 'random_factory(game)')] += 1
    print dict(test)
    print "\nplay('random_factory(game)', 'game.best_moves')"
    test = collections.defaultdict(int)
    for match in range(1000):
        test[play('random_factory(game)', 'game.best_moves')] += 1
    print dict(test)
