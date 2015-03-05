from move import Move

class TippyMove(Move):
    
    '''
    '''
    
    def __init__(self, pos):
        ''' (TippyMove, list) -> NoneType
    
        Initialize a new TippyMove for removing amount from value.

        Assume: ???
        '''
        
        self.pos = [pos[0] - 1, pos[1] - 1]
        #user will enter number from 1 to n
        
    def __repr__(self):
        '''
        '''
        return 'TippyMove({})'.format(str(self.pos))
        
    def __str__(self):
        '''
        '''
        return 'Row: {}  Column: {}'.format(self.pos[0],self.pos[1]) 
    
    def __eq__(self, other):
        '''
        '''
        return (isinstance(other, TippyMove) and 
                        self.pos == other.pos)