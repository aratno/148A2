from game_state import GameState
from tippy_move import TippyMove
from math import sqrt
from random import randint

class TippyGameState(GameState):
    '''
    '''
    
    LET = {'X': 'p1', 'O': 'p2'}
    PLA = {'p1': 'X', 'p2': 'O'}
    
    def __init__(self, p, interactive=False, \
                 current_state=[[' ' for x in range(4)] for x in range(4)]):
        '''
        '''
        
        if interactive:
            size = int(input('Enter the size of your grid: '))
            if isinstance(size, int) and size >= 3:
                current_state = [[' ' for x in range(size)] \
                                 for x in range(size)]
            else:
                raise Exception('Invalid grid size.')
            
        GameState.__init__(self, p)
        self.current_state = current_state
        self.instructions = 'Enter the column number and then the row \
        number of the location where you wish to make your move. The \
        objective is to make a tippy.'
        
    def __repr__(self):
        '''
        '''
        
        return 'TippyGameState({}, {})'.format(repr(self.next_player), \
                                               repr(self.current_state))
    
    def __str__(self):
        '''
        '''
        
        grid = ''
        for i in range(len(self.current_state)):
            for j in range(len(self.current_state)):
                grid += self.current_state[i][j]
                if j != len(self.current_state) - 1:
                    grid += '|'
            
            grid += '\n'
            if i != len(self.current_state) - 1:
                for k in range(2*len(self.current_state) - 1):
                    grid += '-'
                grid += '\n'
                
        return grid
    
    def __eq__(self, other):
        '''
        '''
        
        return (isinstance(other, TippyGameState) and
                self.current_state == other.current_state and
                self.next_player == other.next_player)
    
    def apply_move(self, move):
        '''
        '''
        
        if move.pos in self.possible_next_moves():
            if self.next_player == 'p1':
                self.current_state[move.pos[0]][move.pos[1]] = 'X'
            else:
                self.current_state[move.pos[0]][move.pos[1]] = 'O'
            self.next_player = self.opponent()
        else:
            raise Exception('Not a valid move.')
            
    def get_move(self):
        '''
        '''
        
        move = []
        #first row taken as 1, then corrected in TippyMove
        move.append(int(input('Enter the row: ')))
        move.append(int(input('Enter the column: ')))
        
        return TippyMove(move)
    
    def possible_next_moves(self):
        '''
        '''
        
        moves = []
        if not (self.winner('p1') or self.winner('p2')):
            for i in range(len(self.current_state)):
                for j in range(len(self.current_state)):
                    if self.current_state[i][j] == ' ':
                        moves.append([i, j])
        
        return moves
    
    '''def winner(self, player):
        
        return self.check_state() and self.opponent() == player'''
    
    def winner(self, player):
        '''
        '''
        
        win = False
        i = 0
        
        while not win and i < len(self.current_state) - 2:
            j = 0
            while not win and j < len(self.current_state) - 1:
                if not self.current_state[i][j] == ' ':
                    place = self.current_state[i][j]
                    if j < len(self.current_state) - 2:
                        if self.current_state[i][j+1] == place and \
                           self.current_state[i+1][j+1] == place and \
                           self.current_state[i+1][j+2] == place:
                            win = True
                        if self.current_state[i][j+1] == place and \
                           self.current_state[i+1][j] == place and \
                           self.current_state[i+1][j-1] == place:
                            win = True
                    if i < len(self.current_state) - 2:
                        if self.current_state[i+1][j] == place and \
                           self.current_state[i+1][j+1] == place and \
                           self.current_state[i+2][j+1] == place:
                            win = True
                        if self.current_state[i+1][j] == place and j > 0:
                            if self.current_state[i+1][j-1] == place and \
                               self.current_state[i+2][j-1] == place:
                                win = True
                j += 1
            i += 1
            
        return win and player == TippyGameState.LET[place]
                           
            
                
    
    def rough_outcome(self):
        '''
        '''
        
        L_player = False
        count = 0
        
        
        place = TippyGameState.PLA[self.next_player]

        #check for psuedo-L-configuration for current player 
        i = 0
        while not L_player and i < len(self.current_state) - 1:
            #avoid edges
            j = 0
            while not L_player and j < len(self.current_state) - 1:
                #avoid edges
                if self.current_state[i][j] == place:
                    if self.current_state[i][j+1] == place and \
                       j < len(self.current_state) - 2:
                        #checking left
                        if self.current_state[i+1][j+1] == ' ' and \
                           self.current_state[i+1][j+2] == place:
                            #checking left down
                            L_player = True
                        elif i > 0: #skipping first row
                            if self.current_state[i-1][j+1] == ' ' and \
                               self.current_state[i-1][j+2] == place:
                                #checking left up
                                L_player = True
                    if self.current_state[j+1][j] == place and \
                         i < len(self.current_state) - 2:
                        #checking down
                        if self.current_state[i+1][j+1] == ' ' and \
                           self.current_state[i+2][j+1] == place:
                            #checking down right
                            L_player = True
                        elif j > 0 : #skipping first column
                            if self.current_state[i+1][j-1] == ' ' and \
                               self.current_state[i+2][j-1] == place:
                                #checking down left
                                L_player = True
                else:
                    j += 1 #iterate along columns
            i += 1 #iterate along rows
            
        #check for L-configuration for current player
        i = 0
        while not L_player and i < len(self.current_state) - 1:
            #avoid edges
            j = 0
            while not L_player and j < len(self.current_state) - 1:
                #avoid edges
                if self.current_state[i][j] == place:
                    if self.current_state[i][j+1] == place and \
                       j < len(self.current_state) - 2:
                        #checking right
                        if self.current_state[i+1][j+1] == place and \
                           self.current_state[i+1][j+2] == ' ':
                            #checking down right right
                            L_player = True
                    if self.current_state[i+1][j] == place and \
                         i < len(self.current_state) - 2:
                        #checking down
                        if self.current_state[i+1][j+1] == place and \
                           self.current_state[i+2][j+1] == ' ':
                            #checking down right
                            L_player = True
                        elif j > 0: #skipping first column
                            if self.current_state[i+1][j-1] == place and \
                               self.current_state[i+2][j-1] == ' ':
                                #checking down left
                                L_player = True
                    if self.current_state[i][j+1] == place and \
                       self.current_state[i+1][j] == place:
                        #checking down and right at the same time
                        if j > 0: #skipping first column
                            if self.current_state[i+1][j-1] == ' ':
                                #checking down left
                                L_player = True
                        if i > 0: #skipping first row
                            if self.current_state[i-1][j+1] == ' ':
                                #checking right u[
                                L_player = True
                    if j > 0:
                        if self.current_state[i+1][j-1] == place and \
                           self.current_state[i+1][j] == place and \
                           self.current_state[i][j+1] == ' ':
                            #checking down and down left, then right
                            L_player = True
                else:
                    j += 1 #iterate along columns
            i += 1 #iterate along rows
                            
        
        place = TippyGameState.PLA[self.opponent()]
        
        #check for psuedo-L-configuration for opponent 
        i = 0
        while i < len(self.current_state) - 1:
            #avoid edges
            j = 0
            while j < len(self.current_state) - 1:
                #avoid edges
                if self.current_state[i][j] == place:
                    if self.current_state[i][j+1] == place and \
                       j < len(self.current_state) - 2:
                        #checking left
                        if self.current_state[i+1][j+1] == ' ' and \
                           self.current_state[i+1][j+2] == place:
                            #checking left down
                            count += 1
                        if i > 0: #skipping first row
                            if self.current_state[i-1][j+1] == ' ' and \
                               self.current_state[i-1][j+2] == place:
                                #checking left up
                                count += 1
                    
                    if self.current_state[j+1][j] == place and \
                         i < len(self.current_state) - 2:
                        #checking down
                        if self.current_state[i+1][j+1] == ' ' and \
                           self.current_state[i+2][j+1] == place:
                            #checking down right
                            count += 1
                        if j > 0 : #skipping first column
                            if self.current_state[i+1][j-1] == ' ' and \
                               self.current_state[i+2][j-1] == place:
                                #checking down left
                                count += 1
                else:
                    j += 1 #iterate along columns
            i += 1 #iterate along rows
            
        #check for L-configuration for opponent
        i = 0
        while i < len(self.current_state) - 1:
            #avoid edges
            j = 0
            while j < len(self.current_state) - 1:
                #avoid edges
                if self.current_state[i][j] == place:
                    if self.current_state[i][j+1] == place and \
                       j < len(self.current_state) - 2:
                        #checking right
                        if self.current_state[i+1][j+1] == place and \
                           self.current_state[i+1][j+2] == ' ':
                            #checking down right right
                            count += 1
                        
                    if self.current_state[i+1][j] == place and \
                         i < len(self.current_state) - 2:
                        #checking down
                        if self.current_state[i+1][j+1] == place and \
                           self.current_state[i+2][j+1] == ' ':
                            #checking down right
                            count += 1
                        if j > 0: #skipping first column
                            if self.current_state[i+1][j-1] == place and \
                               self.current_state[i+2][j-1] == ' ':
                                #checking down left
                                count += 1
                    
                    if self.current_state[i][j+1] == place and \
                       self.current_state[i+1][j] == place:
                        #checking down and right at the same time
                        if j > 0: #skipping first column
                            if self.current_state[i+1][j-1] == ' ':
                                #checking down left
                                count += 1
                        if i > 0: #skipping first row
                            if self.current_state[i-1][j+1] == ' ':
                                #checking right up
                                count += 1
                    
                    if j > 0:
                        if self.current_state[i+1][j-1] == place and \
                           self.current_state[i+1][j] == place and \
                           self.current_state[i][j+1] == ' ':
                            #checking down and down left, then right
                            count += 1
                else:
                    j += 1 #iterate along columns
            i += 1 #iterate along rows        
        
        if L_player:
            return TippyGameState.WIN
        elif count >= 2:
            return TippyGameState.LOSE
        else:
            return TippyGameState.DRAW