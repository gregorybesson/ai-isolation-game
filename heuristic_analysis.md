# Introduction
ID Improved is an interesting evaluation function which uses the available moves from both players. 
It denotes a moderately aggressive play, trying to maximize available moves from the AI while reducing the number of available moves from the opponent.

The result is not that bad, and I feel from the beginning that I'll have to try hard to find a better AI.

I've taken a paper and a pen, played manually, trying to understand the "hidden rules" behind this original game: The moves available are the ones a knight can do in Chess game.
here is the list I've created after this analysis, containing the parameters I felt they could impact the success of my AI:

- Number of available moves for the AI
- Number of available moves for the opponent
- The location of particular moves: It seemed to me that we should avoid as much as possible the edges of the game board
- The distance of a move from the edge of the game board (similar to the previous observation but seen as continuous behavior instead of a precise area
- The relative distance between both players: If I can follow my opponent being one square away from him, it seems I can avoid his attacks more easily
- The behavior I should have during the game: Agressive or defensive ? Does it have to change during the game ?
- Following the previous sentence, Should I try to take a square when the opponent has this square as option (attack) or should I avoid it ?

After many "heuristic tentatives", playing with paramaters, I ended up with 3 heuristics trying to find a way to beat the ID improved heuristic:
- Heuristic 1: Aggressive player
- Heuristic 2: Moderately aggressive player trying to keep the center
- Heuristic 3: Aggressive player While 60% of the game board is free, then becoming less aggressive but trying to keep the center.


# Heuristic 1: Aggressive player
## Description
This one is directly inspired from the lecture: We'll be really aggressive using a multiplier to take the opponent available moves into account.
```
player_moves = len(game.get_legal_moves(player))
opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))
return float(player_moves) - 4 * float(opponent_moves)
```
## Results
### Data
```
*************************
 Evaluating: ID_Improved 
*************************

Playing Matches:
----------
tournament.py:100: UserWarning: One or more agents lost a match this round due to timeout. The get_move() function must return before time_left() reaches 0 ms. You will need to leave some time for the function to return, and may need to increase this margin to avoid timeouts during  tournament play.
  warnings.warn(TIMEOUT_WARNING)
  Match 1: ID_Improved vs   Random    	Result: 15 to 5
  Match 2: ID_Improved vs   MM_Null   	Result: 14 to 6
  Match 3: ID_Improved vs   MM_Open   	Result: 14 to 6
  Match 4: ID_Improved vs MM_Improved 	Result: 10 to 10
  Match 5: ID_Improved vs   AB_Null   	Result: 12 to 8
  Match 6: ID_Improved vs   AB_Open   	Result: 14 to 6
  Match 7: ID_Improved vs AB_Improved 	Result: 15 to 5


Results:
----------
ID_Improved         67.14%

*************************
   Evaluating: Student   
*************************

Playing Matches:
----------
  Match 1:   Student   vs   Random    	Result: 18 to 2
  Match 2:   Student   vs   MM_Null   	Result: 16 to 4
  Match 3:   Student   vs   MM_Open   	Result: 12 to 8
  Match 4:   Student   vs MM_Improved 	Result: 13 to 7
  Match 5:   Student   vs   AB_Null   	Result: 17 to 3
  Match 6:   Student   vs   AB_Open   	Result: 11 to 9
  Match 7:   Student   vs AB_Improved 	Result: 12 to 8


Results:
----------
Student             70.71%
```
### Analysis
The results have been tested 5 times on tournaments of 20 games. It shows a tiny improvement over ID_Improved. Don't have a precise explanantion. I feel being aggressive in this game is important but maybe my multiplier is to high and "hide" better options for the player, while taking too much into account the reduction of the opponent's moves.

# Heuristic 2: Aggressive player trying to keep the center
## Description
I refrain a little bit my aggressivity (the multiplier is reduced to 1), but this time I take into account the 9 squares composing the center of the board. And I will privilege these moves for the player while trying to reduce the center moves from my opponent.

```
center_x = game.width//2
center_y = game.height//2
center_locations = [(x, y) for x in [center_x - 1, center_x, center_x + 1] for y in [center_y - 1, center_y, center_y + 1]]

player_moves = len(game.get_legal_moves(player))
opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))

player_center_moves = len([m for m in game.get_legal_moves(player) if m in center_locations])
opponent_center_moves = len([m for m in game.get_legal_moves(game.get_opponent(player)) if m in center_locations])

return ((player_moves + player_center_moves) - (opponent_moves + opponent_center_moves))
```

## Results
### data
```
*************************
 Evaluating: ID_Improved 
*************************

Playing Matches:
----------
tournament.py:100: UserWarning: One or more agents lost a match this round due to timeout. The get_move() function must return before time_left() reaches 0 ms. You will need to leave some time for the function to return, and may need to increase this margin to avoid timeouts during  tournament play.
  warnings.warn(TIMEOUT_WARNING)
  Match 1: ID_Improved vs   Random    	Result: 16 to 4
  Match 2: ID_Improved vs   MM_Null   	Result: 13 to 7
  Match 3: ID_Improved vs   MM_Open   	Result: 11 to 9
  Match 4: ID_Improved vs MM_Improved 	Result: 12 to 8
  Match 5: ID_Improved vs   AB_Null   	Result: 15 to 5
  Match 6: ID_Improved vs   AB_Open   	Result: 13 to 7
  Match 7: ID_Improved vs AB_Improved 	Result: 13 to 7


Results:
----------
ID_Improved         66.43%

*************************
   Evaluating: Student   
*************************

Playing Matches:
----------
  Match 1:   Student   vs   Random    	Result: 17 to 3
  Match 2:   Student   vs   MM_Null   	Result: 17 to 3
  Match 3:   Student   vs   MM_Open   	Result: 14 to 6
  Match 4:   Student   vs MM_Improved 	Result: 13 to 7
  Match 5:   Student   vs   AB_Null   	Result: 17 to 3
  Match 6:   Student   vs   AB_Open   	Result: 15 to 5
  Match 7:   Student   vs AB_Improved 	Result: 14 to 6


Results:
----------
Student             76.43%
```
### Analysis
The results have been tested 5 times on tournaments of 20 games. They show an average improvement of 10% compared to the improved heuristic. It seems that I'm on the right way: Being moderately aggressive while taking the center of the board into account has a positive impact on my AI success, which seems to me quite logical, as these squares are the ones giving the highest number of options for the future moves. 

# Heuristic 3: Aggressive player while 60% of the game board is free, then becoming less aggressive keeping the center
## Description
I think that the strategy should evolve during the game... with the feeling that aggressivity is key during the first part of the game, then trying to keep the center during the second part of the game, while being less aggressive.

```
def adaptive(game, player):
    board_size = game.height * game.width
    moves_to_board = game.move_count / board_size
    
    if moves_to_board > 0.4:
        return aggressive(game, player)
    else:
        return aggressive_center(game, player)
```
## Results
### Data

### Analysis


# Conclusion / next steps
I feel I've clearly stumbled upon an important parameter with the hidden rule "keep the center !"
As explained in my analysis, is seems logical to me as these squares have the highest number of future options, so optimizing these options for me while trying to reduce it for my opponent is a good starting point.

I'm quite happy with the results, but I feel I could go much further. I think that my AI should adapt its strategy during the game. For example, I thought that following my opponent's path being close to him (1 square away from him) was a good option as a first player during the first part of the game. But my first tries haven't been successfull...
Another feeling concerns the symmetries of the game. I've not done anything with it, but I think I could be more efficient taking that into account.

Last but not least, I should tweak the multipliers and levels to find the most accurate results.
Great experience anyway. And a new work in progress with the objective of improving this AI.
