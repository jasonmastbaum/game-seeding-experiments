import itertools
import random

import numpy as np
import pandas as pd

'''
for this test, we are going to create a two-board tournament where one round 
has already been played
'''
players = ["Brand", "Doug", "Shields", "Jason", "Tanya", "Fogel", "Maletsky",
           "Maslow", "Rousse", "Goffy", "Jamal", "Cubis", "Miller", "Yeargin"]
           #"Karthik", "Justin", "DQ", "Silverman", "Doc", "Edi", "Riaz"]

players_to_index = {player: index for index, player in enumerate(players)}
n = len(players)
player_indices = set(range(n))
n_games = int(len(players)/7)
games_matrix = np.zeros((n,n), dtype=int)

non_diagonals = [(i, j) for i in range(n) for j in range(n) if i != j]
diagonals = [(i, j) for i in range(n) for j in range(n) if i == j]

'''
restricting to upper diagonals from the start avoids having to
handle not randomly sampling both (player1, player2) and (player2, player1)
'''
upper_non_diagonals = np.triu_indices(games_matrix.shape[0], k=1)
upper_non_diagonals = list(zip(upper_non_diagonals[0], upper_non_diagonals[1]))
upper_non_diagonals = [(int(und[0]), int(und[1])) for und in upper_non_diagonals]

for d in diagonals:
    games_matrix[d] = 9999

#num_pairs = sum([1 for i in itertools.combinations(players, 2)])


'''
option a: randomly pick the players who've already played together
'''

'''
n players who've played a game with 6 other people
divide by 2 for symmetry--you don't care about the ordering of the
player pair
'''
#num_ones = int((n*6)/2)
#pair_indices = np.random.choice(len(non_diagonals), num_ones, replace=False)
# pair_indices = np.random.choice(len(upper_non_diagonals), num_ones, replace=False)
# pairs = [non_diagonals[i] for i in pair_indices]

'''
option b: for this test case,
assign first 7 and last 7 players to have played with each other
easier to eyeball if the results look right
for two boards, optimal is each game has 4 players from one game and 3 from another

with randomly assigning leftover players after the initial pairs selection, I think
you can wind up with with that shifting to 5-2/2-5
'''
for pair_index in upper_non_diagonals:
    i, j = pair_index
    if (i < 7) and (j < 7):
        games_matrix[i, j] = 1
    if (i >= 7) and (j >= 7):
        games_matrix[i, j] = 1

'''
had this before restricting to upper triangular selection
this will probably come out but leaving commented for now
'''
# for pair in pairs:
#     games_matrix[pair] = 1
#     games_matrix[pair[::-1]] = 1

'''
Assigns pairs of players to games.
This is intended to generalize to any number of games and any number of rounds,
and also handle an arbitrary number of multi-boarders.

Right now this does scale abritrarily on both the pairs seeding and assigning
the leftover players, but does NOT account for multi-boarders. You have to have
7*n_games distinct players for this code to work as expected. This should work
if you have some players from round 1 drop and new players show up for round 2,
resulting in more pairs of players who haven't already played with each other.

First you assign players who haven't played together yet to games, cycling through the games as you go.
If you run out of players who haven't played together it'll move onto players who've
played once together. If you run out of that (if the round is later than the second round)
it'll move onto players who've played twice together. Etc. It will also stop when all games
have 6 players.

Cycling through the games doesn't matter for placing any given pair of players. The intent
is to make sure you spread the pairs of players out throughout the games instead of potentially
having one initial game seeding stacked all with players who haven't played with each other
and another initial game seeding that has a bunch of players who have already played with each
other.

Next you look at the leftovers from the pairs of players who have played together the
least possible number of times depending on how many bins you moved through. Keep doing this
through bins for increasing numbers of times players have played together. Stop when you get to
all games having 7 players (I think you'd just run out of leftover players and end on that condition
but leaving for now just in case.) Right now this assigns lefotver players to games randomly. I would
like to make this try to place leftover players based on where they increase the fitness score of the
game the least.

TODO: If you still have games that do not have 7 players, that means you have multi-boarders. Pass
this through as a separate list and just iterate through that, assigning players to games that still
need players. May need handling to make sure you don't assign a multiboarder to a game they're already in.
Could have similar handling about placing them in the game where they increase the fitness score the least.

TODO: Finally, there should be something to handle the possibility that players who got assigned to games
from separate pairs do not have an unncessarily high number of times having already played together. As
a starting point, this may be just putting the list of games through the existing improve_fitness function.
I think there's probably a better way doing something like just identifying the problem pairs and then identifying
who you could move where while reducing the problem in the current game without making the problem worse in the game
you're swapping the player to.

'''

#assign pairs of players--gets to at most six players per game
games = [set() for _ in range(int(n_games))]

