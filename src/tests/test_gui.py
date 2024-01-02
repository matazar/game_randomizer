import unittest
from .. import gui


class TestJSONGUI(unittest.TestCase):

    def test_default_json_files(self):
        """
        Test that asset data exists and the defaults are listed in json_files.
        """
        # Instantiate the SelectJsonGUI
        app = gui.JSONGUI()

        # Check that all default options are in json_files
        self.assertIn('unit_tests', app.json_files)
        self.assertIn('boardgames', app.json_files)
        self.assertIn('jackbox_games', app.json_files)

    def test_json_select(self):
        """
        Test that the select() function sets the JSON file properly.
        """
        # Instantiate the SelectJsonGUI
        app = gui.JSONGUI()

        # Set the dropdown menu value to the unit_tests.
        app.selected_file.set('unit_tests')

        # Call the method that should set self.selected
        selected = app.select()

        # Check that the returned value is as expected
        self.assertEqual(selected, 'unit_tests')

    def test_exit(self):
        """
        Test that select_and_exit sets the selected attribute properly.
        """
        # Instantiate the SelectJsonGUI
        app = gui.JSONGUI()

        # Set the selected_file StringVar to a known value
        app.selected_file.set('unit_tests')

        # Exit the app.
        selected = app.exit()
        # Check that None is returned.
        self.assertIsNone(selected)


if __name__ == '__main__':
    unittest.main()
