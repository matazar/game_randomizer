import os
import random
import argparse
import json
from .gui import GUI
from .cli import CLI
from pkg_resources import resource_filename


class Randomizer(object):
    """
    Randomizer class to handle the game picking.
    """
    def __init__(self, games, verbose):
        """
        Set up our variables and load the games json file.
        """
        self.verbose = verbose
        # Load the games from the json file.
        self.game_info, self.game_settings = self.load_info(games)
        self.played_games = []
        # Store stats based on json filename
        stats_filename = '%s_stats.json' % (games)
        # Set the stats file in the home directory.
        self.stats_file = os.path.join(os.path.expanduser('~'),
                                       '.game_randomizer', stats_filename)
        self.game_stats = self.load_stats()

    def load_info(self, games):
        """
        Loads the data from the JSON file.
        """
        # Figure out the path based on the current environment.
        json_path = resource_filename('game_randomizer',
                                      os.path.join(
                                          'assets',
                                          f'{games}.json'))
        if self.verbose:
            print(f'Loading games from { json_path }')
        # Open the file
        with open(json_path) as f:
            results = json.loads(f.read())
        # Return the games and settings.
        return results['Games'], results['Settings']

    def load_stats(self):
        """
        Loads the data from the stats JSON file.
        """
        # Try to open our stats file.
        try:
            with open(self.stats_file) as f:
                results = json.loads(f.read())
            # Update the stats to add new games.
            for g in self.game_info.keys():
                if g not in results:
                    results[g] = 0
        # Create a new stats file if it doesn't exist.
        except FileNotFoundError:
            if self.verbose:
                print('No stats file, creating new.')
            # Set up new stats
            results = {}
            for g in self.game_info.keys():
                results[g] = 0
        return results

    def save_stats(self):
        """
        Save the game occurence stats to a file so we can track them between
        sessions.
        """
        # Ensure the directory exists.
        if not os.path.isdir(os.path.dirname(self.stats_file)):
            os.makedirs(os.path.dirname(self.stats_file))
        # Write out the stats
        with open(self.stats_file, 'w') as f:
            f.write(json.dumps(self.game_stats, indent=4))

    def view_stats(self):
        """
        Return an up-to-date copy of the game played stats.
        """
        return self.game_stats

    def settings(self):
        """
        Returns a copy of the settings from the JSON file.
        """
        return self.game_settings

    def games_list(self):
        """
        Returns a list of games and their info.
        """
        return self.game_info

    def pick_game(self, player_count, prev_game):
        """
        Pick a game from a list of avialable games,
        then update the played stats.
        """
        # Create a list to hold the games
        games = []
        # Another for the weights
        weights = []
        # Compute the maximum occurrence of all games.
        max_occurrence = max([self.game_stats[g] for g in self.game_stats])
        # Add games that allow for the current player count.
        for g in self.game_info:
            if (self.game_info[g]['players'] >= player_count and
                    g not in self.played_games):
                games.append(g)
                # Rank games in reverse order of occurrence and
                # according to preference.
                reverse_occurrence = max_occurrence + 1 - self.game_stats[g]
                weights.append(self.game_info[g]['weight'] *
                               reverse_occurrence)
        # Reset games played if we've gone through the entire list.
        if len(games) < 1 and len(self.played_games) > 0:
            # Reset games played
            self.played_games = []
            for g in self.game_info:
                if (self.game_info[g]['players'] >= player_count and
                        g not in self.played_games):
                    games.append(g)
                    # Rank games in reverse order of occurrence and
                    # according to preference.
                    reverse_occurrence = max_occurrence + 1 - \
                        self.game_stats[g]
                    weights.append(self.game_info[g]['weight'] *
                                   reverse_occurrence)
        # Pick the game
        game = random.choices(population=games, weights=weights)[0]
        # Update the states.
        self.game_stats[game] += 1
        self.played_games.append(game)
        # Save the occurrence data.
        self.save_stats()
        # Return the game and its info.
        return game, self.game_info[game]


def main_app(games_json, useCLI, verbose):
    """
    Main App.
    """
    # Create instance with game data.
    randomizer = Randomizer(games_json, verbose)
    if useCLI:
        # CLI version
        p = CLI(randomizer, verbose)
        p()
    else:
        # GUI version
        g = GUI(randomizer, verbose)
        g()


def main():
    """
    Set up main entry point using argparse.
    """
    parser = argparse.ArgumentParser(
        description="Run the Game Randomizer! A GUI random game selector.")
    parser.add_argument('-v', '--verbose',
                        help='Enable verbose output.', action='store_true')
    parser.add_argument('-c', '--cli',
                        help="Run the CLI game randomizer.",
                        action='store_true')
    parser.add_argument('games',
                        choices=['boardgames', 'jackbox_games', 'unit_tests'],
                        help='The name of the JSON file ' +
                             'containing the games information.')
    parser.parse_args()
    args = parser.parse_args()

    main_app(args.games, args.cli, args.verbose)


if __name__ == "__main__":
    main()
