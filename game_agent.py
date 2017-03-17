"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

# Aggressive !
def aggressive(game, player):

    player_moves = len(game.get_legal_moves(player))
    opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(player_moves) - 4 * float(opponent_moves)

# Stay close ! I want to stay as close to my opponent as possible
def stay_close(game, player):

    player_moves = len(game.get_legal_moves(player))
    opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))

    player_location = game.get_player_location(player)
    opponent_location = game.get_player_location(game.get_opponent(player))

    players_distance_x = abs(player_location[0] - opponent_location[0])
    players_distance_y = abs(player_location[1] - opponent_location[1])

    if players_distance_x <= 1 and players_distance_y <= 1:
        res = float( 2 * (player_moves - opponent_moves) / (players_distance_x + players_distance_y))
        # print("distance entre les joueurs : {}".format(players_distance_x + players_distance_y))
        # print("\tresultat PROCHE : {}".format(res))  
        return res
    else:
        res = float((player_moves - opponent_moves) / (players_distance_x + players_distance_y))
        # print("\tresultat : {}".format(res))
        return res

# has the distance from the board edges an impact on the AI ?
def distance(game, player):

    player_moves = len(game.get_legal_moves(player))
    opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))
    same_moves = len(list(set(player_moves) & set(opponent_moves)))

    player_location = game.get_player_location(player)
    opponent_location = game.get_player_location(game.get_opponent(player))

    player_distance = abs(float(player_location[0] - game.width//2)) + abs(float(player_location[1] - game.height//2))
    opponent_distance = abs(float(opponent_location[0] - game.width//2)) + abs(float(opponent_location[1] - game.height//2))

    return float((player_moves + player_distance) - 2*((opponent_moves + opponent_distance)))

# The strategy changes during the game: During the first part of the game, I'm fully aggressive then I try
# to keep the center becoming less aggressive
def adaptive(game, player):

    board_size = game.height * game.width
    moves_to_board = game.move_count / board_size
    
    if moves_to_board > 0.4:
        return aggressive(game, player)
    else:
        return aggressive_center(game, player)

# I refrain my aggressivity a little bit while trying to keep the center !
def aggressive_center(game, player):

    center_x = game.width//2
    center_y = game.height//2
    center_locations = [(x, y) for x in [center_x - 1, center_x, center_x + 1] for y in [center_y - 1, center_y, center_y + 1]]

    player_moves = len(game.get_legal_moves(player))
    opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))

    player_center_moves = len([m for m in game.get_legal_moves(player) if m in center_locations])
    opponent_center_moves = len([m for m in game.get_legal_moves(game.get_opponent(player)) if m in center_locations])
    
    return ((player_moves + player_center_moves) - (opponent_moves + opponent_center_moves))

def custom_score(game, player):
    """moves remaining as a percentage"""
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return adaptive(game, player)

class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=15.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left
         
        if not legal_moves:
            return (-1,-1)

        score_move = (float("-inf"), (-1, -1))

        try:
            if not self.iterative:
                if self.method == "minimax":
                    score_move = self.minimax(game, self.search_depth, True)
                    return score_move[1]
                elif self.method == "alphabeta":
                    score_move = self.alphabeta(game, self.search_depth, float("-inf"), float("inf"), True)
                    return score_move[1]
                else:
                    raise RuntimeError("invalid method. method={self.method}")
            else:
                depth = 0
                best_score_move = (float("-inf"), (-1, -1))
                while depth <= len(game.get_blank_spaces()):
                    if self.method == "minimax":
                        score_move = self.minimax(game, depth, True)
                        if score_move[0] > best_score_move[0]:
                            best_score_move = score_move
                        depth += 1
                    elif self.method == "alphabeta":
                        score_move = self.alphabeta(game, depth, float("-inf"), float("inf"), True)
                        if score_move[0] > best_score_move[0]:
                            best_score_move = score_move
                        depth += 1
                    else:
                        raise RuntimeError("invalid method. method={self.method}")

        except Timeout:
            pass

        return score_move[1]

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # Preparing player and (score,move)
        if maximizing_player:
            player = game.active_player
            score_move = (float("-inf"), (-1, -1))
        else:
            player = game.get_opponent(game.active_player)
            score_move = (float("inf"), (-1, -1))

        legal_moves = game.get_legal_moves(game.active_player)

        # Case 1: The game has a winner
        if game.utility(player) != 0:
            return game.utility(player), game.get_player_location(player)

        # Case 2: I've reached the depth limit.
        if depth == 0:
            return self.score(game, player), game.get_player_location(player)

        # Case 3: I parse the array of legal moves searching the optimum move
        for move in legal_moves:
            if self.time_left() < self.TIMER_THRESHOLD:
                raise Timeout()
            forecast = game.forecast_move(move)
            score, _ = self.minimax(forecast, depth - 1, not maximizing_player)
            # I'm on a max layer and the new score > current optimal score
            if maximizing_player and score > score_move[0]:
                score_move = (score, move)
            # I'm on a min layer and the new score is < current optimal score
            elif not maximizing_player and score < score_move[0]:
                score_move = (score, move)
        return score_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # Preparing player and (score,move)
        if maximizing_player:
            player = game.active_player
            score_move = (float("-inf"), (-1, -1))
        else:
            player = game.get_opponent(game.active_player)
            score_move = (float("inf"), (-1, -1))

        legal_moves = game.get_legal_moves(game.active_player)

        # Case 1: The game has a winner
        if game.utility(player) != 0:
            return game.utility(player), game.get_player_location(player)

        # Case 2: I've reached the depth limit.
        if depth == 0:
            return self.score(game, player), game.get_player_location(player)

        # Case 3: I parse the array of legal moves searching the optimum move
        for move in legal_moves:
            if self.time_left() < self.TIMER_THRESHOLD:
                raise Timeout()
            forecast = game.forecast_move(move)
            score, _ = self.alphabeta(forecast, depth - 1, alpha, beta, not maximizing_player)
            # I'm on a max layer and the new score > current optimal score
            if maximizing_player:
                if score > score_move[0]:
                    score_move = (score, move)
                if score >= beta:
                    return score, move
                alpha = max(alpha, score)
            # I'm on a min layer and the new score is < current optimal score
            elif not maximizing_player:
                if score < score_move[0]:
                    score_move = (score, move)
                if score <= alpha:
                    return score, move
                beta = min(beta, score)
        return score_move