bins = np.unique(games_matrix)
current_bin = 0
for b in bins:
    current_bin = b
    stop_adding_pairs = False

    rows, columns = np.where(games_matrix == b)
    bin_indices = list(zip(rows, columns))
    bin_entries = set([ (int(bin_index[0]), int(bin_index[1])) for bin_index in bin_indices])

    i = 0
    while len(bin_entries) > 0:
        bin_entry = random.choice(list(bin_entries))
        row = bin_entry[0]
        col = bin_entry[1]
        print("\ngame "+str(i%n_games))
        print("adding ", str(row), " and ", str(col))

        if len(games[i%n_games]) + 2 > 6:
            print("switching from pairs of players to individuals, all games have six players")
            stop_adding_pairs = True
            break
        games[i%n_games].add(row)
        games[i%n_games].add(col)
        i += 1
        for bin_entry in bin_entries:
            if (row in bin_entry) or (col in bin_entry):
                bin_entries = bin_entries - {bin_entry}

    if stop_adding_pairs == True:
        break

print("\ngames after assigning pairs")
for game in games: print(game)

#assign leftover players as the 7th to each game
assigned_players = []
for game in games:
    for player in game:
        assigned_players.append(player)

rows, columns = np.where(games_matrix == b)
bin_indices = list(zip(rows, columns))
bin_entries = set([ (int(bin_index[0]), int(bin_index[1])) for bin_index in bin_indices])
valid_entries = set()
for entry in bin_entries:
    if (entry[0] not in assigned_players) and (entry[1] not in assigned_players):
        valid_entries.add(entry)
players_to_assign = []
for entry in valid_entries:
	for subentry in entry:
		players_to_assign.append(subentry)
#this is a temporary kludge
players_to_assign = set(players_to_assign)
print("remaining players to assign:", players_to_assign)

while len(players_to_assign) > 0:
	player = random.choice(list(players_to_assign))
	game = random.choice([game for game in games if len(game) < 7])
	game.add(player)
	players_to_assign.remove(player)

print("\ngames: ", games)

'''
assign countries for the first game
'''
players_to_assign_countries = list(games[0])


# power_adjacencies_array = [
#     [0,0,0,1,2,2,2],
#     [0,0,2,2,0,2,0],
#     [0,2,0,2,1,0,0],
#     [1,2,2,0,1,2,0],
#     [2,0,1,1,0,2,2],
#     [2,2,0,2,2,0,2],
#     [2,0,0,1,2,2,0]
# ]

power_adjacencies_array = [
    [0,0,0,1,3,3,3],
    [0,0,3,3,0,3,0],
    [0,3,0,3,1,0,0],
    [1,3,3,0,1,3,0],
    [3,0,1,1,0,3,3],
    [3,3,0,3,3,0,3],
    [3,0,0,1,3,3,0]
]

countries = ["Austria", "England", "France", "Germany", "Italy", "Russia", "Turkey"]

power_adjacencies = pd.DataFrame(power_adjacencies_array, index=countries, columns=countries)

'''
for this example we don't care which country people have already played
'''
countries_already_played_array = []
for i in range(7):
    temp = [0]*7
    temp[i] = 1
    countries_already_played_array.append(temp)

countries_already_played = pd.DataFrame(countries_already_played_array,
                                        index=countries,
                                        columns=players_to_assign_countries)
countries_already_played = countries_already_played.transpose()

all_possible_orderings = list(itertools.permutations(players_to_assign_countries))
all_possible_assignments = [list(zip(ordering, countries)) for ordering in all_possible_orderings]

def score_game(game):
    all_pairs = list(itertools.combinations(game, 2))

    already_played = sum(countries_already_played.loc[p]*20 for p in game)

    times_played = [games_matrix[pair[0][0], pair[1][0]] for pair in all_pairs]
    country_adjacencies = [power_adjacencies.loc[pair[0][1], pair[1][1]] for pair in all_pairs]

    adjacency_score = sum([a*b for a, b in zip(times_played, country_adjacencies)])

    return already_played + adjacency_score

assignment_scores = [score_game(game) for game in all_possible_assignments]
print("\nworst score: ", max(assignment_scores))

'''
more than one assignment set could be the best game, so pick just one
'''

best_games = np.where(assignment_scores == min(assignment_scores))[0]
best_game = np.random.choice(best_games, size=1)[0]

assignment = all_possible_assignments[best_game]

print("\nfirst game assigned :",assignment)
print("score: ", score_game(assignment))

'''TODO code below to try to intelligently place the remaining players
based on minimzing number of games played with the players already in
the game is not working, so put in the random placement above for now
'''
# i = 0

# game_scores = []
# for game in games:
# 	score = 0
# 	for index0, player0 in enumerate(game):
# 		for index1, player1 in enumerate(game):
# 			if index0 < index1:
# 				score += games_matrix[index0, index1]
# 	game_scores.append(score)

# for player in players_to_assign:
# 	temp_game_scores = game_scores.copy()
# 	print(temp_game_scores)
# 	for index, game in enumerate(games):
# 		if len(game) < 7:
# 			for assigned_player in game:
# 				temp_game_scores[index] += games_matrix[player, assigned_player]
# 	game_to_assign = temp_game_scores.index(min(temp_game_scores))
# 	print("assigning player ", player, "to game ", game_to_assign)
# 	games[game_to_assign].add(player)

# print(game_scores)
# print("\ngames: ", games)