import sys


class CLI(object):
    """
    Simple CLI menu for the app.
    """
    def __init__(self, randomizer, verbose):
        """
        Set up the variables we need.
        """
        self.verbose = verbose
        self.randomizer = randomizer
        self.players = None

    def __call__(self):
        """
        Run the game by keeping it in a loop.
        """
        # Print the welcome message.
        print('\n*****************\nGame Randomizer!\n*****************\n')
        # Prompt user for players
        if not self.players:
            # If we can't INT it, exit.
            try:
                self.players = int(input('How many players? '))
            except ValueError:
                sys.exit('That didn\'t seem like a number...')
        # Start the program loop.
        while 0 == 0:
            # Call the menu function
            game, info = self.menu()
            # Output the game info.
            if game:
                self.info(game, info)

    def menu(self, game=None):
        """
        Main game menu prompt
        """
        print('\nMenu\n-----\n r - Roll\n',
              'p - Change Player Count\n q - Quit\n')
        m = input()
        # Quit
        if m == 'q':
            sys.exit()
        # Roll for game
        if m == 'r':
            game, info = self.randomizer.pick_game(self.players, game)
            return game, info
        # Change player count
        if m == 'p':
            try:
                self.players = int(input('\nHow many players? '))
                # Return NOTHING!
                return None, None
            except ValueError:
                sys.exit('That didn\'t seem like a number...')
        # Try again if we didn't get a valid input.
        return self.menu()

    def info(self, game, info):
        """
        Print the game info.
        """
        print('\n**********\n%s' % (game))
        print('Pack: %s' % (info['pack']))
        print('Players: %s' % (info['players']))
        print('Description: %s' % (info['description']))
        print('**********')
        # Wait for input before moving on.
        return input('\nHit enter to continue...')
