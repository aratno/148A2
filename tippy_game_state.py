from game_state import GameState
from tippy_move import TippyMove
from math import sqrt
from random import randint

class TippyGameState(GameState):
    '''
    '''
    
    def __init__(self, p, interactive=False, \
                 current_state = [[' ' for x in range(4)] for x in range(4)]):
        '''
        '''
        
        if interactive:
            size = input('Enter the size of your grid: ') + 1
            if isinstance(size, int) and size > 2:
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