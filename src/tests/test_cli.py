import unittest
from unittest.mock import Mock, patch
from io import StringIO
from .. import cli


class TestCLI(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment.
        """
        self.randomizer_mock = Mock()
        self.cli = cli.CLI(self.randomizer_mock, verbose=False)

    def test_init(self):
        """
        Ensure CLI defaults are correct
        """
        # Ensure verbosity defaults to False
        self.assertEqual(self.cli.verbose, False)
        # Ensure randomizer object is passed to the function
        self.assertEqual(self.cli.randomizer, self.randomizer_mock)
        # Ensure initial player count is None
        self.assertEqual(self.cli.players, None)

    @patch('sys.stdout', new_callable=StringIO)
    def test_call_with_invalid_input(self, mock_stdout):
        """
        Ensure the CLI exits when invalid input is given.
        """
        # Exists when player count is not a number.
        with patch('builtins.input', side_effect=['not_a_number']):
            self.assertRaises(SystemExit, self.cli)

    @patch('sys.stdout', new_callable=StringIO)
    def test_call_with_valid_input(self, mock_stdout):
        """
        Ensure changing the player count via the menu works.
        """
        # Ensure setting player count to 3 works.
        with patch('builtins.input', side_effect=['3', 'q']):
            self.assertRaises(SystemExit, self.cli)
            self.assertEqual(self.cli.players, 3)

    @patch('sys.stdout', new_callable=StringIO)
    def test_info(self, mock_stdout):
        """
        Ensure the game info will output correctly.
        """
        # Set up test info
        game = "Test Game"
        info = {
            "pack": "Test Pack",
            "players": 4,
            "description": "Test Description"
        }
        # Check results
        with patch('builtins.input', return_value=''):
            self.cli.info(game, info)
            output = mock_stdout.getvalue()
            self.assertIn(game, output)
            self.assertIn(info["pack"], output)
            self.assertIn(str(info["players"]), output)
            self.assertIn(info["description"], output)


if __name__ == '__main__':
    unittest.main()
