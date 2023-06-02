import unittest
import json
from .. import app


# Unit Tests JSON file
TEST_DATA = {
    "Games": {
        "Game1": {
            "pack": "Pack1",
            "players": 4,
            "description": "A fun game for 4 players.",
            "image": "Game1.png",
            "weight": 1
        },
        "Game2": {
            "pack": "Pack2",
            "players": 2,
            "description": "A game for 2 players.",
            "image": "Game2.png",
            "weight": 1
        }
    },
    "Settings": {
        "Max_Players": 4,
        "Default_Players": 2,
        "Logo": "logo.png",
        "Pack_Label": "Test Pack",
        "Title": "Unit Tests Randomizer",
        "Image_Directory": "unit_tests"
    }
}


class TestRandomizer(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment.
        """
        self.verbose = False
        # Note our test JSON file name,
        self.games_file = 'unit_tests'
        # Set the path so we can write a new copy of it.
        games_json_path = f'src/assets/{ self.games_file }.json'
        # Save test game JSON file to assets folder.
        # Overwrite the existing one in case it was changed.
        with open(games_json_path, 'w') as f:
            json.dump(TEST_DATA, f, indent=4)
        # Setup the Randomizer object
        self.randomizer = app.Randomizer(self.games_file, self.verbose)

    def test_load_info(self):
        """
        Test the load_info function.
        """
        game_info, game_settings = self.randomizer.load_info(self.games_file)
        # Check that we have the correct number of test games.
        self.assertEqual(len(game_info), 2)
        self.assertIn('Game1', game_info)
        self.assertIn('Game2', game_info)
        # Check that test settings are correct.
        self.assertEqual(game_settings,
                         {'Default_Players': 2,
                          'Image_Directory': 'unit_tests',
                          'Logo': 'logo.png',
                          'Max_Players': 4,
                          'Pack_Label': 'Test Pack',
                          'Title': 'Unit Tests Randomizer'})

    def test_games_list(self):
        """
        Test the games_list function.
        """
        # Get the list of games.
        game_list = self.randomizer.games_list()
        # Check that we have the correct games listed
        self.assertEqual(len(game_list), 2)
        self.assertIn('Game1', game_list)
        self.assertIn('Game2', game_list)

    def test_pick_game(self):
        """
        Test the pick_game function for various scenarios
        """
        # Test picking a game for 4 players.
        game, info = self.randomizer.pick_game(4, None)
        self.assertEqual(info['players'], 4)
        self.assertIn(game, ['Game1', 'Game2'])
        # Test picking the only game for 2 players.
        game, info = self.randomizer.pick_game(2, None)
        self.assertIn(game, 'Game2')
        # Test picking game where we previously played the other.
        game, info = self.randomizer.pick_game(4, 'Game2')
        self.assertIn(game, 'Game1')


if __name__ == '__main__':
    unittest.main()
