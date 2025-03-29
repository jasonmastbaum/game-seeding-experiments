'''
this is a performance test for brute forcing the game seeding for a two board tournament

the exact contents of games_matrix don't really matter since this is just testing if it's
computationally feasible (within an amount of time acceptable for a Dip tournametnt) to just
try the entire combinatorics space instead of doing random sampling, so I'm not going to
try to fix things like non-zeros on the diagonal (people playing against themselves)
'''

import numpy as np
import itertools
import multiprocessing
import random
from collections import Counter

#14 unique players
players = ["Brand", "Doug", "Shields", "Jason", "Tanya", "Fogel", "Maletsky",
           "Maslow", "Rousse", "Goffy", "Jamal", "Cubis", "Miller", "Yeargin"]

#13 unique players with one person double-boarding
# players2 = ["Brand", "Brand", "Shields", "Jason", "Tanya", "Fogel", "Maletsky",
#            "Maslow", "Rousse", "Goffy", "Jamal", "Cubis", "Miller", "Yeargin"]

players_to_index = {player: index for index, player in enumerate(players)}

n = len(players)
#games_matrix = np.zeros((n, n), dtype=int)
games_matrix = np.random.randint(0,3, size=(n,n))

# for player1, opponents in games_played.items():
#     for player2, times in opponents.items():
#         i = player_to_index[player1]
#         j = player_to_index[player2]
#         games_matrix[i, j] = times

score = 99999
games_list = []
game_scores = []
#games = game_combinations_with_duplicate(players)
games = game_pairs(players)
i = 0
for x in games: i+=1

for game in games:
    same_player_twice = False
    if  max(Counter(game[0]).values()) > 1 or max(Counter(game[1]).values()) > 1:
        print("same player twice")
        continue
    game0_score = score_game(game[0])
    game1_score = score_game(game[1])
    this_score = game0_score+game1_score
    if this_score < score:
        score = this_score
        game_scores = [game0_score, game1_score]
        games_list = game

def generate_games(players):
    # assumes players%7 == 0
    all_combinations = itertools.combinations(players, 7)
    # Create an iterator for the pairs of games
    for first_game in all_combinations:
        remaining_players = set(players) - set(first_game)
        for second_game in itertools.combinations(remaining_players, 7):
            yield (first_game, second_game)

def game_pairs(players):
    # Generate all combinations of 7 players from the 14
    all_combinations = itertools.combinations(players, 7)
    # Create an iterator for the pairs of games
    for first_game in all_combinations:
        remaining_players = set(players) - set(first_game)
        for second_game in itertools.combinations(remaining_players, 7):
            yield (first_game, second_game)

def game_combinations_with_duplicate(players):
    # Iterate over each player to be the duplicate player
    for duplicate_player in players:
        # Remaining players after choosing the duplicate player
        remaining_players = set(players) - {duplicate_player}
        # Generate all combinations of 6 players from the remaining 12
        for first_game in itertools.combinations(remaining_players, 6):
            # The second game consists of the duplicate player and the remaining players
            second_game = (duplicate_player,) + tuple(set(remaining_players) - set(first_game))
            yield (first_game, second_game)

def score_game(game):
    #game is a list of players in the game
    pairs_iterator = itertools.combinations(game, 2)
    #all_pairs = [pair for pair in pairs_iterator]
    fitness_score = sum([games_matrix[players_to_index[pair[0]]][players_to_index[pair[1]]] for pair in pairs_iterator])
    #fitness_scores = [games_matrix[players_to_index[pair[0]]][players_to_index[pair[1]]] for pair in all_pairs]
    return fitness_score


all_combinations_iterator = itertools.chain.from_iterable(itertools.combinations(game1_players, r) for r in range(1, len(game1_players) + 1))
fitness_score = []


def score_permutation(permutation):
    # Define your objective function here
    # Example: return sum(permutation)


for p in game:
    for q in game:
        if p != q:
            try:
                f += (games_played_matrix[p][q] ** 2)
            except KeyError:
                # These players have not played each other
                pass

def process_permutations(permutations):
    best_score = float('-inf')
    best_permutation = None
    for perm in permutations:
        score = score_permutation(perm)
        if score > best_score:
            best_score = score
            best_permutation = perm
    return best_permutation, best_score

def main():
    people = list(range(1, 15))  # Example list of 14 people
    all_permutations = itertools.permutations(people, 14)

    # Use multiprocessing to handle permutations in parallel
    num_workers = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(num_workers)
    
    # Split permutations into chunks for each worker
    chunk_size = 1000  # Adjust based on memory and performance
    chunks = [list(itertools.islice(all_permutations, chunk_size)) for _ in range(num_workers)]
    
    results = pool.map(process_permutations, chunks)
    
    # Find the best overall permutation
    best_overall_score = float('-inf')
    best_overall_permutation = None
    for best_permutation, best_score in results:
        if best_score > best_overall_score:
            best_overall_score = best_score
            best_overall_permutation = best_permutation

    print("Best permutation:", best_overall_permutation)
    print("Best score:", best_overall_score)

if __name__ == "__main__":
    main()
