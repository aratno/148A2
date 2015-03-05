from strategy import Strategy

class StrategyMinimax(Strategy):
    """
    Interface to suggest random moves
    """
    def suggest_move(self,state):
        """
        (StrategyMinimax, GameState) -> Move

        Return a move implemeting minimax from those available for state.

        Overrides Strategy.suggest_move
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
        (StrategyMinimax, GameState) -> float
        
        Returns a float depending on if their exists a winning strategy for 
        player:
        If player has winning strategy, then return 1.0 otherwise
        if player can draw return 0.0
        else return -1.0
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
    
