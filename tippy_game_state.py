from game_state import GameState
from tippy_move import TippyMove
from math import sqrt
from random import randint
from copy import deepcopy

class TippyGameState(GameState):
    ''' The state of the Tippy game
    
    current_state is nxn array of current board
    '''
    
    PLAYER = {'p1': 'X', 'p2': 'O'}
    
    def __init__(self, p, interactive=False, \
                 current_state=[[' ' for x in range(4)] for x in range(4)]):
        '''
        (TippyGameState, str, list) --> Nonetype
        
        Initializes TippyGameState with current_state as the n by n grid
        
        Assume p is in {'p1','p2'}
               that len(current_state) > 3 so the game can be won
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
        (TippyGameState) --> str
        
        Returns the sring representation of TippyGameState that evaluates to 
        to an equivalent SubtractSquareState
        
        >>> t = TippyGameState('p1')
        >>> t
        TippyGameState('p1', [[' ', ' ', ' ', ' '], [' ', ' ', ' ', ' '], \
        [' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ']])
        '''
        
        return 'TippyGameState({}, {})'.format(repr(self.next_player), \
                                               repr(self.current_state))
    
    def __str__(self):
        '''
        (TippyGameState) --> str
        
        Returns a grid resembling what the tippy game should look like
        
        >>>t = TippyGameState('p1')
        >>>print(t)
         | | | 
        -------
         | | | 
        -------
         | | | 
        -------
         | | | 
        '''
        
        grid = ''
        for i in range(len(self.current_state)):#prints row with vertical bars
            for j in range(len(self.current_state)):
                grid += self.current_state[i][j]
                if j != len(self.current_state) - 1:
                    grid += '|'
            
            grid += '\n'
            if i != len(self.current_state) - 1: #prints line inbetween rows
                for k in range(2*len(self.current_state) - 1):
                    grid += '-'
                grid += '\n'
                
        return grid
    
    def __eq__(self, other):
        '''
        (TippyGameState, TippyGameState) -> bool

        Return True iff this TippyGameState is the equivalent to other.

        >>> s1 = TippyGameState('p1')
        >>> s2 = TippyGameState('p1')
        >>> s1 == s2
        True
        '''
        
        return (isinstance(other, TippyGameState) and
                self.current_state == other.current_state and
                self.next_player == other.next_player)
    
    def apply_move(self, move):
        '''(TippyGameState, TippyeMove) -> TippyGameState

        Return the new TippyGameState reached by applying move to self
        
        >>> s1 = TippyGameState('p1')
        >>> s2 = s1.apply_move(TippyMove([1,1]))
        >>> print(s2)
        X| | | 
        -------
         | | | 
        -------
         | | | 
        -------
         | | | 
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
        (TippyGameState) -> TippyMove

        Prompt user and return move.
        
        >>>t = TippyGameState('p1')
        >>>t.get_move()
        Enter the row: 2
        Enter the column: 2
        TippyMove([1, 1])
        '''
        
        move = []
        #first row taken as 1, then corrected in TippyMove
        move.append(int(input('Enter the row: ')))
        move.append(int(input('Enter the column: ')))
        
        return TippyMove(move)
    
    def possible_next_moves(self):
        '''
        (TippyGameState) -> list of TippyMove

        Return a (possibly empty) list of moves that are legal
        from the present state.
        >>> s1 = TippyGameState('p1')
        >>> s2 = s1.apply_move(TippyMove([1,1]))
        >>> s2.list_possible_next_moves()
        [TippyMove([0, 0]), TippyMove([0, 1]), TippyMove([0, 2]), \
        TippyMove([0, 3]), TippyMove([1, 0]), TippyMove([1, 1]), \
        TippyMove([1, 2]), TippyMove([1, 3]), TippyMove([2, 0]), \
        TippyMove([2, 1]), TippyMove([2, 2]), TippyMove([2, 3]), \
        TippyMove([3, 0]), TippyMove([3, 1]), TippyMove([3, 2]), \
        TippyMove([3, 3])]

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
        (TippyGameState,str) --> bool
        
        Returns True if a tippy has been formed and player has won
        
        >>> s1 = TippyGameState('p1')
        >>> s2 = s1.apply_move(TippyMove([1,1]))
        >>> s2.winner('p1)
        False
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
        (TippyGamestate) --> float
        
        Returns and estimate in the interval [LOSE,WIN] that gives number of
        potential winning configs for each player. If game is over, returns 0.0
        
        s1 = TippyGameState('p1')

        s2 = s1.apply_move(TippyMove([1,1]))
        s2.rough_outcome()
        'Wins: 0.0, Losses: 0.0, Number: 0'
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
    (list,str,list) --> bool
    
    returns True if a Tippy has been formed starting at position pos
    
    >>>s1 = TippyGameState('p1')
    >>>temp = s1.current_state
    >>>temp[0][0] = 'X'
    >>>temp[0][1] = 'X'
    >>>temp[1][1] = 'X'
    >>>temp[1][2] = 'X'
    >>>find_tippy(temp,'X',[0,0])
    True
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