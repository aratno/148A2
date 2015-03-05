from game_state import GameState
from tippy_move import TippyMove
from math import sqrt
from random import randint
from copy import deepcopy

class TippyGameState(GameState):
    '''
    '''
    
    PLAYER = {'p1': 'X', 'p2': 'O'}
    
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
        self.instructions = 'Enter the row number and then the column \
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
        
        new_state = deepcopy(self.current_state)
        
        if move in self.possible_next_moves():
            if self.next_player == 'p1':
                new_state[move.pos[0]][move.pos[1]] = 'X'                
            else:
                new_state[move.pos[0]][move.pos[1]] = 'O'
        else:
            raise Exception('Not a valid move.')
        
        new = TippyGameState(self.opponent(), False, new_state)
        
        new.over =  new.winner('p1') or new.winner('p2') or not \
            new.possible_next_moves()
        
        return new
            
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
                        moves.append(TippyMove([i + 1, j + 1]))
        
        return moves
    
    def winner(self, player):
        '''
        '''
        
        win = False
        
        i = 0        
        while not win and i < len(self.current_state):
            j = 0
            while not win and j < len(self.current_state):
                win = find_tippy(self.current_state, \
                                 TippyGameState.PLAYER[player], \
                                 [i, j])
                j += 1
            i += 1
                
        return win
    
    
    def rough_outcome(self):
        '''
        
        If game is over, returns 0.0
        '''
        
        new_states = [self.apply_move(i) for i in self.possible_next_moves()]
        outcome = [i.winner(self.next_player) for i in new_states]
        
        opp = TippyGameState(self.opponent(), False, self.current_state)
        new_opp = [opp.apply_move(i) for i in opp.possible_next_moves()]
        opp_outcome = [i.winner(opp.next_player) for i in new_opp]
        
        wins = float(len([i for i in outcome if i]))
        losses = float(len([i for i in opp_outcome if i]))
        
        try:
            num = 2*wins/(wins + losses) - 1
        except ZeroDivisionError:
            num = 0
        
        return 'Wins: {}, Losses: {}, Number: {}'.format(wins, losses, num)
        

def find_tippy(state, sym, pos):
    '''
    '''
    
    x, y = pos[0], pos[1]
    
    tippy = False
    
    if state[x][y] == sym:
        try:
            if all([state[x][y + 1] == sym, \
                    state[x + 1][y + 1] == sym, \
                    state[x + 1][y + 2] == sym]):
                tippy = True
        except IndexError:
            pass
        
        try:            
            if all([state[x][y + 1] == sym, \
                     state[x + 1][y] == sym, \
                     state[x + 1][y - 1] == sym]):
                tippy = True
        except IndexError:
            pass
        
        try:
            if all([state[x + 1][y] == sym, \
                     state[x + 1][y + 1] == sym, \
                     state[x + 2][y + 1] == sym]):
                tippy = True
        except IndexError:
            pass
        
        try:        
            if all([state[x + 1][y] == sym, \
                     state[x + 1][y - 1] == sym, \
                     state[x + 2][y - 1] == sym]):
                tippy = True
        except IndexError:
            pass
    
    return tippy