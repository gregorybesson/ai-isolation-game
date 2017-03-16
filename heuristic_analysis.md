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

After many "heuristic tentatives", playing with paramaters, I end up with 3 heuristic trying to find a way to beat the ID improved heuristic:
- Heuristic 1: Aggressive player
- Heuristic 2: Aggressive player trying to keep the center
- Heuristic 3: Aggressive player trying to keep center While 60% of the game board is free, then becoming more defensive.


# Heuristic 1: Aggressive player
## Description
This one is directly inspired from the lecture: We'll be really aggressive using a multiplier to take the opponent available moves into account.
```
player_moves = len(game.get_legal_moves(player))
opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))
return float(player_moves) - 2 * float(opponent_moves)
```
## Results

# Heuristic 2: Aggressive player trying to keep the center
## Description
## Results

# Heuristic 3: Aggressive player trying to keep center While 60% of the game board is free, then becoming more defensive.
## Description
## Results

# Conclusion / next steps
