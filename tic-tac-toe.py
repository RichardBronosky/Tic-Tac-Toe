#!/usr/bin/env python
######################################################################################################################
#  Program:  An interactive Tic-Tac-Toe game 
#  Author: Ajay Varghes
#  Date: Sep 10, 2010 2.30 AM
########################################################################################################################3
    
import random
winArr = [('A1','A2','A3'), ('B1','B2','B3'), ('C1','C2','C3'), ('A1','B1','C1'), ('A2','B2','C2'), ('A3','B3','C3'),('A1','B2','C3'),('A3','B2','C1')]
class TicTac:
    def __init__(self):
        self.pos = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
        element = {}
        for pos in self.pos:
            element[pos]=' '
        self.element = element
        self.comp = ''
        self.hum = ''
        self.winner = ''
   
    def displayBoard(self):
        print "    1  2  3"
        print "A   " + self.element['A1'] + '| ' + self.element['A2'] + '| ' + self.element['A3']
        print "   --+--+--"
        print "B   " + self.element['B1'] + '| ' + self.element['B2'] + '| ' + self.element['B3']
        print "   --+--+--"
        print "C   " + self.element['C1'] + '| ' + self.element['C2'] + '| ' + self.element['C3']
    
    def validMoves(self):
        """Return valid position"""
        vp = []
        for k,v in self.element.items():
            if v == ' ': vp.append(k)
        return vp
 
    def addMove(self, move, player):
        """Adds the move for the player"""
        self.element[move] = player

    def delMove(self, move):
        """Undo the move"""
        self.element[move] = " "

    def checkOver(self):
        '''Check for winner or tie'''
        e = self.element
        for p in winArr:
            if (e[p[0]]!=' ' and e[p[0]] == e[p[1]] and e[p[1]] == e[p[2]]):
                self.winner = e[p[0]]
                return True
        for i in e :
            if e[i] == ' ': return False 
        self.winner = "T" 
        return True 

    def getWinner(self):
       '''Return winner'''
       if self.winner == self.comp:
           return "Computer"
       elif self.winner == self.hum:
           return "Human" 
       return False

def compMove(t):
    '''Does the computer move based on human move.'''
    k = t.comp
    e = t.element
    ctr = 0
    vp = t.validMoves()
    #Check for player has two in a row, mark the third 
    for p in vp:
        for w in winArr:
            if p not in w: 
                continue
            ctr = 0; nf = -1
            for i in w: 
                if e[i] == k: ctr+=1
                elif e[i] == ' ': nf = i 
            if ctr >= 2 and nf != -1:
                t. addMove(nf, k)
                return
    #check for a opponent winning move (two in a row and a clear third)
    k = t.hum
    for p in vp:
        for w in winArr:
            if p not in w: 
                continue
            ctr = 0; nf = -1
            for i in w: 
                if e[i] == k: ctr+=1
                elif e[i] == ' ': nf = i 
            if ctr >= 2 and nf != -1:
                t. addMove(nf, t.comp)
                return
    #Play the center
    if e['B2'] == ' ':
        t.addMove('B2', t.comp)
        return
    #Play side center if opponent are either corner
    for w in winArr:
       if w[1] in vp and w[0] == w[2] and w[0] != ' ':
           t.addMove(w[1], t.comp)
           return
    #Play in the corner square
    for w in winArr:
        if w[0] in vp: 
            t.addMove(w[0], t.comp)
            return
        if w[2] in vp:
            t.addMover(w[2], t.comp)
            return
    #Play in the center square
    for w in winArr:
        if w[1] in vp:
            t.addMove(w[1], t.comp)
            return
    t.addMove(random(vp), t.comp)
    return
 
def humanMove(t):
    '''Does the human move'''
    t.displayBoard()
    vp = t.validMoves()
    move = raw_input("Enter your move(A1,B2... where alpha for column and num for row  position):")
    while move not in vp:
        print "Sorry, '%s' is not a valid move. Please try again." % move
        move = raw_input("Enter your move(A1,B2... where alpha for column and num for row  position):")
    t.addMove(move, t.hum)

if __name__ == "__main__":
     t = TicTac()
     hp =' '
     while ((len(hp)!= 1) or (hp[0] != "X" and hp[0] != "O")):
         hp = raw_input("Choose your side, X or O:")
     t.hum = hp
     if hp == 'X':
         t.comp = 'O'
     else:
         t.comp = 'X'
     ctr = 1
     while True:
         print "%d. turn" %ctr
         humanMove(t)
         if t.checkOver(): 
             break
         compMove(t)
         if t.checkOver(): 
             break
         ctr += 1
 
     t.displayBoard()
     ret = t.getWinner()
     if ret:
         print 'Player %s wins' % ret
     else:
         print 'Game over'
