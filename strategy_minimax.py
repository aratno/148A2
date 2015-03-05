from strategy import Strategy

from tippy_game_state import TippyGameState
from tippy_move import TippyMove

from subtract_square_state import SubtractSquareState
from subtract_square_move import SubtractSquareMove
class StrategyMinimax(Strategy):
    """
    """
    def suggest_move(self,state):
        """
        """
        temp = state.possible_next_moves()[0]
        win = state.WIN
        for i in state.possible_next_moves():
            if self.minimax(state.apply_move(i)) == state.LOSE:
                temp = i
                win = state.WIN
                break
        if win == state.LOSE:
            for k in state.possible_next_moves():
                if self.minimax(state.apply_move(k)) == state.DRAW:
                    temp = k
                    break
        return temp
        
    def minimax(self,state):
        """
        """
        
        if state.winner('p1'):
            return state.WIN
        elif state.winner('p2'):
            return state.LOSE
        elif not state.possible_next_moves():
            return state.DRAW
        elif state.next_player == 'p1':
            return max([self.minimax(state.apply_move(i)) for i in state.possible_next_moves()])
        elif state.next_player == 'p2':
            return min([self.minimax(state.apply_move(i)) for i in state.possible_next_moves()])
        else: 
            return 0
    
